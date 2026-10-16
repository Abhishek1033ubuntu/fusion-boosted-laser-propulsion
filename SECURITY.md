# Security & Version Support Policy

## Supported Versions

The table below outlines the active version support lifetime for the **Fusion-Boosted Laser-Ablative Propulsion System (`fusion-boosted-laser-propulsion`)** codebase, simulation solvers, and technical baseline documentation.

| Version | Release Date | Multi-Physics Baseline ID | Security & Bug Fix Support | Status |
| :--- | :--- | :--- | :--- | :--- |
| **4.1.x** | October 2026 | `FBLA-PROP-2026-REV4` | :white_check_mark: Supported | **Current Main Release** |
| **4.0.x** | September 2026 | `FBLA-PROP-2026-REV3` | :x: End of Life | Deprecated |
| **< 4.0** | Earlier Releases | Legacy Prototypes | :x: End of Life | Unsupported |

---

## Reporting a Vulnerability or Solver Defect

We take computational accuracy, numerical stability, and code safety seriously. If you discover a bug, numerical instability in PyTorch/Numba solvers, security vulnerability, or physical model discrepancy in this repository, please report it through secure channels.

### How to Report

1. **Email Notification:**  
   Please send details of the issue directly to the Principal Investigator:
   * **Lead Author / Principal Investigator:** Abhishek Singh
   * **Primary Email:** [abhishek1033@gmail.com](mailto:abhishek1033@gmail.com)
   * **Secondary Email:** [abhishek.s@live.in](mailto:abhishek.s@live.in)

2. **Information to Include:**
   * A clear description of the issue or mathematical discrepancy.
   * Steps or environment details (e.g., Python version, PyTorch/CUDA runtime, Colab GPU model) to reproduce solver errors.
   * Expected vs. actual numerical behavior.

### Response & Patch Timeline

* **Initial Acknowledgment:** Within **24 to 48 hours**.
* **Triage & Verification:** Within **5 business days**.
* **Fix & Patch Release:** Critical mathematical or code execution fixes will be committed directly to the `main` branch with an updated patch version tag (e.g., `v4.1.1`).

---

## Disclosure Policy

When a vulnerability or critical solver defect is identified and patched, full credit will be given to the reporter in the repository release notes (unless anonymity is requested).
