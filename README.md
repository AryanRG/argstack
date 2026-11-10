# argstack

A collection of agent skills for building software, reviewing changes, preparing documents, and working unattended. The same skill directory can be linked into multiple agent runtimes, including Codex, Claude Code, Pi and Kiro. Each harness still supplies its own tools, permissions and model access.

## Try it

Clone to a directory you plan to keep. The installer creates symlinks; moving the clone breaks them. Use a fresh target for a trial or choose a few skills first.

~~~sh
git clone https://github.com/AryanRG/argstack.git
cd argstack
python3 install.py --list
python3 install.py --target ~/.agents/skills overnight council app-demo-video
~~~

For Claude Code, use its config directory's skills folder; for Pi, use its agent directory's skills folder. For isolated T3 providers, repeat the install against each configured provider home. Refresh provider discovery or start a new agent session. Invoke a skill from the host's picker, for example:

- **$overnight** — “Continue the current milestone. Done means the regression test passes. Leave publication for me.” Reads the goal back, makes reversible decisions and parks human-only gates. Use “confirm first” for a hard checkpoint. A skill cannot wake a sleeping machine or restart a stopped chat.
- **$council** — “Review this diff read-only. Give me the evidence and the disagreements.” Select real provider/model pairs in your environment; a second route to the same model is not a new model family.
- **$app-demo-video** — “Show how a user resolves this exception in staging. Make it a conversational walkthrough.” Includes a local editor, captions and optional voiceover; see the [production guide](skills/app-demo-video/references/production.md).

## Catalog

| Area | Skills |
| --- | --- |
| Unattended work and review | overnight, council, how, statechart |
| Pull requests | file-pr, modernize |
| Communication | bro, ketchup, ketchup-video, unslop |
| Product development | frontend-design, webapp-testing, mcp-builder, app-demo-video |
| Documents | docx, pdf, pptx, xlsx, [doc-coauthoring (upstream)](https://github.com/anthropics/skills/tree/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/doc-coauthoring) |

There are **18 bundled skills and one optional upstream skill**. To link all 19, run `python3 install.py --target /path/to/skills --all`. This fetches only the pinned doc-coauthoring text from its publisher and checks its SHA-256 before linking it. Installing bundled skills makes no network calls. Existing unrelated files and skills are never replaced. To uninstall, remove only the symlinks created by the installer.

Python 3.9+ and a filesystem with directory symlink support are needed for installation. Individual skills have their own runtime dependencies. In particular, statechart needs a TypeScript-capable runtime, Java and TLC; app-demo-video uses ffmpeg, ffprobe and uv. Model weights, test footage, provider configuration and logins are not included.

See [sources, adaptations, and licenses](THIRD_PARTY_NOTICES.md). This is an independent collection, not an official distribution of the upstream projects.
