"""
Generates realistic sample markdown documents in markdown_docs/ matching
the 3 core reference documents from the curated QA dataset:
1. javascript_tutorial.md
2. blockchain.md
3. fortinet.md

This enables immediate learning, testing, indexing, and evaluation without
requiring external PDF downloads.
"""

import os
import sys
from pathlib import Path

# Ensure workspace root is in python path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning import config


def create_sample_documents(target_dir: str = None) -> list[str]:
    """
    Creates the sample markdown files required for RAG learning and evaluation.
    
    Args:
        target_dir: Directory to write the markdown files into (default: config.MARKDOWN_DIR)
        
    Returns:
        List of generated file paths.
    """
    out_dir = Path(target_dir or config.MARKDOWN_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    files_created = []

    # 1. javascript_tutorial.md
    js_content = """# JavaScript Tutorial & Reference Guide

## 1. Overview and Capabilities
Client-side JavaScript lets an HTML page include programs that interact with the user, control the browser, and dynamically create content. For example, a form can check if the user has entered a valid e-mail address when they submit the form, and the form submission is sent only if all the entries are valid.

### Advantages of JavaScript
The tutorial lists four main advantages of using JavaScript on a web page:
- **Less server interaction**: You can validate user input before sending the page off to the server. This saves server traffic, which means less load on your server.
- **Immediate feedback to the visitors**: Visitors do not have to wait for a page reload to see if they have forgotten to enter something.
- **Increased interactivity**: You can create interfaces that react when the user hovers over them with a mouse or activates them via the keyboard.
- **Richer interfaces**: You can use JavaScript to include such items as drag-and-drop components and sliders to give a Rich Interface to your site visitors.

### Limitations of Client-Side JavaScript
We cannot treat client-side JavaScript as a full-fledged programming language because it lacks the following important features:
- Client-side JavaScript does not allow the reading or writing of files. This has been kept for security reasons.
- JavaScript cannot be used for networking applications because there is no such support available.
- JavaScript doesn't have any multithreading or multiprocessor capabilities.

### Development Tools
JavaScript does not require expensive development tools. You can start with a simple text editor such as Notepad or VS Code, and since it is an interpreted language inside the browser, you don't even need to buy a compiler.

## 2. Standards and Syntax
### ECMA-262 and Implementations
The ECMA 262 Specification defined a standard version of the core JavaScript language. Netscape's JavaScript and Microsoft's JScript conform to the ECMA-262 standard, though each browser vendor may add proprietary extensions that are not a part of the standard.

### Placement in HTML
JavaScript can be placed within the **<script>... </script>** HTML tags in an HTML document. You can place the script in either the `<head>` or the `<body>` section, but it is normally recommended that you should keep it within the **<head>** tags. In HTML 4, the type attribute's value should be set to "text/javascript".

### HTML Comments for Older Browsers
Older browsers that do not support JavaScript can be prevented from displaying raw script code using an optional HTML comment that surrounds our JavaScript code. The comment ends with a "//-->" where the "//" signifies a JavaScript single-line comment so the browser script engine does not execute the HTML closing sequence. It should be written as //-->.

### Whitespace and Semicolons
JavaScript ignores spaces, tabs, and newlines that appear in JavaScript programs. Simple statements in JavaScript are generally followed by a semicolon character, just as they are in C, C++, and Java. However, JavaScript allows you to omit this semicolon if each of your statements is placed on a separate line. But when formatted on a single line, you must use semicolons.

## 3. Variables and Operators
### Variable Naming Rules
When naming variables in JavaScript:
- You should not use any of the JavaScript reserved keywords (such as `break`, `boolean`, `function`).
- JavaScript variable names should not start with a numeral (0-9). They must begin with a letter or an underscore.
- JavaScript variable names are case-sensitive (e.g., `Name` and `name` are two different variables).

### Logical Operators
JavaScript supports standard boolean logical operators:
- `&& (Logical AND)`: Returns true if both operands are non-zero/true.
- `|| (Logical OR)`: Returns true if any of the two operands are non-zero/true.
- `! (Logical NOT)`: Reverses the logical state of its operand.
"""

    # 2. blockchain.md
    bc_content = """# Blockchain Technology: Fundamentals & Architecture

## 1. What is Blockchain?
A blockchain is a tamper-proof, shared digital ledger that permanently stores the history of asset exchanges across a peer-to-peer network. An asset can be tangible (a house, car, cash, land) or intangible (intellectual property, patents, copyrights, branding).

### Risks of Centralized Record-Keeping
Traditional centralized record-keeping gives a single entity, such as a bank or land registry, full control over transaction records. This architecture introduces single points of failure vulnerable to corruption, hacking, and business failures. Blockchain seeks to eliminate the need for gatekeepers by distributing consensus across independent cryptographic nodes.

### Historical Background
Before Bitcoin, cryptographic researchers laid foundational building blocks:
- In 1991, **Stuart Haber and W. Scott Stornetta** introduced cryptographically secured chains of blocks to securely timestamp digital documents so that they could not be backdated or tampered with.
- In 1998, **Nick Szabo conceptualized 'bit gold'**, a decentralized digital currency mechanism that required proof-of-work puzzles to mint coins.

### Bitcoin and Double Spending
In 2008, Satoshi Nakamoto released the Bitcoin whitepaper. Bitcoin was the first technology to prevent the issue of double spending without relying on any central authority or trusted third party, using a transparent and immutable ledger system governed by cryptographic consensus.

## 2. Cryptography and Consensus Mechanisms
### Cryptographic Foundations
- **Digital Signatures:** Participants sign transactions using their private key, and anyone on the network can verify authenticity using the sender's public key without revealing the private key.
- **Hash Functions:** Each block in the blockchain contains the hash of the previous block, creating an unbreakable mathematical chain. Altering data in any block changes its hash and invalidates all subsequent blocks.

### Comparison of Consensus Protocols
- **Proof of Work (PoW):** Nodes (miners) compete to solve computationally intensive mathematical puzzles to validate transactions and add new blocks.
- **Proof of Stake (PoS):** Validators are chosen to propose and validate blocks based on the number of tokens they hold and have committed as collateral (stake).
- **Delegated Proof of Stake (dPoS):** Token holders vote for a limited set of delegates (witnesses) who take turns validating transactions and producing blocks.
- **Proof of Authority (PoA):** A reputation-based consensus mechanism where pre-approved identity-validated nodes serve as authorities.

### Blockchain vs. Traditional Databases
Blockchain would be a better option when multiple untrusted parties need shared, immutable, and tamper-proof records without a central authority. Conversely, traditional databases may be more suitable for applications requiring extremely high throughput, private single-party writes, or low computational overhead.

### Permissionless vs Permissioned Networks
- **In permissionless blockchains**, there are no gatekeepers; anyone can read, write, and participate in consensus (e.g., Bitcoin, Ethereum).
- **In permissioned blockchains**, not anyone can join; access control lists restrict participant identities, common in enterprise consortia (e.g., Hyperledger Fabric).

## 3. Real-World Applications
### Supply Chain Traceability
Blockchain improves supply chain management by enhancing transparency, traceability, and security. It provides end-to-end visibility of goods from origin to end customer using unique digital identifiers and immutable timestamps on every handoff.

### Decentralized Finance (DeFi)
Traditional Finance, or TradFi, relies on centralized intermediaries like banks, brokers, and clearing houses. In contrast, Decentralized Finance (DeFi) operates on decentralized, open, and peer-to-peer models governed by autonomous smart contracts, creating financial products that are open, permissionless, and resistant to censorship.
"""

    # 3. fortinet.md
    fn_content = """# Fortinet Security Target & Evaluated Configuration

## 1. Target of Evaluation (TOE) Overview
The Target of Evaluation (TOE) Type is a **Boundary Protection Device**. The FortiGate Series or FortiGate Family provides firewall, VPN, antivirus, and traffic inspection capabilities. Physical hardware models include appliance hardware with FortiOS software, while Virtual Machine (VM) models consist only of the FortiOS virtual appliance software running on hypervisors.

### Evaluated Firmware Build
All evaluated models share a common software platform running **FortiOS 5.2.7 build number b718**, also designated as FortiOS 5.2.7 CC Compliant Firmware.

### Evaluation Scope and Exclusions
Features within the scope of this evaluation include:
- Core stateful firewall packet filtering
- IPsec and SSL virtual private networking (VPN)
- Antivirus inspection
- Web filtering security functional policies

Non-evaluated features: Antispam, content filtering and traffic shaping features are not included within the evaluated Common Criteria configuration.

## 2. Administration, Cryptography and Auditing
### Local and Remote Administration
Authorized administrators can access the FortiGate unit locally and remotely:
- A dedicated console port is available on all models for direct serial connection.
- Remote administration may be performed over SSH or using a web browser that supports TLS to allow HTTPS for the Network Web-Based GUI.

### Random Number Generation (FIPS-CC Mode)
In FIPS-CC mode, the Fortinet TOE supports a deterministic random bit generator (DRBG) compliant with NIST Special Publication 800-90A. The DRBG is seeded from a hardware-based random noise source with a minimum of 256 bits of entropy.

### Audit Generation and Protection
The TOE generates security audit records for administrative events, potential policy violations and information flow decisions. Each record records the identity of the administrator or user, event time, event type, and outcome. Access to view or export audit logs must be specifically granted to authorized roles.

## 3. Security Policies and Traffic Processing
### Information Flow Security Policies
The TOE enforces four information flow security functional policies (SFPs):
- Firewall SFP (restrictive default values, denies all non-explicitly permitted traffic)
- Web Filtering SFP (Web Filtering SFP has permissive default values, allowing categorized access unless prohibited)
- Antivirus SFP
- VPN SFP

### Packet Processing Workflow
The very first processing step when a packet arrives at an interface evaluates packet header anomalies to block syn floods, ping of death, source routing and port scans. Once verified, traffic is only passed to the next enforcement method in the pipeline.

### Authentication Mechanisms
The Fortinet TOE requires identification and authentication for all administrative actions and remote user sessions. Authentication methods include local passwords, RADIUS/LDAP, FortiToken one-time password generator devices, and client certificates. VPN peers authenticate using preshared keys or certificates.

### Secure Channels and Clustering
Trusted paths are used to protect remote administrator authentication using SSH and TLS version 1.1 or higher. In High Availability (HA) clusters, HA heartbeat encryption and authentication are disabled by default and must be explicitly configured by an administrator.
"""

    doc_map = {
        "javascript_tutorial.md": js_content,
        "blockchain.md": bc_content,
        "fortinet.md": fn_content,
    }

    for filename, content in doc_map.items():
        file_path = out_dir / filename
        file_path.write_text(content.strip(), encoding="utf-8")
        files_created.append(str(file_path))
        print(f"✓ Created sample document: {file_path.name} ({len(content)} chars)")

    return files_created


if __name__ == "__main__":
    print("Generating sample documents for Agentic RAG learning...")
    created = create_sample_documents()
    print(f"\n🎉 Successfully created {len(created)} sample documents in '{config.MARKDOWN_DIR}'")
