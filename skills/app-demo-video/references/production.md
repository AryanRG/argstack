# Capture and export

Use the available Playwright CLI in a named session. Resize before capture. For example: open the demo URL, resize to 1440 by 720, snapshot, then run video-start with the filename, --size=1440x720 and --cursor when supported. Perform the actual action, check the new UI, pause for readability and video-stop. Check the installed CLI help for available flags. Record distinct takes or use multiple intervals of one recording. When using Playwright's context-level recordVideo instead, close the context before consuming its output. Never disable a project's security checks just to film a flow.

For native apps, capture a specific window or a simulator. Omit the desktop and notifications. Do not stretch portrait footage: compose a portrait delivery or use an intentional frame. When you need the original sound, supply a mixed narration track or edit separately; the bundled renderer deliberately strips raw clip audio.

Create an edit.json alongside the footage (relative paths resolve against the manifest). start and duration are seconds. Titles, labels and captions are literal text. Keep captions short; the renderer rejects overlong lines. Example:
~~~json
{"brand":"Linen","title":"Invoice review","shots":[{"clip":"compare.webm","start":1,"duration":4,"label":"Compare","caption":"Twelve units at five dollars over the agreed price."}]}
~~~

Run: uv run --script <skill-directory>/scripts/render.py edit.json <new-output-directory>. Requires ffmpeg/ffprobe and Arial or DejaVu Sans. UV resolves Pillow separately from the project's environment. Optional top-level narration is a local audio path. The output directory must not already exist.

The renderer exports H.264 MP4, burned-in captions, a matching WebVTT transcript, a final-state poster and a contact sheet. Do not enable the sidecar by default in a player that already shows the burned-in captions. For narration with different wording, supply a separately transcribed speech track. The contact sheet is an editorial check, not a substitute for reviewing interaction timing.

## Voiceover
Set top-level `"voiceover":{"voice":"Samantha","words_per_minute":170}` for offline macOS speech. Pick another installed voice with `say -v '?'`. Each shot uses its caption by default; set `spoken` to a natural spoken line and `voice_start` to its offset in seconds. Set `spoken` to an empty string for a deliberate silent beat. Lines that overrun the shot cause an error identifying the shot. The renderer aligns voice to 30 fps cuts, normalizes the assembled track and includes `voiceover.vtt` with the spoken wording. Use that sidecar for speech accessibility. For a human recording, use the existing top-level narration path instead. For silent output omit both fields.

### Conversational walkthrough preset

For a presenter walking someone through a task, try `"voiceover":{"engine":"kokoro","voice":"af_heart","speed":1.0}`. This is a local synthetic voice. Keep the macOS preset for a quick cut or for a comparison. After the first setup no external speech service receives the script. The helper uses uv with Python 3.12 and kokoro-onnx 0.4.9. Put kokoro-v1.0.int8.onnx and voices-v1.0.bin from the [model-files-v1.0 release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) in ~/.local/share/argstack/voice-models/kokoro-v1, or specify model_dir.

Frame each line as something a colleague would actually say while driving: invite the viewer to look, explain the clue on screen, then say what you are doing about it. For example: “We agreed on eighty dollars a ream. They've billed us eighty-five.” Let the screen supply obvious labels. Skip filler, vary sentence length, and leave a beat for the result. For an A/B comparison keep the picture, mix level and duration fixed.
