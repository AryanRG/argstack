---
name: council
description: Convene independent reviewers for a council on a proposal, implementation, or tradeoff. Resolve the requested panel and report evidence and disagreements.
---

# Council

Identify the decision or diff, exact revision where applicable, and review-only scope. Take the user's named panel first. Otherwise use the roster guidance below, resolving every target against the current catalog before dispatch. A provider instance determines routing and billing: do not drop the instance, normalize dots into hyphens, switch accounts or spend API credits as a fallback.

Resolve three seats from the user’s own roster, for example GPT Astra for architecture, Claude Opus for regressions, and Claude Fable for counterexamples. Treat provider and model as a pair. In T3, query each configured instance by family, including omitted models, and use the exact advertised slug. An API-credit seat must be explicitly selected by the user or their roster. If no roster is configured, use distinct suitable already-authorized routes; report when fewer than three are available. Never silently cross billing routes. If versions are ambiguous do not claim the selected version is the latest.

These are independent reviewers, not necessarily three independent model families. Do not count the parent as a delegate. If an explicit member is unavailable, name it; proceed with available members unless the user requires the complete panel. Never invent an independent opinion or silently substitute a same-name model. If no delegation tool is available, report that the council did not run; offer a separately labeled single-agent analysis.

In T3, use orchestrator_capabilities (including model search) and delegate_task with explicit target.providerInstanceId and target.model. Set role to review, use asynchronous dispatch, and use a stable clientRequestId per seat and round. Only pass effort if the live schema supports it; never claim a configured effort without evidence. Outside T3, use the host’s available delegation tool only if it can address the requested route. A chat saying “I am Opus” is not routing verification.

Give each reviewer the same decision, constraints, and source material, without the other reviewers’ conclusions. Request a read-only assessment with a concrete failure case, supporting evidence, and a proposed check. For design questions ask what would change the recommendation. Track task IDs and result states. Poll existing tasks; a wait timeout is not permission to start another paid worker. Use a bounded wait; if activity stops or the time budget expires, report incomplete seats and stop or cancel only this council’s workers per the user's instructions.

One independent round by default. Verify actionable findings against sources or tests; keep material dissent and label unknowns. Only run one targeted follow-up round if new evidence or an authorized fix changes the decision. Do not iterate for unanimity. Report the actual routes, completed/failed seats, recommendation and remaining disagreement. A review request alone does not authorize edits, PR publication, or a merge.
