import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secure_postgres_password@localhost:5432/green_gold")


class SupabaseUploader:
    """Direct PostgreSQL/Supabase Uploader with smart fallback."""
    
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(DATABASE_URL)
            self.conn.autocommit = True
            print("✅ Connected to PostgreSQL/Supabase successfully")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")
            print("   Data will be printed to console only.")
    
    def upload_round(self, round_data: dict) -> bool:
        if not self.conn:
            print(f"📊 [LOCAL] Round: {round_data.get('round_id')} -> {round_data.get('multiplier')}x")
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO rounds (round_id, multiplier, source)
                VALUES (%s, %s, %s)
                ON CONFLICT (round_id) DO NOTHING
                """,
                (
                    round_data.get("round_id"),
                    round_data.get("multiplier"),
                    round_data.get("source", "collector")
                )
            )
            cursor.close()
            print(f"✅ Uploaded: {round_data.get('round_id')} -> {round_data.get('multiplier')}x")
            return True
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
