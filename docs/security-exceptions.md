# Security Exceptions

## Pi Claude Bridge dependency audit

- Owner: `joserosas-vanta/dotfiles` maintainers
- Accepted: 2026-11-17
- Re-reviewed: 2026-11-23, for the bump from `df907db` (0.9.1) to `5ea9bb8` (v0.13.0)
- Expires for re-review: 2027-02-17
- Scope: the commit-pinned `pi-claude-bridge` package configured in `group_vars/all.yml`
- Disposition: accepted for remote development-machine deployment

`npm audit --omit=dev` at commit `5ea9bb88bd54395c1fe38cc95ec2ce1dbdcf15cc` (v0.13.0) reported
five moderate and three high findings, with no critical findings, unchanged from the earlier
audit at `df907dbb5f9cec66446c89a9e2c8eb1c89a7828c`. The high findings involved
`@modelcontextprotocol/sdk`, `body-parser`, and `zod`. This records automated audit output, not a
claim that each finding is exploitable in the Pi integration.

Compensating controls:

- The source repository is fetched over HTTPS at an explicit commit SHA.
- Dependencies are installed with `npm ci` from the committed lock file.
- The package is installed only for the target workspace user.
- `fff.nvim` is not installed.

At expiry, maintainers must re-run the production-dependency audit and either update the pin,
renew this exception with current evidence, or disable the managed package.
