# Optional human narration · recording brief

14 November 2026. **Unrecorded, unapproved rehearsal copy**, not a decision to
add audio. The current 80-second silent v7 movie and its canonical captions
remain unchanged. No voice was recorded, synthesized, cloned or impersonated.
No music or paid service is selected. This is a concrete preparation option
for the open silent-versus-human-narration decision, not another render.

Read the [complete 154-word recording script](NARRATION_SCRIPT.md).
Its editable content and provisional windows are in [narration.json](narration.json),
separate from rendering. The generator checks those windows against the
existing lesson's 19 cue windows, frozen lesson/movie identity, unrecorded
status and an explicit mechanical rate budget. It does not estimate actual
speech duration. Source baseline: `fa1d45046df8a462f3b92c9b4f36b8ea5e2fca4a`.
Target reference movie SHA256:
`1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.

## Directing the read

- Address one technically curious person; explain, don't announce a breakthrough.
- Give the prediction question space. Its planned one-second pause is only a
  rehearsal allocation, not evidence that every viewer can answer in that time.
- Read units as “milliseconds”; read the rounded quotient as “about one point
  one one,” not a two-times total gain. Say the limiting factor as “one point
  two five.” Fourier has its ordinary mathematical pronunciation; no imitation
  of any creator's voice, delivery, music or distinctive assets is requested.
- Emphasize **only** the Fourier step, **fixed** other work, and the **whole**
  job. Don't turn the result into a percentage claim the script hasn't stated.
- At 49–61 s, distinguish four questions with a small vocal reset: operation
  counts, computation errors, elapsed time, and validated system deadlines.
- The last sentence leaves a planned second of silence. Do not force the
  recording into these windows by speeding up the voice or chopping breaths.

The count is 154 words using the documented tokenizer: apostrophes stay in
words; hyphens split spoken words. Across 80 seconds that is 115.50 words/minute;
after subtracting two seconds of planned pauses it is about 118.46 words/minute.
The largest cue-level rate is 140 words/minute. A 160-word/minute mechanical
ceiling is our draft planning budget, **not** a validated accessibility or
speaking-speed standard. Word lengths, emphasis and breaths vary; only an
actual authorized read can establish timing and comprehension.

## Content and visual alignment audit

The original synthetic accounting remains 20+80=100 ms, then 10+80=90 ms;
old/new=100/90≈1.11, with a limiting factor of 100/80=1.25. All four
assumptions are spoken: sequential work at 8 s; same accuracy and no added
overhead at 22 s; other work fixed at 26 s. These are assumptions, not
measured implementation guarantees. Complexity/stability/latency/readiness
remain distinct, and the 61–70 s lines disclaim both a new algorithm benchmark
and real-time grid capability. Concept placement is Fourier methods → algorithms
→ component costs → total latency; readiness requires separate validation.

The producer compared planned numbers/focus windows with the current lesson
and storyboard. The 90 ms spoken result is in the settled-bar interval, and
the 1.25 limiting factor starts with the existing 44.5 s quotient cue, not
beside the moving ceiling bar. Category speech follows the existing four
highlight windows in order. No fresh frame/render/clipping/equation inspection
was performed: pixels have not changed and earlier visual findings still apply.

This is NOT ready to lay over the silent captions: at 22–26 s, for example,
the proposed speech states accuracy/overhead while the current reading caption
describes unchanged work. Rebuild speech-aligned captions from the actual
recording and review concurrent reading load, rather than certifying sync from
equal target windows. Reading captions are not automatically transcripts.

The 70–80 s rehearsal ending is deliberately destination-neutral. It does
NOT endorse either a live Marimo lesson or the proposed source-only route.
The frozen visual end card still contains the unverified live-lesson CTA;
this script does not remove that blocker or adopt the source-only proposal.
Any adopted narrated candidate needs a controlled ending/content/caption/
review/package update as a whole, with its own new exact-version identity.

## Sources, provenance and reproduction

This is original Math in Context spoken copy derived from the existing
synthetic lesson, not podcast quotations or a copied creator script.
[FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html),
rechecked 14 November, support keeping numerical error distinct from runtime;
they do not validate the invented timing numbers. No research-agent conclusions,
operator data, private notebooks, clips or unverified discussion claims enter it.
Open Notebook remains source-management context, not a claimed deployed service.

From `videos/`:

```sh
uv run --locked python narration_script.py --check
uv run --locked python -m unittest test_narration_script -v
# After deliberately editing narration.json, regenerate only its derived script:
uv run --locked python narration_script.py
```

No dependency or lockfile change. Existing renderer retained; no new audio
engine or licensing choice is needed for text-only preparation. Standard-library
[JSON documentation](https://docs.python.org/3/library/json.html) and
[Python licence](https://docs.python.org/3/license.html) checked 14 November;
tested Python is 3.12.14, not the latest documentation version. No binaries
are bundled and this does not clear commercial codec/asset/recording rights.
The four focused tests cover window/pause/rate accounting, wrong identity/
timing/approval, invalid pauses/over-budget text, generated-script identity
and required assumption/disclaimer wording. Full results: [STATUS.md](../STATUS.md).

## Next action and exact blockers

Editorially review this script and choose silent or authorized human narration.
If narration is chosen, obtain a consented human read using an already available
recording method, listen at natural speed and log actual cue/breath boundaries.
No specific narrator, voice rights or recorded file is currently supplied.
Then make a separate controlled audio candidate, transcribe/align captions to
what was actually said, and inspect full playback, numeric/category cut timing,
audio intelligibility and smaller-device reading load. No synthetic placeholder
voice, paid purchase, automatic upload or blanket approval.

Existing ending/destination choice, live-lesson gate unless explicitly changed,
math/editorial/rights/device review, parent-PR reconciliation and exact-version
publication approval remain open. No browser restriction was retried or bypassed.
No new render, audio, notebook, research, hosting, account setting, publication,
merge or automation change.
