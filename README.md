# tap-yandex-cloud

`tap-yandex-cloud` is a Singer tap for YandexCloud.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPI repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPI:

```bash
uv tool install tap-yandex-cloud
```

Install from GitHub:

```bash
uv tool install git+https://github.com/ORG_NAME/tap-yandex-cloud.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-yandex-cloud --about --format=markdown
```
-->

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-yandex-cloud --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

tap-yandex-cloud supports two authentication methods:

`iam_token` — a short-lived IAM token.
`service_account_key_json` — a Yandex Cloud service account authorized key JSON.

For local development and quick checks, `iam_token` is the simplest option:

```bash
export TAP_YANDEX_CLOUD_IAM_TOKEN="$(yc iam create-token)"
```

IAM tokens are short-lived and are valid for up to 12 hours, so this method is not recommended for unattended production runs.

For production, prefer `service_account_key_json`. The tap uses the service account authorized key to generate IAM tokens automatically during execution. This avoids manually rotating `iam_token` before every scheduled run.

Example:

```bash
export TAP_YANDEX_CLOUD_SERVICE_ACCOUNT_KEY_JSON='{"id":"...","service_account_id":"...","created_at":"...","key_algorithm":"RSA_2048","public_key":"...","private_key":"..."}'
```

The service account must have enough permissions to read billing usage data for the configured billing account.

Minimal required tap settings:

```bash
export TAP_YANDEX_CLOUD_BILLING_ACCOUNT_ID="your-billing-account-id"
export TAP_YANDEX_CLOUD_START_DATE="2025-01-01T00:00:00Z"
export TAP_YANDEX_CLOUD_AGGREGATION_PERIOD="DAY"
export TAP_YANDEX_CLOUD_API_ENDPOINT="billing.api.cloud.yandex.net:443"
```

Then provide either:

```bash
export TAP_YANDEX_CLOUD_IAM_TOKEN="$(yc iam create-token)"
```

or:

```bash
export TAP_YANDEX_CLOUD_SERVICE_ACCOUNT_KEY_JSON='...'
```


## Usage

You can easily run `tap-yandex-cloud` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-yandex-cloud --version
tap-yandex-cloud --help
tap-yandex-cloud --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

Prerequisites:

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
then run:

```bash
uv run pytest
```

You can also test the `tap-yandex-cloud` CLI interface directly using `uv run`:

```bash
uv run tap-yandex-cloud --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Use Meltano to run an EL pipeline:

```bash
# Install meltano
uv tool install meltano

# Test invocation
meltano invoke tap-yandex-cloud --version

# Run a test EL pipeline
meltano run tap-yandex-cloud target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
