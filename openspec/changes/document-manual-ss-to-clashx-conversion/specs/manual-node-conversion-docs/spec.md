## ADDED Requirements

### Requirement: Document manual Shadowsocks-to-Clash conversion
The project SHALL document a manual workflow for converting a single valid `ss://` share link into a ClashX/Clash Meta YAML configuration without relying on automated subscription generation.

#### Scenario: Reader starts from a raw Shadowsocks link
- **WHEN** a reader has a single `ss://` node link and wants to use it in ClashX or Clash Meta
- **THEN** the documentation MUST explain that the link represents a single node share and not a Clash subscription document
- **THEN** the documentation MUST describe the node fields that need to be extracted or inferred for Clash YAML, including server, port, cipher, password, and node name

### Requirement: Provide a minimum working Clash Meta configuration shape
The project SHALL document the minimum YAML structure required for ClashX/Clash Meta to load and expose a manually added Shadowsocks node as a selectable proxy.

#### Scenario: Reader needs a valid local configuration
- **WHEN** a reader follows the manual conversion workflow
- **THEN** the documentation MUST include a working configuration example containing `proxies`, `proxy-groups`, and `rules`
- **THEN** the documentation MUST show the manually added node inside a selectable group rather than leaving `proxy-groups` empty
- **THEN** the documentation MUST include a routing mode that makes validation straightforward, such as a global path for initial testing

### Requirement: Explain how to verify effective proxy usage
The project SHALL document the difference between successfully loading a node and actually sending traffic through it.

#### Scenario: Reader sees an unexpected public IP
- **WHEN** the client displays the imported node but public IP checks still show the local network location
- **THEN** the documentation MUST direct the reader to verify the active proxy group selection, routing mode, and system proxy status
- **THEN** the documentation MUST explain that successful speed tests or node selection alone do not prove all traffic is using the proxy

### Requirement: Document the limits of the manual workflow
The project SHALL explain where the manual single-node workflow is useful and where it stops short of a full subscription-based setup.

#### Scenario: Reader compares manual setup to airport subscriptions
- **WHEN** a reader asks whether the manual YAML setup is equivalent to configuring a full airport subscription
- **THEN** the documentation MUST explain that the manual approach configures individual nodes successfully
- **THEN** the documentation MUST explain that automatic node updates, multi-node rotation, and subscription maintenance remain out of scope for this workflow

### Requirement: Preserve reasoning alongside the steps
The project SHALL present the manual workflow with the reasoning that motivated the major decisions and checks, not only with final instructions.

#### Scenario: Reader wants to understand why the manual path existed
- **WHEN** a reader follows the learning document from top to bottom
- **THEN** the document MUST explain why manual conversion was useful as a debugging and learning path even though automatic conversion exists in the project
- **THEN** the document MUST connect key steps to the uncertainty they resolve, such as separating node parsing issues from client import or proxy activation issues
