# VocalVibe AI 🎙️

AI-inspired vocal discovery, browser-based voice diagnostics, personalized song-fit recommendations, and interactive karaoke practice.

## Current release

This repository contains a deployable, responsive Milestone 1 prototype:
- Microphone permission and live waveform visualization
- Browser-side pitch estimation and a guided 30-second assessment
- Vocal Aura profile with estimated pitch range and voice texture cues
- Song discovery cards with fit explanations and mood filters
- Karaoke studio with timed demo lyrics, pitch feedback, recording controls, and semitone controls
- Responsive accessibility-minded interface and reduced-motion support
- Node HTTP server with `/health` and `/healthz` health endpoints

**Honest limitations:** vocal type and celebrity-twin percentages are entertainment-oriented estimates, not validated clinical or professional classifications. This MVP uses demo song/lyric data and a synthesized practice tone; it does not ship copyrighted backing tracks or full commercial lyrics. Real song synchronization requires licensed audio and lyric assets. Robust pitch-shifting, server-side Librosa analysis, authentication, persistent user data, and Gemini integration are later milestones.

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

Microphone input is processed in the browser for the prototype and is not uploaded by this app. The browser may ask for microphone permission. Stop recording when finished. Do not treat automated feedback as professional vocal coaching or medical advice.

## Architecture roadmap

1. **MVP (included):** browser microphone, pitch visualization, recommendations, karaoke interaction.
2. **Analysis API:** FastAPI + Librosa/pYIN, request limits, validation, privacy-conscious upload handling, tests and observability.
3. **Personalization:** licensed catalog, verified song key/range metadata, account controls and consent-based persistence.
4. **Advanced studio:** licensed stems, time-stretched pitch shifting, synced licensed LRC, mix recording and export.
