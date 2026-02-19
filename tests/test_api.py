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


def test_get_sites_structure():
    resp = api.get_sites()

    # sites API might still be raw dict or list
    assert isinstance(resp, (list, dict)), "Sites must be list or dict"

    if isinstance(resp, dict):
        assert "data" in resp
        assert isinstance(resp["data"], list)

    print(json.dumps(resp, indent=2))


def test_devices_response_formats():
    sites_resp = api.get_sites()

    assert isinstance(sites_resp, dict), "Expected dict with 'data'"
    sites = sites_resp.get("data", [])
    assert len(sites) > 0, "No sites returned"

    site_id = sites[0]["id"]

    # --- Default (dict) ---
    resp = api.get_unifi_devices(site_id)
    assert_paginated_response(resp)

    # --- List mode ---
    resp_list = api.get_unifi_devices(site_id, as_list=True)
    assert_list_response(resp_list)

    # Ensure same data length
    assert len(resp_list) == len(resp["data"])


def test_clients_response_formats():
    sites_resp = api.get_sites()

    sites = sites_resp.get("data", [])
    site_id = sites[0]["id"]

    # --- Default (dict) ---
    resp = api.get_clients(site_id)
    assert_paginated_response(resp)

    # --- List mode ---
    resp_list = api.get_clients(site_id, as_list=True)
    assert_list_response(resp_list)

    assert len(resp_list) == len(resp["data"])


def test_max_items_limit():
    sites_resp = api.get_sites()
    site_id = sites_resp["data"][0]["id"]

    max_items = 5

    resp = api.get_unifi_devices(site_id, max_items=max_items)
    assert_paginated_response(resp)
    assert len(resp["data"]) <= max_items

    resp_list = api.get_unifi_devices(site_id, max_items=max_items, as_list=True)
    assert_list_response(resp_list)
    assert len(resp_list) <= max_items


def test_device_object_structure():
    sites_resp = api.get_sites()
    site_id = sites_resp["data"][0]["id"]

    resp = api.get_unifi_devices(site_id, max_items=1, as_list=True)

    if not resp:
        pytest.skip("No devices to validate")

    device = resp[0]

    # Validate expected keys (adjust as needed)
    expected_keys = ["id", "name"]

    for key in expected_keys:
        assert key in device, f"Missing key '{key}' in device"


def test_client_object_structure():
    sites_resp = api.get_sites()
    site_id = sites_resp["data"][0]["id"]

    resp = api.get_clients(site_id, max_items=1, as_list=True)

    if not resp:
        pytest.skip("No clients to validate")

    client = resp[0]

    expected_keys = ["id", "ipAddress"]

    for key in expected_keys:
        assert key in client, f"Missing key '{key}' in client"


# -------------------------
# Helpers
# -------------------------

def assert_paginated_response(resp):
    """Ensure dict response format is correct"""
    assert isinstance(resp, dict), "Response should be dict"
    assert "data" in resp, "Missing 'data' key"
    assert isinstance(resp["data"], list), "'data' must be list"

    # Optional but expected keys
    for key in ["count", "totalCount", "offset", "limit"]:
        assert key in resp, f"Missing '{key}' key"

    assert resp["count"] == len(resp["data"]), "count mismatch"


def assert_list_response(resp):
    """Ensure list response format is correct"""
    assert isinstance(resp, list), "Response should be list"

