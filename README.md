# VocalVibe AI — Version 3 Studio

VocalVibe AI Version 3 is a comprehensive, full-stack vocal studio and acoustic analysis platform.

## 🌟 Full 4-Phase VocalVibe AI Studio

### Phase 1: 30-Second Guided Vocal Diagnostic Test
- **Prompts:** Sa Re Ga Ma (Classical Scale), Universal Melody, Rhythmic Lyric
- **Real-Time Visualizers:** Live FFT & Waveform visualizers, Decibel Meter (-INF to 0 dB)
- **Calibration:** Noise Gate calibration to filter background acoustic noise

### Phase 2: Acoustic Analysis & Vocal Aura Profile
- **YIN F0 Pitch Analysis & Range:** Classification into Bass, Baritone, Tenor, Alto, Mezzo-Soprano, Soprano
- **Spectral Centroid:** Timbre brightness/weight estimation
- **Harmonic-to-Noise Ratio (HNR):** Voice clarity vs. huskiness metric
- **Pitch Jitter & Stability:** Sustain stability measurement
- **Celebrity Vocal Twin Match:** AI-powered vocal similarity matching

### Phase 3: Smart Song Recommendation Engine
- **Vocal Fit Score Badges:** Dynamic percentage matching based on user vocal profile
- **Mood & Genre Filters:** Romantic, Sufi, Indie, Retro, Sad, Rap/Hip-Hop, High-Energy
- **Insights:** "Why This Suits You" personalized reasoning for every song recommendation

### Phase 4: Interactive Karaoke & Practice Studio
- **Synthesized Backing Track & Lyrics:** Time-synced `.LRC` lyrics engine
- **Real-Time Pitch Guide (Sur Meter):** Octave-normalized pitch-class comparison (`const semitoneDiff = Math.abs(((midi % 12) - (target % 12) + 12) % 12); const normalizedDiff = Math.min(semitoneDiff, 12 - semitoneDiff);`)
- **Scale / Pitch Shifter:** Transpose backing track from `-2` to `+2` semitones
- **Note Rendering:** HTML-escaped note rendering (`String(m.note).replace(/[&<>"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]))`)
- **Quality Safeguards:** `recording_quality` automatically capped at `'Medium'` when `duration < 5`

## 🚀 Getting Started

```bash
# Frontend
open index.html

# Backend API
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```
 practice workspace.

## V2 product direction

Version 2 is a rebuild around the supplied VocalVibe AI blueprint. New V2 work is developed separately before promotion; preserve the baseline branch as a fallback.

## Current V2 experience

- **Vocal assessment:** Sa Re Ga Ma scale, universal melody, rhythmic lyric, or sustained-vowel prompt; record up to 30 seconds; live waveform and progress meter.
- **Browser audio capture:** microphone permission flow, optional echo cancellation/noise suppression and auto gain control, live pitch estimate, recording timer, and WAV conversion of captured PCM.
- **Vocal Aura:** API-derived median pitch and percentile range, broad pitch-zone estimate, spectral brightness clue, RMS energy, voiced-frame ratio, rough tempo hint, recording-quality checks, MFCC vector size, and detected note segments.
- **Song discovery:** mood filters and original practice prompts. Compatibility scores and celebrity vocal twin percentages are not fabricated without validated song/artist reference data.
- **Karaoke workspace:** optional YouTube embed, `.LRC` timestamp parsing, plain-text lyric import, lyric offset, practice timer, previous/next line controls, and a generated reference tone adjustable by ±2 semitones.
- **Live sur meter:** browser pitch estimate compared to the generated reference tone; displays on-pitch/flat/sharp cues and approximate cents difference.
- **Session recording:** captures microphone PCM and exports/replays a vocal-only WAV. This is not a mixed karaoke cover and does not separate vocals from backing tracks.
- **Privacy:** uploaded analysis is processed in memory by the API; external playback may bleed into a microphone, so headphones are recommended.

## API

- `GET /health` and `GET /healthz`: health checks.
- `POST /api/v1/analyze`: bounded WAV/FLAC analysis (10 MB maximum, 50-second server cap).
- OpenAPI documentation is available at `/docs` on the deployed API.

## Important limitations

This is a working prototype, not yet a production-grade music intelligence platform. A short recording cannot reliably establish a singer's complete vocal classification, breath control, jitter/shimmer, or celebrity similarity. The browser pitch tracker is a lightweight autocorrelation estimator. The reference-tone pitch meter compares against a synthesized note, not automatically against a song melody. The ±2 semitone control changes only the generated reference tone, not external video audio. Lyrics sync to the practice timer, not the YouTube player's current time. Publish compatibility percentages only when verified music metadata and a validated scoring method exist.

## Local development

Frontend: `npm install && npm start`

Backend: `pip install -r api/requirements.txt` then `uvicorn main:app --app-dir api --reload`

Run API tests from `api/` with `pytest -q`.

## Release gate

Before calling V2 release-ready, run the backend test suite, validate JavaScript and recording/export flows in a real browser, verify microphone permission/error states, and confirm frontend/backend deployment health. A syntax check alone is not an end-to-end test.
