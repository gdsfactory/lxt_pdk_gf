# Public PDK continuous integration

Tag: `pdk-public-ci`

The public LXT PDK delegates code checks, model checks, coverage, documentation, DRC, GDS comparison, and review automation to `doplaydo/pdk-ci-workflow-public`. The development Makefile fetches pre-commit configuration from the same public repository.

Nyanlib generation passes `GFP_API_KEY`, `GFP_ECR_IMAGE`, and `SHARED_SERVICES_AWS_OIDC_ROLE_ARN` to the public workflow and grants the required OIDC permission. Secret values stay in GitHub Actions configuration.

Release publication runs only on pushed `v*` tags. The tag version matches the project version in `pyproject.toml` before the distribution is built and checked. The workflow uploads the distribution to PyPI using the configured credentials, skipping files already uploaded on a retry, then publishes an existing GitHub draft or creates release notes for the tag. It does not create version bumps or tags. There is no separate Release Drafter workflow.

Shared security scans follow the canonical public security template. A template must reference public actions or run scanners locally so that a public caller can start its jobs.
