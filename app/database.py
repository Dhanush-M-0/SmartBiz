from supabase import create_client, Client
from .config import Config

_client: Client = None

def get_client() -> Client:
    """Return a singleton Supabase client."""
    global _client
    if _client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in your .env file.")
        _client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _client

# Alias for compatibility
get_db = get_client
