# Local comparison review · prototype

12 November 2026. **Tested code increment; browser UI and tablet playback unverified.**
Source baseline: `60c09d44da94f88fe43915b9806211a6b3419620`.
This is a small reviewer aid, not a website deployment, third pacing variant,
new movie, learning-outcomes experiment or publication workflow.

## Use after browser checks

1. Save [review-player.html](review-player.html) as an HTML file. GitHub displays
   its source; this link is not a hosted player. Open the saved file in a browser.
2. Choose the exact 28- and/or 34-second MP4 review copies already supplied in
   the project conversation. They are not bundled or downloaded by the page.
3. The page hashes local file bytes, checks known candidate SHA-256 identities
   and media duration, then enables native video controls. A mismatch is blocked.
   Hashing/file-open support varies by browser/context; do not bypass a failure.
4. Watch each complete silent cut at normal speed. Use the 22-second shortcut
   only afterwards. Pause at a problem, write a short public-project note and
   add its timestamp. Native currentTime is not frame-accurate certification.
5. Download the draft feedback JSON before closing the page. Inspect it before
   attaching it to PR #4 or sharing it. There is no automatic posting or storage.

No account, server, API key, external assets, network fetches, localStorage,
telemetry, autoplay or paid services. A restrictive CSP blocks connections.
File bytes and notes stay in memory; the page cannot recover unsaved notes.
Export includes candidate identities, loaded candidate IDs, issue type/text,
timestamp, provisional preference and explicitly self-reported playback checks.
No local file paths or reviewer name are collected. Never enter operator data,
private notes or credentials. `publication_approved` is always false.

## One useful comparison

Can the viewer explain why 20+80=100 ms becomes 10+80=90 ms rather than
twice the whole-system speed? Can they distinguish complexity, numerical
stability, latency and grid readiness without rereading the closing card?
Mark unreadable secondary text at normal size; do not infer comprehension from
token counts or a preference click. This is a synthetic sequential model with
same accuracy, no added overhead and unchanged other work. No operational
benchmark or real grid telemetry. Concept links and educational sources stay in
[the lesson/storyboard](TEASER.md); the 80-second pilot remains first milestone.

## Implementation and actual verification

`fft_review_player.py` builds the single offline HTML from a separate template
and frozen candidate JSON files. There are no new runtime dependencies or
lockfile changes. Original HTML/CSS/JavaScript only; system browser fonts.
No copied creator footage/assets or fabricated voice. It neither changes nor
re-encodes any video, caption, lesson or research conclusion.

From videos/:

```sh
python3 fft_review_player.py --check
python3 -m unittest test_fft_review_player -v
node test_review_player_logic.cjs
```

Three Python regressions cover generated file/candidate identity, static
network/approval guards, safe text insertion and controls. Built-in-only Node
24.22.1 DOM-shim tests cover unknown/oversize rejection, fixture switch/seek,
literal-text notes, exact-identity draft export, mismatched-duration blocking
and object-URL cleanup. The matching-file fixture is NOT a real-browser hash
acceptance test. Full Python-suite result is recorded in [STATUS.md](../STATUS.md).

Attempted real browser validation stopped: Playwright's bundled browser is
absent; the installed Chromium could not launch because its process-singleton
socket was denied by the environment. No permission workaround, download or
account change was attempted. Consequently NO screenshot/layout/clipping,
native-video decoding, successful matching-file selection, keyboard/screen-reader
or real-device review is claimed for this page. DOM shims cannot verify those.
Do not treat it as a finished or accessibility-certified tablet interface.

API references checked 12 November: [local SHA-256](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest),
[object URLs](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static),
[native media time](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime).
These document the API mechanisms, not browser/device compatibility approval
for this particular implementation.

Next: run a permitted real-browser smoke test at phone/tablet widths before
relying on this tool, then collect complete comparison playback feedback.
If browser/file support is unsuitable, use the native MP4 player and manually
record candidate and timestamp; do not let this optional aid block video review.
Human/math/editorial/rights review, audio/destination decisions, parent-branch
reconciliation and exact-version publishing approval remain open. Nothing
uploaded to YouTube/Substack/socials or merged; no Open Notebook deployment assumed.
