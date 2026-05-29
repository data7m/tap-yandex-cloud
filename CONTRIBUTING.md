# Contributing

## Local checks

- uvx ruff check tap_yandex_cloud tests
- uvx ruff format tap_yandex_cloud tests
- uv run pytest
- uv run --group typing mypy tap_yandex_cloud tests
- uv run --group typing ty check tap_yandex_cloud tests
- uv run tap-yandex-cloud --config ENV --discover
- uv run tap-yandex-cloud --config ENV

## Useful commands

- build package by command: uv build
- run tests by command: uv run pytest
- run tests by command: uvx --with tox-uv tox
- format code by command: uvx ruff format tap_yandex_cloud tests
- lint code by command: uvx ruff check tap_yandex_cloud tests
- fix linter errors by command: uvx ruff check tap_yandex_cloud tests --fix

## Environment variables

export TAP_YANDEX_CLOUD_BILLING_ACCOUNT_ID="..."
export TAP_YANDEX_CLOUD_IAM_TOKEN="$(yc iam create-token)"
export TAP_YANDEX_CLOUD_SERVICE_ACCOUNT_KEY_JSON="$(jq -c . authorized_key.json)"
export TAP_YANDEX_CLOUD_START_DATE="2026-05-25T00:00:00Z"
export TAP_YANDEX_CLOUD_END_DATE="2026-05-27T00:00:00Z"
export TAP_YANDEX_CLOUD_AGGREGATION_PERIOD="DAY"
export TAP_YANDEX_CLOUD_LOOKBACK_DAYS="7"
export TAP_YANDEX_CLOUD_API_ENDPOINT="billing.api.cloud.yandex.net:443"

### Billing account id

Available at Yandex Cloud → Billing or
```bash
export YC_IAM_TOKEN="$(yc iam create-token)"

curl \
  -H "Authorization: Bearer $YC_IAM_TOKEN" \
  https://billing.api.cloud.yandex.net/billing/v1/billingAccounts
```
