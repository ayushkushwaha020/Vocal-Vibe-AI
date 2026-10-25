# VocalVibe AI — Version 2

Version 2 is developed on the separate `version-2` branch. The existing `main` branch remains the Version 1 baseline and is not modified by V2-only commits.

## V2 implemented in this branch

- Keeps the existing responsive VocalVibe AI interface, microphone flow, karaoke prototype, and note-segment results.
- Adds backend spectral rolloff and 13 averaged MFCC coefficients as additional acoustic descriptors.
- Adds heuristic recording-quality checks for low signal level, low voiced-frame ratio, short samples, and possible clipping.
- Displays recording-quality feedback and acoustic diagnostics in the results interface.
- Extends the synthetic-tone API test to check the new response fields.

## Important limitations

- The quality label is a lightweight heuristic, not a calibrated studio-quality rating.
- MFCCs and spectral measurements do not independently establish voice type, vocal health, breath control, or celebrity similarity.
- Detected notes are observed pitches; note correctness requires a target scale or melody.
- Song compatibility scores remain hidden until verified song key/range metadata and a validated scoring method are available.
- Karaoke transposition, lyric synchronization, vocal separation, recording mix/export, Gemini coaching, authentication, and persistent user profiles are not yet complete.
- Browser end-to-end testing and deployment validation are required before release.

## V2 development roadmap

1. **Analyzer reliability:** test synthetic tones across frequencies, note transitions, noisy audio, clipping, and quiet recordings.
2. **Targeted note accuracy:** add a selectable reference scale and compare observed pitches with expected notes.
3. **Vocal profile:** validate pitch range and acoustic descriptions; avoid definitive vocal-type claims from short samples.
4. **Song matching:** add verified song metadata and explainable fit calculations before showing compatibility percentages.
5. **Karaoke:** validate real pitch shifting, timestamped lyrics, live target-note feedback, and recording replay.
6. **AI coaching:** add a server-side AI provider integration with secret management, consent, rate limits, and grounded feedback.
7. **Release gate:** run API tests, frontend syntax checks, browser workflow tests, accessibility checks, and deployment health checks.

## Local development

Frontend: `npm install && npm start`

Backend: `pip install -r api/requirements.txt` then `uvicorn main:app --app-dir api --reload`

Run API tests from the `api` directory with `pytest -q`.

V2 should be deployed from this branch only after its tests pass and the remaining release criteria are reviewed.
