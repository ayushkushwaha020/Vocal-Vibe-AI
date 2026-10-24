# VocalVibe AI — 15-Member Virtual Product Council

This is a role-based virtual review council: a structured set of specialist perspectives used to plan and evaluate the product. These are not 15 real people or autonomous agents working continuously in the background.

| # | Council seat | Specific responsibility | Quality gate |
|---|---|---|---|
| 1 | Product Director | Own product vision, MVP boundaries, roadmap, and prioritization | Every release maps to a user outcome |
| 2 | Technical Architect | Own system boundaries, API contracts, deployment topology, and technical decisions | Architecture is documented and maintainable |
| 3 | UX Research Lead | Validate beginner-singer needs and test the assessment journey | Core tasks are understandable without coaching |
| 4 | UI / Visual Design Lead | Maintain visual system, responsive layouts, motion, and accessibility | Keyboard, mobile, contrast, and reduced-motion checks |
| 5 | Frontend Engineering Lead | Own component structure, browser compatibility, and state management | No uncaught errors; supported browsers tested |
| 6 | Audio DSP Engineer | Own pitch estimation, filtering, signal quality, and latency | Algorithms evaluated against known test signals |
| 7 | Vocal Science Advisor | Review voice terminology, range interpretation, and safe coaching language | No unsupported diagnosis or misleading certainty |
| 8 | Recommendation / ML Engineer | Design vocal-to-song fit scoring and evaluation datasets | Recommendation scores are explainable and measurable |
| 9 | Catalog & Music Metadata Curator | Maintain song keys, comfortable ranges, tempo, mood, and licensing metadata | Every shipped track has rights and verified metadata |
| 10 | Karaoke / Synchronization Engineer | Own lyric timestamps, playback sync, transposition, and session controls | Sync drift and pitch-shift quality tested |
| 11 | Backend / API Engineer | Build FastAPI endpoints, validation, rate limits, and service health | Contract tests, bounded uploads, safe errors |
| 12 | Data & Privacy Officer | Minimize collection, document consent, retention, and deletion | Audio handling is disclosed and privacy-reviewed |
| 13 | Security Engineer | Threat-model uploads, dependencies, secrets, headers, and abuse cases | No secrets in source; dependency and input checks pass |
| 14 | QA / Accessibility Engineer | Own unit, integration, browser, keyboard, and assistive-technology testing | Release checklist passes before production |
| 15 | DevOps / SRE & Release Manager | Own CI, Render deployment, logs, health checks, rollback, and incidents | Health check succeeds and rollback path is known |

## Council operating protocol

1. Product Director writes the release goal and acceptance criteria.
2. Architect identifies dependencies and proposes implementation boundaries.
3. UX, vocal science, DSP, recommendation, catalog, and karaoke seats review domain behavior.
4. Engineering seats implement against reviewed interfaces.
5. QA and accessibility seat tests the candidate; security and privacy seats review risks.
6. DevOps deploys only after the release gate passes and confirms health.
7. Product Director records limitations, open risks, and next steps.

## Current MVP release gate

- [x] Responsive landing page and navigation
- [x] Browser microphone permission and waveform
- [x] Approximate pitch estimation and voice snapshot
- [x] Demo song cards and mood filters
- [x] Karaoke demo lyrics, controls, target pitch feedback, and semitone reference control
- [x] Node server and health endpoints
- [x] Render deployment configuration
- [ ] Automated unit/browser test suite
- [ ] Production FastAPI + Librosa analysis service
- [ ] Validated vocal-range classifier and recommendation evaluation
- [ ] Licensed backing tracks and synchronized licensed lyrics
- [ ] True tempo-preserving pitch shifting and saved mixed recordings
- [ ] Authentication, user data persistence, and account controls

## Non-negotiable product safeguards

- A brief sample cannot establish a user's complete vocal range or a reliable celebrity-vocal twin.
- Do not imply a celebrity similarity score is scientific unless it has a validated, consented dataset and disclosed evaluation method.
- Only use music and lyrics the project has rights to distribute or stream.
- Clearly tell users when audio is processed, transmitted, stored, or deleted.
- Keep vocal feedback supportive and avoid encouraging users to strain their voice.
