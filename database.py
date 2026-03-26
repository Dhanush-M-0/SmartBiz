from supabase import create_client, Client
from config import Config
import logging

logger = logging.getLogger(__name__)

class SupabaseDB:
    """Supabase database connection handler"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            try:
                self.supabase: Client = create_client(
                    Config.SUPABASE_URL,
                    Config.SUPABASE_KEY
                )
                self._initialized = True
                logger.info("✓ Connected to Supabase")
            except Exception as e:
                logger.error(f"✗ Failed to connect to Supabase: {str(e)}")
                raise
    
    def get_client(self):
        """Return the Supabase client"""
        return self.supabase
    
    def health_check(self):
        """Check if database connection is alive"""
        try:
            result = self.supabase.table('employees').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False

# Initialize database connection
db = SupabaseDB()

def get_db():
    """Get database instance"""
    return db.get_client()
