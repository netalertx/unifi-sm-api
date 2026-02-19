import pytest
import json
import logging
from unifi_sm_api.api import SiteManagerAPI
from tests.config import API_KEY, BASE_URL, VERSION, VERIFY_SSL

logging.basicConfig(level=logging.INFO)
api = SiteManagerAPI(api_key=API_KEY, version=VERSION, base_url=BASE_URL, verify_ssl=VERIFY_SSL)


def test_init_sites():
    result = api.get_sites()
    assert isinstance(result, list) or isinstance(result, dict)
    print(json.dumps(result, indent=2))
    logging.info(json.dumps(result, indent=2))


def test_init_devices_and_clients_all_sites():
    sites_resp = api.get_sites()

    assert isinstance(sites_resp, dict), "Expected dict with 'data' key"
    sites = sites_resp.get("data", [])
    assert isinstance(sites, list), "Expected 'data' to be a list"
    assert len(sites) > 0, "No sites returned"

    for site in sites:
        site_id = site["id"]
        site_name = site.get("name", "Unnamed Site")
        print("\n=======================SITE===========================")
        logging.info(f"\n--- Site: {site_name} ({site_id}) ---")

        # --- Devices ---
        unifi_devices = api.get_unifi_devices(site_id)
        assert isinstance(unifi_devices, (list, dict)), f"Devices response for site {site_id} should be list or dict"
        print("\n==================UNIFI DEVICES=======================")
        print(f"\nDevices for {site_name} ({site_id}):")
        print(json.dumps(unifi_devices, indent=2))
        logging.info(json.dumps(unifi_devices, indent=2))

        # --- Clients ---
        clients = api.get_clients(site_id)
        assert isinstance(clients, (list, dict)), f"Clients response for site {site_id} should be list or dict"

        print("\n=====================CLIENTS=========================")
        print(f"\nRetrieved {len(clients)} clients for {site_name} ({site_id}):")
        print(json.dumps(clients, indent=2))
        logging.info(json.dumps(clients, indent=2))
