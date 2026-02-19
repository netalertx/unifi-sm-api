import requests


class SiteManagerAPI:
    def __init__(self, api_key: str, version: str = "v1", base_url: str = "https://api.ui.com/", verify_ssl: bool = True):
        self.api_key = api_key
        self.version = version
        self.base_url = base_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.headers = {
            "X-API-KEY": f"{self.api_key}",
            "Accept": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{self.version}/{endpoint.lstrip('/')}"
        response = requests.request(
            method,
            url,
            headers=self.headers,
            verify=self.verify_ssl,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    def _fetch_all_paginated(self, endpoint, params=None, max_items=None, page_size=100):
        """
        Fetch all paginated results automatically.

        :param endpoint: API endpoint
        :param params: dict of query params (e.g. filter)
        :param max_items: optional max number of items to return
        :param page_size: number of items per request
        :return: list of results
        """
        if params is None:
            params = {}

        offset = 0
        results = []

        while True:
            query = {
                **params,
                "offset": offset,
                "limit": page_size,
            }

            resp = self._request("GET", endpoint, params=query)

            data = resp.get("data", [])
            count = resp.get("count", len(data))
            total = resp.get("totalCount", 0)

            if not data:
                break

            results.extend(data)

            # Stop if we've reached max_items
            if max_items is not None and len(results) >= max_items:
                return results[:max_items]

            offset += count

            # Stop if we've fetched everything
            if offset >= total:
                break

        return results

    # https://{host}/proxy/network/integration/{version}/sites
    def get_sites(self):
        return self._request("GET", "sites")

    # https://{host}/proxy/network/integration/{version}/sites/{site_id}/devices
    def get_unifi_devices(self, site_id, max_items=None, filter=None):
        params = {}
        if filter:
            params["filter"] = filter

        return self._fetch_all_paginated(
            f"sites/{site_id}/devices",
            params=params,
            max_items=max_items
        )

    # https://{host}/proxy/network/integration/{version}/sites/{site_id}/clients
    def get_clients(self, site_id, max_items=None, filter=None):
        params = {}
        if filter:
            params["filter"] = filter

        return self._fetch_all_paginated(
            f"sites/{site_id}/clients",
            params=params,
            max_items=max_items
        )
