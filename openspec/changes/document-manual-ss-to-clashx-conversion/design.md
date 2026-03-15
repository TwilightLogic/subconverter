## Context

This fork exploration taught us a practical workflow that is not obvious from the upstream `subconverter` README alone: a raw Shadowsocks share link can be valid input for conversion, but a ClashX/Clash Meta client expects a Clash-style YAML document or a subscription endpoint that returns one. We manually decoded a single-node `ss://` link, translated it into a minimal Clash Meta configuration, debugged common client-side issues such as empty proxy groups and inactive system proxy settings, and confirmed the node by real traffic tests.

The change is documentation-only, but it still benefits from design decisions because the value is in preserving the reasoning and the failure modes, not just pasting a final YAML snippet.

## Goals / Non-Goals

**Goals:**
- Preserve a repeatable manual conversion workflow for a single Shadowsocks node.
- Explain the minimum ClashX/Clash Meta YAML structure required for a working manual import.
- Capture the debugging checkpoints that distinguish "node parses" from "traffic is actually proxied".
- Make the document specific to what we learned in this fork so future automation work has a reliable baseline.
- Preserve the thinking path behind the workflow so readers can understand why each step exists and when to stop using the manual path.

**Non-Goals:**
- Implement automatic conversion inside the application.
- Replace the upstream README or describe every supported subscription format.
- Cover multi-node subscriptions, provider automation, or advanced rule-set design in depth.

## Decisions

### Record the workflow as a new capability-specific spec
We will define a dedicated capability, `manual-node-conversion-docs`, instead of burying the knowledge in an ad hoc note. This keeps the change archiveable and gives future work a formal requirement baseline.

Alternative considered:
- Add a loose markdown note outside OpenSpec. Rejected because it would not integrate with the repo's spec-driven workflow and would be easier to lose or bypass later.

### Center the documentation on a single-node manual path
The document will focus on one valid and tested path: `ss://` share link -> decoded node fields -> Clash Meta YAML -> client verification. This is the smallest useful learning artifact and matches what we actually validated.

Alternative considered:
- Generalize immediately to all subscription formats. Rejected because it would dilute the clarity of the lessons we actually confirmed.

### Include troubleshooting as first-class behavior
The spec will require the document to explain at least the following failure modes: raw `ss://` links are not the same as Clash subscriptions, empty `proxy-groups` lead to no selectable nodes, and seeing the wrong public IP often means the system proxy or mode is not active.

Alternative considered:
- Only document the final working YAML. Rejected because the hard part of the exercise was diagnosis, not syntax.

### Blend procedure with reasoning instead of splitting them into separate documents
The learning page will keep the operational steps and the accompanying thought process close together. Readers should see not only what to do next, but also what uncertainty that step is resolving.

Alternative considered:
- Write one strict how-to guide and a separate retrospective note. Rejected because the split would make the diagnostic reasoning easier to miss and less useful during actual troubleshooting.

## Risks / Trade-offs

- [Risk] Documentation may overfit this one Shadowsocks example. -> Mitigation: describe the example as an instance of a reusable single-node workflow and name the fields that generalize.
- [Risk] Future client UI changes may make exact menu labels stale. -> Mitigation: emphasize configuration structure and verification behavior over fragile screenshot-level instructions.
- [Risk] Readers may treat the manual path as a full replacement for subscription-based workflows. -> Mitigation: explicitly document the limits of manual conversion and note that it is best for learning, testing, or one-off nodes.

## Migration Plan

Add the OpenSpec artifacts for this change. No runtime migration, deployment, or rollback steps are required because the change does not alter application behavior.

## Open Questions

- Whether we want a follow-up change that turns the manual workflow into a helper script or example input/output pair in the main repository.
