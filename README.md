# VocalVibe AI 🎙️

AI-inspired vocal discovery, browser-based voice diagnostics, personalized song-fit recommendations, and interactive karaoke practice.

## Current release

This repository contains a deployable, responsive Milestone 1 prototype:
- Microphone permission and live waveform visualization
- Browser-side live pitch preview and a guided 10-second singing assessment
- Vocal Aura profile with median pitch estimate, observed pitch percentiles, acoustic texture cue, and average signal energy
- Demo song discovery cards with mood filters (personalized compatibility scores are not shown until real song metadata is available)
- Karaoke studio with timed demo lyrics, pitch feedback, recording controls, semitone controls, and YouTube search / pasted-video embedding
- Responsive accessibility-minded interface and reduced-motion support
- Node HTTP server with `/health` and `/healthz` health endpoints

**Honest limitations:** vocal type and celebrity-twin percentages are entertainment-oriented estimates, not validated clinical or professional classifications. This MVP uses original demo song/lyric data and a synthesized practice tone. The starter-song button redirects to YouTube search; users can paste a video URL to embed it when permitted. YouTube search results are not fetched into the app, and no commercial backing tracks or full copyrighted lyrics are bundled. Real song synchronization requires licensed audio and lyric assets. Robust pitch-shifting, server-side Librosa analysis, authentication, persistent user data, and Gemini integration are later milestones.

## Run locally

Requires Node.js 20+.

```bash
npm start
```

Open http://localhost:3000. Use HTTPS or localhost for microphone access.

## Deploy on Render

Create a **Node** Web Service connected to this repository:
- Build command: `npm install`
- Start command: `npm start`
- Health check path: `/health`
- Node version: 20+

The included `render.yaml` describes the service for Blueprint-based deployments.

## Privacy and safety

Live microphone audio is processed in the browser for the pitch preview. When the user selects Analyze, the recorded WAV sample is uploaded to the FastAPI audio service for feature extraction. The API processes it in memory and does not intentionally persist the uploaded file. Use headphones during karaoke playback to reduce music leaking into the microphone. The browser may ask for microphone permission; stop recording when finished. Do not treat automated feedback as professional vocal coaching or medical advice.

## Architecture roadmap

1. **MVP (included):** browser microphone, pitch visualization, recommendations, karaoke interaction.
2. **Analysis API:** FastAPI + Librosa/pYIN, request limits, validation, privacy-conscious upload handling, tests and observability.
3. **Personalization:** licensed catalog, verified song key/range metadata, account controls and consent-based persistence.
4. **Advanced studio:** licensed stems, time-stretched pitch shifting, synced licensed LRC, mix recording and export.
