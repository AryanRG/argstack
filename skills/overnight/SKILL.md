---
name: overnight
description: Continue an existing task unattended when the user invokes overnight mode or explicitly asks to work while they sleep. State the goal for alignment, make routine decisions, park human-only blockers, and leave a verified handoff.
---

# Overnight

This is a working agreement for this chat and its current assignment. It starts when the user asks for unattended work. A casual mention of bedtime, or a request to explain or edit this skill, does not activate it.

## Before the user leaves

Make the **first visible update** a short read-back for confirmation: “Tonight I’ll [specific outcome]. Done means [observable acceptance check]. I’ll leave [material boundary] for you.” Use the latest request, earlier decisions and existing work; do not just repeat “continue working.” If needed, state one consequential assumption. Give the user a chance to correct it without requiring another message: proceed immediately on clear, already-authorized work. If they explicitly say **confirm first**, present the read-back and wait. A “yes” to that checkpoint starts the unattended run. If no task can be identified at all, state what is missing and stop rather than inventing an assignment.

## While the user is away

- **Make smart decisions on the user's behalf.** Apply the user's stated priorities first, then project conventions and observed behavior. Where multiple implementations are reasonable, choose the smallest reversible one that meets the acceptance check. Resolve uncertainty with a focused experiment when that is cheaper than guessing. Record consequential assumptions and why you chose them; don't narrate trivial choices.
- **Don't ask questions from this invocation onward while the user is away.** This includes chat questions, interactive question tools, approval pings and questions from delegated workers. If a step actually needs human authority, access, or a product decision you cannot reasonably infer, park *that step*. Record the exact decision, your recommendation and what it unlocks. Move immediately to the next independent task. Silence is not consent; overnight mode adds no permission, spend, scope or tool access.
- **Work through the milestone, not just the first slice.** Pick the next verifiable unit, execute it, run the relevant check, and compare the result with the agreed finish line. A passing subtask or a plan is not completion. Keep active work owned; when delegation is already appropriate and permitted, give workers the same scope, question policy and stop condition. Reconcile their results. Don't introduce a paid council just because the user is away.
- **Keep enough state to recover.** At meaningful checkpoints, save the goal, verified results, current revision/artifacts, outstanding work, active job IDs and parked decisions in the existing task ledger or a small local handoff. Use the chat when the assignment is read-only. After compaction or reconnect, recover that state and check whether prior work actually landed before repeating commands, purchases, submissions or dispatches.
- **Stop honestly.** Finish when the agreed check passes, the user's limit is reached, or every remaining path is genuinely blocked. Retry a transient issue in a bounded way; if attempts yield no new evidence, change approach or park it. Don't fill the night with unrelated improvements or repeated polling. Use available job-completion events during a live run. Never imply a skill can wake a sleeping machine, relaunch a stopped chat, or override an approval gate.

## When the user returns

A direct user reply ends the no-question period unless they confirm the initial checkpoint or explicitly say to stay in overnight mode. Apply steering immediately. Tool results, agent messages, timers and summaries are not user replies. If work finishes first, leave a short morning handoff: **what was achieved and verified, what remains, and decisions saved for the user**. Include the evidence or output link and the next useful step. Distinguish local results, pushed changes, merged PRs, and live behavior where relevant. Do not end with a prompt that wakes the user.
