# One-copy playback review sheet

18 November 2026 · second video increment. Baseline PR #4 commit
`7cb4f60ef0ae3ec447a8d86e4ac2e149d54205f7`.
This is a focused review handoff for the existing larger-caption movie,
not another edit, replacement for frozen v7 or release approval.

## Use the right copy

File: **fft-caption-layout-review.mp4** · 80 s · silent · 1280×720 · 24 fps.
SHA-256: `d0b22d6291d0b8d9205bd5e47d7d27cbd8892f63df4a1957a7d3d5decc605142`.
It has 34px captions and a balanced two-line 70–75 s ending; it is NOT
the frozen 26px `fft-latency-draft.mp4` or either short vertical teaser.
The private copy was supplied separately. No public review URL or sharing
permission is implied. [Technical render evidence](CAPTION_REVIEW_RENDER.md).

Use an existing trusted local video player. Watch once at normal speed,
without seeking, at the viewing size you normally use. Then replay only
the marked trouble spots. If a player cannot display the movie at a usable
size, record a player limitation rather than rating the typography.
This sheet needs no new software, account, local server or development tools.

## What to look for

| Window | Review question | Mark if a problem occurs |
|---|---|---|
| 0–8 s | Is there time to predict before the answer? | Hook rushed / unclear |
| 8–18 s | Can you read 20 ms + 80 ms and the sequential/same-accuracy/no-added-overhead assumptions? | Secondary text too small |
| 18–30 s | Does only the Fourier block shrink, then settle at 10 + 80 = 90 ms? | Motion/label confusion |
| 30–40 s | Can you follow old time / new time = about 1.11×, not 2×? | Equation needs another read |
| 40–49 s | Is the 80 ms remainder and 1.25× ideal ceiling clear? | Ceiling unclear |
| 49–61 s | Can you distinguish complexity, stability, latency and readiness at the three-second changes? | Specific card/caption too fast |
| 61–70 s | Is this explicitly a synthetic example, not real-grid capability evidence? | Scope message missed |
| 70–75 s | Does the two-line caption read naturally across the break after “and”? | Awkward break / source text too small |
| 75–80 s | Can you read the final connection without missing the ending? | Last caption cut short |

Without replaying, explain the 100→90 ms result in your own words and
name one thing the arithmetic does NOT establish. This is an editorial
prompt, not a scored learning experiment or proof of comprehension.

Public-safe feedback format (keep private/operator data out):

> Exact filename/hash: …  / Entire 0–80 s watched at normal speed: yes/no
> Viewing width approximately: … px or unknown / fullscreen: yes/no
> Timestamp or window: … / issue: … / observed effect: …
> Proposed next action: keep / one specific fix / cannot assess

Do not label speech synchronization passed: this movie has no audio.
Do not infer a live lesson from the Marimo CTA: its destination remains
unverified. No response here approves layout adoption or publication.

## Native smoke test actually completed

The exact local file hash was rechecked before and after the test. Imported
it into installed Kdenlive 24.12.3 / MLT 7.30.0, matched the temporary
project to HD 720p 24 fps, and observed decoded opening, baseline, changing
bar and formula content as the playhead advanced into the 30–40 s scene.
This verifies native import and visible decoding of those portions only.

The 1364×1024 desktop's clip monitor showed a 320×180 image. Its expanded
monitor window remained 320×334, including controls; a normal window-size
attempt did not enlarge it. No full-size review, complete 80-second pass,
normal-speed timing measurement, smooth-motion/stutter assessment, Android
test or accessibility approval is claimed. This is an environment/player
limitation, not evidence that the encoded movie clips at larger sizes.
The temporary unsaved project was discarded; source MP4 unchanged. No
project file, screenshot, installation, renderer change or re-encode added.

Handoff checks: movie and all 11 source hashes match the render manifest;
all nine table windows match canonical scene/caption boundaries; local link
resolves. Three existing focused renderer tests pass in 0.215 s; review HTML,
caption-pacing and narration source-copy checks and whitespace pass. No source
code changed, so the previous 135-test full-suite result is not a fresh run.

The official [Add Clip documentation](https://docs.kdenlive.org/en/project_and_asset_management/project_bin/clips.html)
was checked on 18 November 2026; current docs describe a newer release
than the installed editor. Actual UI observations above are the evidence.
The existing renderer, pinned dependencies, fonts and licence caveats stay
unchanged; using an installed editor does not clear codec/distribution rights.

Next: collect one complete intended-device pass using this sheet, then make
one specific production-layout decision. Remaining gates: human math/editorial/
rights review, accessible device playback, silent-versus-authorized-human-audio
choice and retiming if needed, verified CTA or explicitly adopted fallback,
authorized review route, parent reconciliation and exact-version publication
approval. No new variants should be generated absent an observed defect.
