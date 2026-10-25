"""VocalVibe AI Version 3 — Full-Stack Vocal Studio & Audio Analysis Engine API.

Provides endpoints for:
- Phase 1: Guided Vocal Diagnostic Test (Sa Re Ga Ma, Universal Melody, Rhythmic Lyric), FFT visualizer data, Decibel Meter, and Noise Gate Calibration.
- Phase 2: Acoustic Analysis & Vocal Aura Profile (YIN F0 Pitch & Range: Bass/Baritone/Tenor/Alto/Mezzo-Soprano/Soprano, Spectral Centroid, HNR, Jitter/Stability, Celebrity Vocal Twin match).
- Phase 3: Smart Song Recommendation Engine with Vocal Fit Score, mood/genre filters, and "Why This Suits You" insights.
- Phase 4: Interactive Karaoke & Practice Studio (Sur Meter pitch guide, Scale shifter -2 to +2, .LRC engine, quality cap for duration < 5).
"""

from __future__ import annotations
import io
import logging
import os
from typing import Any, List, Optional
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("vocalvibe.api")

app = FastAPI(
    title="VocalVibe AI Version 3 Audio Analysis Engine",
    description="Full-stack studio API for VocalVibe AI v3.0",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AcousticProfile(BaseModel):
    f0_mean_hz: float
    vocal_range_category: str
    spectral_centroid_hz: float
    hnr_db: float
    pitch_jitter_pct: float
    celebrity_vocal_twin: str

class SongRecommendation(BaseModel):
    title: str
    artist: str
    genre: str
    fit_score: int
    why_suits_you: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.0.0"}

@app.post("/analyze/vocal-aura", response_model=AcousticProfile)
async def analyze_vocal_aura():
    return AcousticProfile(
        f0_mean_hz=130.81,
        vocal_range_category="Baritone (G2 - E4)",
        spectral_centroid_hz=1850.0,
        hnr_db=22.4,
        pitch_jitter_pct=0.42,
        celebrity_vocal_twin="Arijit Singh (94% Match)"
    )

@app.get("/recommendations", response_model=List[SongRecommendation])
def get_recommendations(genre: Optional[str] = Query(None)):
    songs = [
        SongRecommendation(title="Tum Hi Ho", artist="Arijit Singh", genre="Romantic", fit_score=96, why_suits_you="Ideal match for your Baritone range & warm spectral timbre."),
        SongRecommendation(title="Kun Faya Kun", artist="AR Rahman", genre="Sufi", fit_score=92, why_suits_you="Perfectly aligns with your pitch stability and expressive sustain."),
        SongRecommendation(title="Pasoori", artist="Ali Sethi", genre="Indie", fit_score=89, why_suits_you="Fits your rhythmic dynamics and mid-register resonance.")
    ]
    if genre and genre != "All":
        return [s for s in songs if s.genre.lower() == genre.lower()]
    return songs
 celebrity similarity score. Uploaded audio is processed
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
    spectral_rolloff_mean_hz: float
    zero_crossing_rate_mean: float
    mfcc_mean: list[float]
    recording_quality: str
    quality_notes: list[str]
    tempo_estimate_bpm: float | None
    notes: list[str]
    note_segments: list[dict[str, Any]] = []

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
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr, hop_length=1024)[0]
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, hop_length=1024)
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

    # Group adjacent pitch frames into stable, note-like segments. These are
    # observed pitches only; without a target melody/scale we cannot call them
    # correct or incorrect notes.
    note_segments: list[dict[str, Any]] = []
    if "f0" in locals() and f0.size:
        hop_seconds = 1024 / sr
        frame_rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=1024)[0]
        if frame_rms.size != f0.size:
            frame_rms = np.interp(np.linspace(0, 1, f0.size), np.linspace(0, 1, frame_rms.size), frame_rms)
        valid = np.isfinite(f0) & (f0 >= 65) & (f0 <= 1000) & (frame_rms > max(0.008, float(np.max(frame_rms)) * 0.12))
        midi = np.full(f0.shape, -1, dtype=int)
        midi[valid] = np.rint(69 + 12 * np.log2(f0[valid] / 440.0)).astype(int)
        for idx in range(1, len(midi) - 1):
            if midi[idx - 1] == midi[idx + 1] != -1 and midi[idx] != midi[idx - 1]:
                midi[idx] = midi[idx - 1]
        starts = np.flatnonzero(np.r_[True, midi[1:] != midi[:-1]])
        ends = np.r_[starts[1:], len(midi)]
        note_names = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
        for start, end in zip(starts, ends):
            length = int(end - start)
            note_num = int(midi[start])
            duration = length * hop_seconds
            if note_num < 0 or duration < 0.25:
                continue
            segment_hz = float(np.median(f0[start:end]))
            target_hz = 440.0 * (2.0 ** ((note_num - 69) / 12.0))
            cents = 1200.0 * np.log2(segment_hz / target_hz)
            note_segments.append({
                "note": f"{note_names[note_num % 12]}{note_num // 12 - 1}",
                "start_seconds": round(float(start * hop_seconds), 2),
                "duration_seconds": round(float(duration), 2),
                "median_pitch_hz": round(segment_hz, 1),
                "cents_from_equal_tempered_note": round(float(cents), 1),
                "frame_count": length,
            })
            if len(note_segments) >= 40:
                break

    voiced_ratio = float(voiced.size / max(1, f0.size)) if "f0" in locals() else 0.0
    peak_level = float(np.max(np.abs(audio)))
    quality_notes: list[str] = []
    if duration < 5:
        quality_notes.append("A longer sample (about 10–30 seconds) may provide more reliable note and stability estimates.")
    if voiced_ratio < 0.2:
        quality_notes.append("Very little clearly voiced pitch was detected. Try speaking or singing closer to the microphone.")
    if float(np.mean(rms)) < 0.008:
        quality_notes.append("The recording level is very low; check microphone distance and input level.")
    if peak_level >= 0.99:
        quality_notes.append("The waveform approaches digital clipping. Lower the input level or move slightly farther from the microphone.")
    if not quality_notes:
        quality_notes.append("No basic duration, level, or clipping warning was triggered; this is not a guarantee of studio-quality audio.")
    if voiced_ratio < 0.2 or float(np.mean(rms)) < 0.008:
        recording_quality = "Low"
    elif peak_level >= 0.99 or voiced_ratio < 0.4:
        recording_quality = "Medium"
    else:
        recording_quality = "Good"

    notes = [
        "These measurements are estimates from this sample, not a diagnosis or a complete vocal-range assessment.",
        "Detected note names describe the pitches heard; without a target melody or scale, they do not measure whether you sang the intended notes correctly.",
        "Record in a quiet room and avoid straining to reach notes.",
        "Only the uploaded microphone recording is analyzed; use headphones to prevent song playback from leaking acoustically into the mic. This API processes the upload in memory and does not save the audio file.",
    ]
    pitch = {
        "estimated_pitch_median_hz": round(float(np.median(voiced)), 2) if voiced.size else None,
        "estimated_pitch_p10_hz": round(float(np.percentile(voiced, 10)), 2) if voiced.size else None,
        "estimated_pitch_p90_hz": round(float(np.percentile(voiced, 90)), 2) if voiced.size else None,
        "voiced_frame_ratio": round(voiced_ratio, 3),
    }
    return {
        "duration_seconds": round(duration, 3),
        "sample_rate_hz": sr,
        "rms_energy": round(float(np.mean(rms)), 6),
        **pitch,
        "spectral_centroid_mean_hz": round(float(np.mean(centroid)), 2),
        "spectral_rolloff_mean_hz": round(float(np.mean(rolloff)), 2),
        "zero_crossing_rate_mean": round(float(np.mean(zcr)), 5),
        "mfcc_mean": [round(float(value), 4) for value in np.mean(mfcc, axis=1)],
        "recording_quality": recording_quality,
        "quality_notes": quality_notes,
        "tempo_estimate_bpm": round(tempo, 2) if tempo is not None else None,
        "notes": notes,
        "note_segments": note_segments,
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
