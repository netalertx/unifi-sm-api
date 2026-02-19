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

        Returns full response structure for backward compatibility.
        """
        if params is None:
            params = {}

        offset = 0
        results = []
        total = 0

        while True:
            query = {
                **params,
                "offset": offset,
                "limit": page_size,
            }

            resp = self._request("GET", endpoint, params=query)

            data = resp.get("data", [])
            count = resp.get("count", len(data))
            total = resp.get("totalCount", total)

            if not data:
                break

            results.extend(data)

            # Stop if we've reached max_items
            if max_items is not None and len(results) >= max_items:
                results = results[:max_items]
                break

            offset += count

            # Stop if we've fetched everything
            if total and offset >= total:
                break

        return {
            "data": results,
            "count": len(results),
            "totalCount": total,
            "offset": 0,
            "limit": len(results),
        }

    # https://{host}/proxy/network/integration/{version}/sites
    def get_sites(self):
        return self._request("GET", "sites")

    # https://{host}/proxy/network/integration/{version}/sites/{site_id}/devices
    def get_unifi_devices(self, site_id, max_items=None, filter=None, as_list=False):
        params = {}
        if filter:
            params["filter"] = filter

        resp = self._fetch_all_paginated(
            f"sites/{site_id}/devices",
            params=params,
            max_items=max_items
        )

        return resp["data"] if as_list else resp

    # https://{host}/proxy/network/integration/{version}/sites/{site_id}/clients
    def get_clients(self, site_id, max_items=None, filter=None, as_list=False):
        params = {}
        if filter:
            params["filter"] = filter

        resp = self._fetch_all_paginated(
            f"sites/{site_id}/clients",
            params=params,
            max_items=max_items
        )

        return resp["data"] if as_list else resp
