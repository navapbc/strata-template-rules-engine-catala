<p>
  <img src="template-only-docs/assets/Nava-Strata-Logo-V02.svg" alt="Nava Strata" width="400">
</p>
<p><i>Open source tools for every layer of government service delivery.</i></p>
<p><b>Strata is a gold-standard target architecture and suite of open-source tools that gives government agencies everything they need to run a modern service.</b></p>

<h4 align="center">
  <a href="https://github.com/navapbc/strata-template-rules-engine-catala/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-apache_2.0-red" alt="Nava Strata is released under the Apache 2.0 license" >
  </a>
  <a href="https://github.com/navapbc/strata-template-rules-engine-catala/blob/main/CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs welcome!" />
  </a>
  <a href="https://github.com/navapbc/strata-template-rules-engine-catala/issues">
    <img src="https://img.shields.io/github/commit-activity/m/navapbc/strata-template-rules-engine-catala" alt="git commit activity" />
  </a>
  <a href="https://github.com/navapbc/strata-template-rules-engine-catala/repos/">
    <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/navapbc/strata-template-rules-engine-catala/total">
  </a>
</h4>

# Template Rules Engine (Catala)

## Overview

This is a template for creating a rules engine using [Catala](https://catala-lang.org/), a domain-specific language designed to faithfully translate legislative and regulatory texts into executable code. This template includes:

* Catala source files for encoding legislative rules with literate programming style
* Compilation pipeline from Catala to Python
* REST API for exposing compiled rules as endpoints
* Docker-based development environment with the Catala compiler pre-installed
* Thorough formatting & linting tools for the Python wrapper layer
* CI/CD workflow for linting, typechecking, and testing

The template application is intended to work with the infrastructure from [template-infra](https://github.com/navapbc/template-infra).

## Installation

To get started using the template application on your project:

1. [Install the nava-platform tool](https://github.com/navapbc/platform-cli).
2. Install template by running in your project's root:
    ```sh
    nava-platform app install --template-uri https://github.com/navapbc/strata-template-rules-engine-catala . <APP_NAME>
    ```
3. Follow the steps in `/docs/<APP_NAME>/getting-started.md` to set up the application locally.
4. Optional, if using the Platform infrastructure template: [Follow the steps in the `template-infra` README](https://github.com/navapbc/template-infra#installation) to set up the various pieces of your infrastructure.

## What is Catala?

[Catala](https://catala-lang.org/) is a programming language adapted for socio-fiscal legislative purposes. It allows developers to:

- Write rules alongside the legislative text they implement (literate programming)
- Handle complex legal logic including exceptions and edge cases
- Generate executable code (Python, OCaml) from the legislative specification
- Produce human-readable documentation from the same source

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Community

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guidelines](CONTRIBUTING.MD)
- [Security Policy](SECURITY.md)
