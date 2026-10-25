# Acting and synchronization

## Separate the clocks

Story/action time samples the physical scene. Performance time samples the actual
output waveform, word alignment and speaking role. A camera cut can lead a spoken
thought while articulation continues on its original performance clock. A dub
requires a new map between these clocks. `core.TimeMap` validates an invertible,
strictly increasing map and refuses frame rounding that collapses a shot.

## A small usable face rig

Store eyes/brows, pupils/gaze and mouth selections separately. A face expression
group must not contain a permanent drawn mouth underneath the speaking mouth.
Useful articulation states include rest/closed, open vowel, wide vowel, rounded,
lip/teeth contact and tongue; useful emotional states include smile, frown, smirk
and gasp. Select one mouth at a time, including during pauses.

For approximate word-guided acting, choose shapes from language-appropriate
phonetic hints and close the mouth during low-energy waveform windows. Do not
label spelling-derived shapes or amplitude gates as phoneme alignment. A genuine
phoneme aligner or authored phonetic timing is a different capability.

Keep the actual direct speaker's head visible throughout a line, unless the shot
intentionally establishes offscreen speech. Do not animate a listener's mouth to
the narrator. Let listeners blink, glance toward the speaker and react instead.

## Expression arcs

Author an emotion transition that matches the sentence and event: confidence →
realization → embarrassment, or anticipation → shock → recovery. Add blinks,
small gaze shifts and head accents without random expression flashes. Hold an
important reaction long enough to read. A freeze-frame is genuinely held artwork;
articulation and idle blink loops must not continue under a claimed freeze.

An attached cup/flour bag/tool should remain a child of its carrying forearm or
use a computed grip constraint. Counter-rotate about the grip when it must remain
upright. Feet use contact constraints rather than continuous whole-body bobbing.
Establish an environment with functional props, scale and counter/foreground
occlusion, not only a different wall color.

## Review evidence

Watch at normal speed with audio. Inspect beginning/middle/end of each direct
speaking passage. Compare actual rendered mouth crops, not merely intended rig
states. A correct mux offset proves placement of the audio, not convincing lips.
Track which kinds of evidence exist: waveform checks, decoded pictures, moving
playback, direct listening and user approval are distinct.
