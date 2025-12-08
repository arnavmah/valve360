import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection string
DATABASE_URL = 'postgresql://neondb_owner:npg_tPbMCYj16Bry@ep-curly-math-a1qq5vqt-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

def explore_schema():
    """Explore database schema to find relevant tables"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all tables
        print("=" * 80)
        print("DATABASE TABLES")
        print("=" * 80)
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        for table in tables:
            table_name = table['table_name']
            print(f"\n📊 Table: {table_name}")
            
            # Get column information
            cur.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            
            print("   Columns:")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                print(f"   - {col['column_name']}: {col['data_type']} ({nullable})")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cur.fetchone()['count']
            print(f"   Total Records: {count}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_schema()
