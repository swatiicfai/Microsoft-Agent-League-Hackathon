# Security Policy

## Supported Versions

AutoUI is currently in active development for the Microsoft Agents League Hackathon. The main branch is the only supported version.

| Version | Supported          |
| ------- | ------------------ |
| `main`  | :white_check_mark: |

## Reporting a Vulnerability

Security and confidential information protection are top priorities for AutoUI.

This project is designed as a client-side only application. User API keys (such as Google Gemini or Microsoft Azure OpenAI keys) are processed entirely locally within the user's browser. **Keys are never transmitted to our servers or stored in any database.** 

If you discover a vulnerability or security issue that could expose API keys or result in cross-site scripting (XSS) within the generated sandboxed iframe, please report it immediately.

**How to report:**
1. Please do NOT open a public issue for security vulnerabilities.
2. Email the repository owner directly.
3. Include steps to reproduce the issue and the potential impact.

We will acknowledge your report within 48 hours and work to issue a patch as quickly as possible.
