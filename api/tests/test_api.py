import io

import numpy as np
import soundfile as sf
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "vocal-vibe-audio-api"

def test_rejects_unsupported_content_type():
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("song.mp3", b"not audio", "audio/mpeg")},
    )
    assert response.status_code == 415

def test_rejects_empty_upload():
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("empty.wav", b"", "audio/wav")},
    )
    assert response.status_code == 422

def test_rejects_upload_over_limit():
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("huge.wav", b"x" * (main.MAX_UPLOAD_BYTES + 1), "audio/wav")},
    )
    assert response.status_code == 413

def test_analyze_synthetic_tone(monkeypatch):
    sr = 22050
    time = np.arange(sr * 3) / sr
    tone = 0.2 * np.sin(2 * np.pi * 220 * time)
    buffer = io.BytesIO()
    sf.write(buffer, tone, sr, format="WAV")
    payload = buffer.getvalue()
    result = main.analyze_audio_bytes(payload)
    assert 2.9 <= result["duration_seconds"] <= 3.1
    assert result["sample_rate_hz"] == sr
    assert result["rms_energy"] > 0
    assert result["estimated_pitch_median_hz"] is not None
    assert abs(result["estimated_pitch_median_hz"] - 220) < 20
