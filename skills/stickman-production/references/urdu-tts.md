# Urdu TTS research — checked 2026-10-25

These are candidates, not installed/tested adapters. Keep true Urdu script,
pronunciation and RTL captions distinct from Hindi transliteration.

| Candidate | Practical status | Licence/deployment note |
|---|---|---|
| [OmniVoice Urdu fine-tune](https://huggingface.co/mlwithabdullah/omnivoice-urdu-12000) | Open local candidate to audition; based on [OmniVoice](https://github.com/k2-fsa/OmniVoice). This package has not measured its pronunciation, latency or VRAM. | Both upstream code and the fine-tune card identify Apache-2.0. Model-card evaluation numbers are author-reported, not our benchmark. |
| [Azure Speech Urdu](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts) | Official Pakistan Urdu voices `ur-PK-UzmaNeural` (female) and `ur-PK-AsadNeural` (male). Useful cloud voices to audition. | Hosted proprietary service, not an offline open-source model. Requires its own account/service adapter. |
| [Meta MMS Urdu](https://huggingface.co/facebook/mms-tts-urd-script_arabic) | Dedicated local Urdu-script checkpoint; a small experimental baseline. Not tested in this package. | Model card says CC-BY-NC-4.0; do not choose it as an unrestricted monetized-production default. |

The tested Kokoro voice list has Hindi, not a dedicated Urdu preset. Chatterbox's
[official multilingual list](https://github.com/resemble-ai/chatterbox#supported-languages)
also does not list Urdu. Do not treat Arabic or Hindi support as proof of Urdu.
The installed Voicebox generation schema used in the originating workflow did not
accept `ur`; a new provider needs an explicit adapter rather than a silent switch.

If choosing a local candidate, test a small original Urdu passage before changing
the episode pipeline. Judge Urdu-specific consonants, names, numbers, English
code-switching, pace and expressive consistency across the intended cast. Keep
that test and its actual model/version/settings as a regression fixture. No model
download, paid request, voice cloning or Urdu generation was performed merely
to write this research note.
