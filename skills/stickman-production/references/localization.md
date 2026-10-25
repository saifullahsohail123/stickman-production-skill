# Dubs, scripts and fonts

Freeze the original revision. Adapt the jokes into natural language while keeping
their visual mechanism: a literal cooking instruction or self-moving prop needs
a translation that preserves the misunderstanding. Keep a separate language tag
and revision; changing language does not consume a new episode number.

Verify the installed app's actual engine/preset list, not only a model's upstream
language claims. Kokoro's Hindi presets include hf_alpha/hf_beta and hm_omega/
hm_psi; these are not verified child voices. Do not submit Urdu script to a Hindi
frontend and describe it as a native Urdu engine. Check the Urdu research note
when that language is requested.

Measure each new take without changing speech speed. Map old utterance start/end
to new start/end, retaining deliberate gaps where appropriate. Retimed action,
camera/foley contacts and expression arcs follow the mapped story clock. Mouth
closure and articulation follow the actual new waveform. Keep the direct speaker
visible for the entire newly measured line.

Use UTF-8 explicitly. Test complex shaping in the real renderer; the font simply
existing on disk does not prove that final captions render. Devanagari needs
proper conjunct/vowel shaping. Urdu needs right-to-left bidi layout and joined
Arabic-script glyphs. Do not reverse Unicode characters manually or reuse
left-to-right karaoke word positions for Urdu. Obtain glyph/run positions from
a bidi/shaping-aware layout engine, or use whole-phrase captions until verified.

Distinguish:

- Independent ASR: what the recognizer heard, preserved even when wrong.
- Known-text alignment: the supplied script timed to the audio; its echoed text
  is not an independent recognition/accuracy result.
- Phoneme alignment: phonetic boundaries, not merely word times or amplitudes.

A Hindi production test found multilingual ASR emitting Urdu script. Its raw
recognition was retained; known Devanagari text was aligned through cached
Whisper cross-attention/DTW instead. That workaround produced estimated lexical
timing; it did not certify pronunciation or exact lip sync. Keep implementation
and cache paths project-local rather than embedding them in this skill.
