# FFT/latency · live-lesson handoff

**BLOCKED FOR PUBLIC RELEASE · checked 31 October 2026, 10:02 Sydney.**
This is a read-only readiness audit, not permission to enable Pages, merge,
deploy or publish. No live lesson URL has been verified.

## Evidence at this check

| Item | Observed state | What it does—and does not—establish |
|---|---|---|
| Main | `c9fdf98729379dd404afce99daad1a6aa042156e`, original template | The FFT lesson is not in main. |
| [Pilot PR #1](https://github.com/jeunjetta/math-in-context-/pull/1) | Open, head `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc` | Review branch contains the lesson; it is not a public interactive URL. |
| [Pilot tests](https://github.com/jeunjetta/math-in-context-/actions/runs/40734730180) | Successful at that pilot head | Passing content checks does not mean Pages deployment or tablet review passed. |
| [Pages run](https://github.com/jeunjetta/math-in-context-/actions/runs/40723050432) | Failed on 28 October at main's template commit | Build/export and artifact upload succeeded; the deploy job failed. This run did not contain the FFT pilot. |
| Deploy error | HTTP 404 creating the Pages deployment; annotation says to check that Pages is enabled | Concrete deployment blocker, not an FFT arithmetic/render failure. Current authenticated Pages settings were not inspected or changed. |
| Public Pages metadata | Unauthenticated `GET /repos/jeunjetta/math-in-context-/pages` returned 404 | No site URL obtained. A public API 404 alone does not prove all settings or authorization details. |
| Actions history | Five available runs: four successful content-test runs, one failed Pages run | No successful Pages deployment found in the returned history. |
| Video PR #2 | Draft, head `c15591adcaa07b97467afbec10e862e9bb76fc21` before this audit | Silent v4 exists; no human approval or new render inferred. |

The deploy annotation explicitly reports a failed deployment with status 404
and points to Pages settings. It is an error message, not a verified root-cause
diagnosis of account configuration. The Node.js deprecation warning is not
identified as the cause of the 404. No paid review service is required here.

## Keep the draft call-to-action honest

The current end card (70–80 s) says
`Try: apps/fft_and_latency.py · pilot PR #1` and refers readers to
`videos/README.md`. Its first caption invites the Marimo experiment. This is
a **source-path review pointer**, not a clickable hosted lesson address.
It remains acceptable only as an explicitly labelled draft; do not upload
this exact CTA as though the experiment were publicly usable.

The draft description in [REVIEW.md](REVIEW.md) must retain
`ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION` until verification is complete.
Do not construct a guessed `github.io` URL, use an Actions artifact as the
permanent learner link, or replace it with Open Notebook (not known deployed).
The interactive lesson is a separate release dependency from video rendering.

## Approval-dependent handoff, in order

1. Review PR #1 and obtain explicit merge authorization. This audit does not
   merge it or request that another agent do so automatically.
2. An authorized owner checks [Pages settings](https://github.com/jeunjetta/math-in-context-/settings/pages)
   and confirms the intended GitHub Actions publishing source. Enabling or
   changing it requires approval; do not rerun deployment as part of this audit.
3. After authorized deployment, obtain the **actual deployment output URL**,
   run link and deployed source commit. Follow the index's FFT lesson link;
   the template root alone is not proof that the lesson exists.
4. On the real tablet, load from a fresh browser session, wait for WebAssembly
   startup, and test defaults (100 ms, 20%, 2× → 90 ms and 1.11×), slider
   reactivity, quiz feedback, navigation and source links. Record any browser
   error and initial-load delay separately from toy pipeline timings.
5. Record the evidence below, then replace the description placeholder and
   end-card pointer with the **same verified lesson destination**. Use a short
   readable display URL if needed; a QR code may supplement, not replace it.
6. Rerender and inspect the encoded end card, readability, captions and full
   playback. Obtain mathematical/editorial, rights and exact-version
   publication approval. Successful deployment alone clears none of those.

GitHub's [official custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
was checked on 31 October 2026. It distinguishes enabling a publishing source,
building/uploading an artifact and deploying it. No infrastructure, workflow
version or repository setting has been changed by this video audit.

## Evidence to fill in later — all currently pending

- [ ] Authorized merge / publishing-source decision, reviewer and date:
- [ ] Successful deployment run and exact deployed commit:
- [ ] Actual lesson URL (followed from deployment, not inferred):
- [ ] Tablet/browser, date, default values, sliders and quiz verified:
- [ ] Description and encoded end card match that destination:
- [ ] Exact final MP4 hash and human release approval:

Do not tick these from automated layout tests. Recheck current repository state
before acting; this page is dated evidence, not a permanent service-status claim.
