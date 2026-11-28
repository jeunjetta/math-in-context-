## Current FFT pilot review focus — 23 November 2026

**Draft, unadopted and not approved for publication.** Review one complete
80-second silent copy, not a teaser or the older live-lesson-CTA movie.
This summary reconciles the PR opening with the existing repository handoff;
it does not create a new candidate or adopt the source-only release route.

**Start with the [source-only playback worksheet](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/fft-latency/SOURCE_PLAYBACK_REVIEW.md).**
Use the already supplied `fft-source-only-review.mp4`: 732,406 bytes,
80 seconds, 1280×720, 24 fps, silent H.264. SHA-256:
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
These repository links do not supply the movie, grant access or imply a
public video destination. No installation is needed just to watch and comment.

Watch once at normal speed on the intended device. Then return one timestamped
observation and **keep / one specific fix / cannot assess**, using the worksheet.
Prioritize 49–61 s (four distinct questions) and 70–80 s (source-only ending).
The [descriptive text alternative](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/fft-latency/DESCRIPTIVE_TRANSCRIPT.md)
is available for this exact silent copy; equivalence and assistive-technology
review remain open. A review recommendation is not publication approval.

### What this copy teaches

Synthetic sequential workload: 20 ms Fourier computation + 80 ms other work
= 100 ms. Halving Fourier time gives 10 + 80 = 90 ms overall, about 1.11×,
not 2×; zero Fourier time would leave 80 ms, an ideal 1.25× ceiling.
Assume unchanged other work, unchanged accuracy and no added overhead.
Arithmetic complexity, numerical stability, whole-workload latency and
validated real-time readiness are separate questions. No new FFT, benchmark,
operator telemetry or operational grid capability is claimed.

The ending offers public Python/Marimo **source code**, not a live interactive
lesson. See the [exact-copy evidence and matching unpublished description](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/fft-latency/SOURCE_ONLY_REVIEW.md).
Frozen v7 and earlier comparison movies remain unchanged and unapproved.

### Evidence, supporting work and limits

The [dated status log](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/STATUS.md)
separates actual test/decode/sample checks from incomplete human review.
The [same-host fresh-environment rebuild](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/fft-latency/CLEAN_REBUILD.md)
reproduced this exact copy; that is not a clean-host or intended-device test.
No new render/decode/playback/audio-sync evidence is claimed by this PR-summary
update. The film has no speech; speech synchronization is not applicable,
not passed. Existing tool/font/build licensing caveats remain.

An [optional overhead prediction](https://github.com/jeunjetta/math-in-context-/blob/cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1/videos/fft-latency/OVERHEAD_CHECK.md)
supports learning after the video; retained studies and technical helpers are
not prerequisites to giving feedback on the one review focus. No learner
study or accessibility certification is claimed.

### Scope and remaining gates

Work stays under `videos/` on `codex/video-teaser-pacing`. This is still a
draft stacked on PR #3, which is stacked on PR #2; parent reconciliation
is needed before integration. PR #1 remains unmerged. No merge is requested.
No notebook/research conclusions changed; Open Notebook deployment is not assumed.

Open gates: complete intended-device playback, mathematical/editorial and
rights review, accessible text/playback review, audio choice and retiming if
needed, source-only adoption, parent reconciliation, authorized review route
and explicit exact-version publication approval. Decide the release design
before migrating canonical candidate/captions/package together. Nothing
uploaded to YouTube, posted to Substack/social, merged, deployed or purchased;
no account/sharing change or additional automation.

Summary source baseline: `cff39958e2e1a1e52bd9d24dbd732bc3c60b94e1`.
Earlier PR notes below are historical evidence for their own named copies,
not the current review request or proof that any release gate has cleared.
