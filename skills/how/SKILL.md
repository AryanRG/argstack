---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Trace one concrete request or event from entry point to observable result. Verify the owning module, data boundary, and any important branch or failure path. For a small question, do this in the current agent. For a larger one, divide the investigation by subsystem; use read-only delegates only if permitted and useful. Pass evidence with file locations between explorers and the explainer. Use the current harness's available models/tools. If delegation is unavailable, do the exploration locally.
  
Use the bundled [explorer brief](references/explorer-prompt.md) and [explainer brief](references/explainer-prompt.md) as templates, not as evidence that agents were spawned. Explain in the user's terms; include the key source locations and distinguish verified behavior from inference. Do not edit the subsystem during a walkthrough.
