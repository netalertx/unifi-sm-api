# UniFi Site Manager API Client

Python library for interacting with UniFi’s Site Manager Integration API. Tested on a selfhosted local instance only. Downlod from here: https://pypi.org/project/unifi-sm-api/

> [!NOTE]
> This library was mainly creted to be used with [NetAlertX](https://github.com/jokob-sk/NetAlertX), as such, full API coverage is not planned. PRs are however more than welcome.

## 📦 Usage

Navigate to Site Manager _⚙️ Settings -> Control Plane -> Integrations_.

- `api_key` : You can generate your API key under the _Your API Keys_ section.
- `base_url` : You can find your base url in the _API Request Format_ section.
- `version` : You can find your version as part of the url in the _API Request Format_ section.

```python
from unifi_sm_api.api import SiteManagerAPI

api = SiteManagerAPI(
    api_key="fakeApiKey1234567890",
    base_url="https://192.168.100.1/proxy/network/integration/",
    version="v1",
    verify_ssl=False
)

sites = api.get_sites()

for site in sites:
    site_id = site["id"]

    unifi_devices = api.get_unifi_devices(site_id=site_id)
    clients = api.get_clients(site_id=site_id)
```

---

## 📘 Endpoints Covered

- `/sites` — list available sites
- `/sites/{site_id}/devices` — list UniFi devices for a site
- `/sites/{site_id}/clients` — list connected clients
- `/sites/{site_id}/wans`

## 🔧 Requirements

- Python 3.8+
- `requests`
- `pytest` (for running tests)
- Local `.env` file with API credentials

---

## Testing

### 🌍 Environment Setup

Create a `.env` file in the project root with the following:

```env
API_KEY=fakeApiKey1234567890
BASE_URL=https://192.168.100.1/proxy/network/integration/
VERSION=v1
VERIFY_SSL=False
```
### 🧪 Running Tests

Make sure PYTHONPATH includes the project root, then run:

```bash
python3 -m venv venv && source venv/bin/activate
pip install pytest python-dotenv
cd unifi-sm-api/
pip install -e .
PYTHONPATH=.. pytest -s tests/test_api.py
```

## 💙 Donations

- [GitHub](https://github.com/sponsors/jokob-sk)
- [Buy Me A Coffee](https://www.buymeacoffee.com/jokobsk)
- [Patreon](https://www.patreon.com/user?u=84385063)