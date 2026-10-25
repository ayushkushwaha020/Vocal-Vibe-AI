#!/usr/bin/env python3
"""Dependency-free structural and JavaScript syntax checks for VocalVibe AI V2."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"

class InlineScriptParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.in_script = False
        self.external_script = False
        self.current = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            self.in_script = True
            self.external_script = any(k.lower() == "src" for k, _ in attrs)
            self.current = []

    def handle_data(self, data):
        if self.in_script and not self.external_script:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.in_script:
            if not self.external_script:
                self.scripts.append("".join(self.current))
            self.in_script = False
            self.external_script = False
            self.current = []

html = HTML_FILE.read_text(encoding="utf-8")
required = [
    'const $=id=>document.getElementById(id),API="https://vocal-vibe-audio-api.onrender.com"',
    'fetch(API+"/health"',
    'fetch(API+"/api/v1/analyze"',
    'pcmToWav(assessmentPcm,ctx.sampleRate)',
    'id="apiStatus"',
    'id="prompt"',
    'id="pitchRangeMetric"',
    'id="lrcUpload"',
    'id="targetToneBtn"',
    'id="recordBtn"',
    'id="exportBtn"',
    'data-practice=',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("Frontend integration checks failed; missing: " + ", ".join(missing))

# Compatibility must not be represented as a fabricated measured score.
if "94% Vocal Match" in html or 'id="heroFit">94%' in html:
    raise SystemExit("Frontend checks failed: fabricated personalized song-fit scores must not be shown.")

parser = InlineScriptParser()
parser.feed(html)
inline_scripts = [s for s in parser.scripts if s.strip()]
if not inline_scripts:
    raise SystemExit("No inline JavaScript found in index.html")

with tempfile.TemporaryDirectory() as temp_dir:
    for index, script in enumerate(inline_scripts, start=1):
        path = Path(temp_dir) / f"inline-{index}.js"
        path.write_text(script, encoding="utf-8")
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        if result.returncode:
            print(result.stdout, end="")
            print(result.stderr, end="")
            raise SystemExit(f"JavaScript syntax check failed for inline script {index}")

print(f"Frontend checks passed: {len(inline_scripts)} inline script(s) parse and V2 integration markers are present.")
