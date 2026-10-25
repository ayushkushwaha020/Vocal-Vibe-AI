"""Privacy-conscious first-pass vocal feature API for VocalVibe AI.

This service computes acoustic descriptors, not a medical diagnosis, full vocal
range classification, or celebrity similarity score. Uploaded audio is processed
in memory and is not persisted by this application.
"""
from __future__ import annotations

import io
import logging
import os
from typing import Any

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import correlate
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("vocalvibe.api")

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_DURATION_SECONDS = 50
ALLOWED_CONTENT_TYPES = {
    "audio/wav", "audio/x-wav", "audio/wave", "audio/vnd.wave",
    "audio/flac", "audio/x-flac", "application/octet-stream",
}
TARGET_SAMPLE_RATE = 22050

app = FastAPI(
    title="VocalVibe AI Audio API",
    description="First-pass acoustic feature extraction for singing practice.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)
origins = [x.strip() for x in os.getenv(
    "FRONTEND_ORIGIN", "http://localhost:3000,https://vocal-vibe-ai.onrender.com"
).split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

class VocalFeatures(BaseModel):
    duration_seconds: float
    sample_rate_hz: int
    rms_energy: float
    estimated_pitch_median_hz: float | None
    estimated_pitch_p10_hz: float | None
    estimated_pitch_p90_hz: float | None
    voiced_frame_ratio: float
    spectral_centroid_mean_hz: float
    zero_crossing_rate_mean: float
    tempo_estimate_bpm: float | None
    notes: list[str]

def analyze_audio_bytes(data: bytes) -> dict[str, Any]:
    """Decode bounded audio and compute transparent, first-pass descriptors."""
    try:
        audio, sr = librosa.load(io.BytesIO(data), sr=TARGET_SAMPLE_RATE, mono=True)
    except Exception as exc:
        logger.info("Audio decode rejected: %s", type(exc).__name__)
        raise HTTPException(
            status_code=415,
            detail="Unsupported or unreadable audio. Upload a valid WAV or FLAC file.",
        ) from exc

    if audio.size == 0:
        raise HTTPException(status_code=422, detail="Audio file contains no samples.")
    duration = float(audio.size / sr)
    if duration < 1.0:
        raise HTTPException(status_code=422, detail="Audio must be at least 1 second long.")
    if duration > MAX_DURATION_SECONDS:
        raise HTTPException(
            status_code=413,
            detail=f"Audio must be {MAX_DURATION_SECONDS} seconds or shorter.",
        )
    if not np.isfinite(audio).all():
        raise HTTPException(status_code=422, detail="Audio contains invalid numeric samples.")

    rms = librosa.feature.rms(y=audio, hop_length=1024)[0]
    centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, hop_length=1024)[0]
    zcr = librosa.feature.zero_crossing_rate(y=audio, hop_length=1024)[0]
    # pYIN is more expensive and can fail on short/noisy samples; use YIN and
    # keep only estimates in a broad singing-frequency range.
    try:
        f0 = librosa.yin(audio, fmin=65, fmax=1000, sr=sr, frame_length=2048, hop_length=1024)
        frame_rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=1024)[0]
        if frame_rms.size != f0.size:
            frame_rms = np.interp(
                np.linspace(0, 1, f0.size),
                np.linspace(0, 1, frame_rms.size),
                frame_rms,
            )
        voiced = f0[(frame_rms > max(0.008, float(np.max(frame_rms)) * 0.12)) & np.isfinite(f0)]
    except Exception:
        logger.exception("Pitch estimation failed")
        voiced = np.array([], dtype=float)

    # Estimate tempo from the already-computed RMS envelope instead of
    # running librosa's full onset/beat-tracking pipeline. This is much cheaper
    # for short voice samples; treat it as a rough rhythm hint, not a music BPM.
    tempo = None
    if rms.size >= 12:
        envelope = np.asarray(rms, dtype=np.float64)
        envelope = envelope - np.mean(envelope)
        norm = float(np.linalg.norm(envelope))
        if norm > 1e-9:
            envelope /= norm
            # RMS frames use librosa's default 512-sample hop.
            min_lag = max(1, int((60.0 / 200.0) * sr / 512))
            max_lag = min(len(envelope) - 1, int((60.0 / 50.0) * sr / 512))
            if max_lag > min_lag:
                correlations = correlate(envelope, envelope, mode="full", method="fft")[len(envelope)-1:]
                lag = min_lag + int(np.argmax(correlations[min_lag:max_lag + 1]))
                candidate = 60.0 * sr / (512 * lag)
                if 50 <= candidate <= 200:
                    tempo = float(candidate)

    notes = [
        "These measurements are estimates from this sample, not a diagnosis or a complete vocal-range assessment.",
        "Record in a quiet room and avoid straining to reach notes.",
        "Only the uploaded microphone recording is analyzed; use headphones to prevent song playback from leaking acoustically into the mic. This API processes the upload in memory and does not save the audio file.",
    ]
    pitch = {
        "estimated_pitch_median_hz": round(float(np.median(voiced)), 2) if voiced.size else None,
        "estimated_pitch_p10_hz": round(float(np.percentile(voiced, 10)), 2) if voiced.size else None,
        "estimated_pitch_p90_hz": round(float(np.percentile(voiced, 90)), 2) if voiced.size else None,
        "voiced_frame_ratio": round(float(voiced.size / max(1, f0.size)), 3) if "f0" in locals() else 0.0,
    }
    return {
        "duration_seconds": round(duration, 3),
        "sample_rate_hz": sr,
        "rms_energy": round(float(np.mean(rms)), 6),
        **pitch,
        "spectral_centroid_mean_hz": round(float(np.mean(centroid)), 2),
        "zero_crossing_rate_mean": round(float(np.mean(zcr)), 5),
        "tempo_estimate_bpm": round(tempo, 2) if tempo is not None else None,
        "notes": notes,
    }

@app.get("/", tags=["operations"])
def root() -> dict[str, str]:
    """Provide a useful service landing response instead of a generic 404."""
    return {
        "service": "VocalVibe AI Audio API",
        "status": "ok",
        "health": "/health",
        "docs": "/docs",
        "analyze": "/api/v1/analyze",
    }

@app.get("/health", response_model=HealthResponse, tags=["operations"])
@app.get("/healthz", response_model=HealthResponse, include_in_schema=False)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="vocal-vibe-audio-api", version="0.1.0")

@app.post("/api/v1/analyze", response_model=VocalFeatures, tags=["analysis"])
async def analyze(file: UploadFile = File(...)) -> dict[str, Any]:
    content_type = (file.content_type or "").lower().split(";")[0].strip()
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Upload a WAV or FLAC audio file.")
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if not data:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Maximum upload size is 10 MB.")
    return analyze_audio_bytes(data)
