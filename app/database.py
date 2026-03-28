import requests
from .config import Config

class SupabaseClient:
    """Direct REST API client for Supabase"""
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.base_url = f"{url}/rest/v1"
        self.headers = {
            "apikey": key,
            "Content-Type": "application/json"
        }

    def table(self, name: str):
        return SupabaseTable(self.base_url, self.headers, name)


class SupabaseTable:
    """Helper for Supabase table operations"""
    def __init__(self, base_url: str, headers: dict, table_name: str):
        self.base_url = base_url
        self.headers = headers
        self.table_name = table_name
        self.url = f"{base_url}/{table_name}"
        self._select = "*"
        self._filters = {}
        self._order = None
        self._limit_val = None
        self._operation = "select"
        self._data = None

    def select(self, columns: str = "*"):
        self._select = columns
        return self

    def eq(self, column: str, value):
        self._filters[column] = f"eq.{value}"
        return self

    def neq(self, column: str, value):
        self._filters[column] = f"neq.{value}"
        return self

    def lt(self, column: str, value):
        self._filters[column] = f"lt.{value}"
        return self

    def order(self, column: str, desc: bool = False):
        self._order = f"{column}.{'desc' if desc else 'asc'}"
        return self

    def limit(self, n: int):
        self._limit_val = n
        return self

    def single(self):
        self._limit_val = 1
        return self

    def insert(self, data: dict):
        self._data = data
        self._operation = "insert"
        return self

    def update(self, data: dict):
        self._data = data
        self._operation = "update"
        return self

    def delete(self):
        self._operation = "delete"
        return self

    def execute(self):
        try:
            if self._operation == "insert":
                response = requests.post(self.url, headers=self.headers, json=self._data)
                response.raise_for_status()
                return SupabaseResponse(response.json())

            elif self._operation == "update":
                filter_str = "&".join([f"{k}={v}" for k, v in self._filters.items()])
                url = f"{self.url}?{filter_str}" if filter_str else self.url
                response = requests.patch(url, headers=self.headers, json=self._data)
                response.raise_for_status()
                return SupabaseResponse(response.json())

            elif self._operation == "delete":
                filter_str = "&".join([f"{k}={v}" for k, v in self._filters.items()])
                url = f"{self.url}?{filter_str}" if filter_str else self.url
                response = requests.delete(url, headers=self.headers)
                response.raise_for_status()
                return SupabaseResponse([])

            else:  # SELECT
                params = []
                # Only add select if it's not the default *
                if self._select != "*":
                    params.append(f"select={self._select}")

                # Add filters
                for k, v in self._filters.items():
                    params.append(f"{k}={v}")

                # Add order
                if self._order:
                    params.append(f"order={self._order}")

                # Add limit
                if self._limit_val:
                    params.append(f"limit={self._limit_val}")

                query_str = "&".join(params)
                url = f"{self.url}?{query_str}" if query_str else self.url

                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()

                if self._limit_val == 1 and isinstance(data, list):
                    return SupabaseResponse(data[0] if data else None)
                return SupabaseResponse(data if isinstance(data, list) else [data])

        except requests.exceptions.RequestException as e:
            raise Exception(f"Supabase error: {e}")


class SupabaseResponse:
    """Response wrapper"""
    def __init__(self, data):
        self.data = data


_client = None

def get_client():
    """Get Supabase client singleton"""
    global _client
    if _client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        _client = SupabaseClient(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _client

get_db = get_client

