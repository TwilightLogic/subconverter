## Why

We manually converted a single `ss://` share link into a working ClashX/Clash Meta configuration while learning how this repository, subscription formats, and local client behavior fit together. That knowledge is currently trapped in chat context, so we need a project-local document that records the workflow, the pitfalls we hit, and the correct mental model for future contributors.

## What Changes

- Add a documented workflow for manually converting a Shadowsocks share link into a valid ClashX/Clash Meta YAML configuration.
- Capture the specific lessons learned during our fork-based exploration, including why a raw `ss://` link is not the same as a Clash subscription.
- Define validation guidance for confirming that a node is loaded, selected, and actually used as the active proxy.
- Document the limits of the manual approach so future work can build on it, such as multi-node generation or automated conversion.
- Interleave the learning document with the reasoning that led to each step so the page reads as a guided troubleshooting notebook rather than only a final recipe.

## Capabilities

### New Capabilities
- `manual-node-conversion-docs`: Document how to manually transform a single-node `ss://` link into a usable ClashX/Clash Meta configuration and how to validate the result.

### Modified Capabilities

## Impact

Affected areas are the OpenSpec change artifacts for this fork, the project-local learning document, and future contributor onboarding for manual subscription conversion work. There are no code, API, or dependency changes in this proposal.
