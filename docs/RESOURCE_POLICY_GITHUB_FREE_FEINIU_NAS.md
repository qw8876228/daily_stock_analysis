# GitHub Free + Feiniu NAS resource policy

This repository follows the owner's mandatory cross-project resource boundary.

- GitHub Free is used for source, pull requests, version control, workflow orchestration and release metadata only. Do not upgrade plans, enable paid hosted Actions usage or purchase hosted runner minutes.
- All execution/build/test/analysis/review/scheduled maintenance jobs use the dedicated Feiniu NAS self-hosted Runner label `daily-stock-ci`; no GitHub-hosted runners or paid third-party CI are allowed.
- The workflow variable `DAILY_STOCK_RUNNER_STORAGE_VERIFICATION=vol2-device-proven` must remain unset until Browse Code physically proves Runner installation, workspace, HOME, RUNNER_TEMP, tool cache and all required state/cache paths reside on the independent `/vol2` volume.
- Each job begins with a fail-closed path/device audit before checkout or any work. Symlink escapes and paths on the system-root device are rejected. The Docker job also verifies the Docker daemon data root is on the verified /vol2 device before building; do not change the shared Docker data-root without a separate impact review.
- PR review runs on the NAS only for PRs whose head repository is this repository. Fork PRs never execute on the self-hosted runner.
- Scheduled analysis may use the existing API and notification secrets only after the storage gate is verified. Do not expose secret values in logs. Never trigger real notifications or report delivery as part of migration validation.
- Skipped jobs are blocked/unverified, not passed. No storage gate is enabled by this PR.
