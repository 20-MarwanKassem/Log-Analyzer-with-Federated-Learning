import psycopg2
import os

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER', 'postgres'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'log_analyzer'),
    'password': os.environ.get('DB_PASSWORD', 'logai'),
    'port': os.environ.get('DB_PORT', '5432'),
}

try:
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Get the exact structure of the logs table
    cur.execute("""
        SELECT column_name, data_type, column_default
        FROM information_schema.columns
        WHERE table_name = 'logs'
        ORDER BY ordinal_position;
    """)
    
    columns = cur.fetchall()
    
    print("=== LOGS TABLE STRUCTURE ===")
    for col in columns:
        print(f"Column: {col[0]}, Type: {col[1]}, Default: {col[2]}")

    # Check for primary key
    cur.execute("""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                            AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = 'logs'::regclass
        AND    i.indisprimary;
    """)
    
    pk_columns = cur.fetchall()
    
    print("\n=== PRIMARY KEY ===")
    for pk in pk_columns:
        print(f"Primary key column: {pk[0]}")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")