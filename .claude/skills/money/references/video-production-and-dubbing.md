# Turning raw trade footage into tutorials, and dubbing them: tools and prices

Built 2026-09-20 from main-pc, from the vendors' own pricing, documentation and
terms pages. Every quotation was seen in the page text; the `dub-*` claims in
`claims.json` re-check the ones a script can reach. Prices change often - the
date is part of every figure. Facts only: what each tool costs, what it can do
and what its terms allow. The setting: a person films real installs on a phone;
an AI agent on a Windows PC edits, captions and dubs; the budget starts near
zero.

## 1. Dubbing

| Item | Value | Label | Source |
|---|---|---|---|
| YouTube automatic dubbing | free and "This feature is enabled by default for eligible creators."; from English into "Arabic, Bengali, Dutch, French*, German*, Hebrew, Hindi*, Indonesian*, Italian*, Japanese, Korean, Malayalam, Polish, Portuguese*, Punjabi, Russian, Spanish*, Tamil, Telugu, Ukrainian"; not for videos where "The video exceeds 120 minutes."; such tracks "are marked as “auto-dubbed” in the video description." | [V 2026-09-20] | support.google.com/youtube/answer/15569972 |
| YouTube, uploading one's own dubbed track | "Multi-language audio is currently available to creators with access to Advanced features."; "If an automatic dub already exists for a language, you must delete it before uploading your own version."; Advanced features come by "Completing phone verification Building sufficient channel history or verifying identity using a valid ID or video" | [V 2026-09-20] | support.google.com/youtube/answer/13338784; /answer/9891124 |
| YouTube disclosure rule | "we require creators to disclose when they use AI to meaningfully alter or generate photorealistic content"; listed among what needs no disclosure: "Cloning one’s own voice to create voice overs or dubs" | [V 2026-09-20] | support.google.com/youtube/answer/14328491 |
| ElevenLabs, by API | "Dubbing v1 Dubbing $0.33 Price per minute" with "29 languages supported MP3, MP4, WAV, and MOV formats"; "Dubbing v2 Dubbing $2.20 Price per minute" with "92 languages supported"; "Is Dubbing v2 available via API? Yes. Creating and downloading dubs is available on all plans."; the speaker's voice is kept by default ("disable_voice_cloning boolean Optional Defaults to false"); no lip-sync is mentioned anywhere in its dubbing documentation | [V 2026-09-20] | elevenlabs.io/pricing/api; elevenlabs.io/docs/capabilities/dubbing; /docs/api-reference/dubbing/create |
| ElevenLabs limits and rights | "Upload limits: Up to 1 GB and 180 minutes in the app, or 3 GB per source file via the API"; "Free-tier dubs are watermarked automatically; paid-tier dubs are not."; free use is "for non-commercial purposes" only, paid plans "may use the Services for commercial purposes"; the first paid plan is 6 dollars a month | [V 2026-09-20]; the 6-dollar figure seen by the researcher only [S] | elevenlabs.io/docs/capabilities/dubbing; elevenlabs.io/terms-of-use |
| HeyGen Video Translate, by API | pay-as-you-go without a subscription ("you can purchase API credits without having Creator, Pro, or Business plans"): "Speed — Audio Only (no lip sync dubbing) $0.57", lip-sync 0.81 and precision 1.50 dollars a minute (same table) | [V 2026-09-20] | help.heygen.com, article on API pricing |
| HeyGen in the app | "Creator $29 / mo"; "Creator: 600 credits → 100 min VT Pro: 1000 credits → 166 min VT Business: 1500 credits → 250 min VT"; "Audio Only = 4 credits/minute"; "Translate videos into 175+ languages with realistic AI voices, lip sync, and subtitles."; the free plan's output "may not be sold, sublicensed, redistributed, monetized, or used in connection with commercial activities" | [V 2026-09-20] | heygen.com/pricing; help.heygen.com; heygen.com/terms (updated 2026-07-23) |
| Rask AI | "$ 60 /mo billed monthly 25 minutes per month included"; its API is "Available to customers on Business and Enterprise Plans" | [V 2026-09-20] | rask.ai/pricing; rask.ai/api |
| Descript | dubbing "Available in 30 languages", charged in AI credits with no minutes figure given; "Hobbyist $ 16 $ 24 per person / month" | [V 2026-09-20] | descript.com/pricing |
| Consent to clone a voice | ElevenLabs forbids to "intentionally replicate the voice of another person: a) without consent or legal right"; HeyGen "verifies that you own the original voice before training a voice clone, requires written consent for any third-party voice" | [V 2026-09-20] | elevenlabs.io/use-policy; heygen.com/tool/ai-voice-cloning |

## 2. Editing, sound and captions

| Item | Value | Label | Source |
|---|---|---|---|
| FFmpeg (the agent's command-line editor) | "FFmpeg is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later." | [V 2026-09-20] | ffmpeg.org/legal.html |
| Whisper for transcripts and subtitles | run locally: "Whisper's code and model weights are released under the MIT License."; by API: "gpt-4o-mini-transcribe Transcription $1.25 $5.00 $0.003 / minute"; "The Transcriptions API accepts files up to 25 MB." | [V 2026-09-20] | github.com/openai/whisper; platform.openai.com/docs/pricing |
| Descript for editing by transcript | "The Descript API lets you programmatically create projects, import media, and edit your projects — all without opening the app."; a command-line client ("npm install -g @descript/platform-cli@latest"); but "Currently, the API does not support uploading a file directly." | [V 2026-09-20] | docs.descriptapi.com |
| DaVinci Resolve | free download, or "Davinci Resolve Studio Buy Online Now $295"; scripting is listed as a Studio feature: "DaVinci Resolve Studio features support for both Python and LUA scripting, along with developer APIs". What the free version allows by script is not stated on Blackmagic's site [G] | [V 2026-09-20]; free-version scripting [G] | blackmagicdesign.com/products/davinciresolve |
| CapCut | its terms forbid to "use automated scripts or other technologies to collect information from or otherwise interact with the Services"; its AI translator "is available in specific regions" | [V 2026-09-20] | capcut.com/clause/terms-of-service; capcut.com/tools/ai-video-translator |
| Auphonic (levelling, noise) | "Auphonic is free for 2 hours of processed audio per month."; "Productions of free users come with a jingle."; "The Auphonic REST API allows you to integrate our complete services and algorithms into your scripts, external workflows and third-party applications." | [V 2026-09-20] | auphonic.com/pricing; auphonic.com/help/api |
| Adobe Enhance Speech, free tier | "30 minutes max duration (up to 500 MB), 1 hour max per day"; "Enhance audio only, no video support" | [V 2026-09-20] | podcast.adobe.com/en/plans |
| YouTube automatic captions | offered in a long list of languages, English among them | [V 2026-09-20] | support.google.com/youtube/answer/6373554 |

## 3. Which languages, by reach

| Item | Value | Label | Source |
|---|---|---|---|
| Share of websites by content language (a proxy for reach on the web, not a count of people) | "English 49.5% Spanish 6.0% German 5.9% Japanese 4.9% French 4.5% Portuguese 4.1% Russian 3.4% Italian 2.8% Dutch, Flemish 2.1% Polish 1.8% Turkish 1.6% Chinese 1.3%" | [V 2026-09-20] | w3techs.com/technologies/overview/content_language |
| Speakers | "When factoring in second-, third-, and higher language speakers, English is the largest language in the world."; the speaker counts themselves are in charts and were not readable [G] | [V 2026-09-20]; counts [G] | ethnologue.com/insights/most-spoken-language/ |

## 4. What the facts allow [I]

- On YouTube the first dubbing costs nothing and needs no tool: automatic
  dubbing covers twenty languages from English. Paid dubbing matters for the
  course itself, hosted elsewhere, and for a better voice than the automatic one.
- For hands-on footage where the speaker is mostly off camera, lip-sync is
  worth little; the audio-only prices are the ones to compare: 0.33 dollars a
  minute (ElevenLabs v1, 29 languages) against 0.57 (HeyGen) and 2.20
  (ElevenLabs v2). A ten-hour course into one language is 600 minutes.
- An agent can drive FFmpeg, local Whisper, the ElevenLabs and HeyGen
  interfaces, Auphonic and Descript without a screen. It may not drive CapCut.
- Cloning his own voice needs his consent on record and, on YouTube, no
  disclosure label.
