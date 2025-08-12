import psycopg2

def check_database():
    try:
        conn = psycopg2.connect(
            user='postgres',
            password='logai',
            host='localhost',
            port='5432',
            database='log_analyzer'
        )
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM logs')
        total_count = cursor.fetchone()[0]
        print(f'Total logs in database: {total_count}')
        
        # Get count of new logs
        cursor.execute('''
            SELECT COUNT(*) FROM logs 
            WHERE device_name IN ('Workstation-05', 'Server-06', 'Laptop-05', 'Router-01', 'Firewall-01')
        ''')
        new_count = cursor.fetchone()[0]
        print(f'New logs from test: {new_count}')
        
        # Show some samples
        cursor.execute('''
            SELECT user_id, device_name, log, status, time 
            FROM logs 
            WHERE device_name IN ('Workstation-05', 'Server-06', 'Laptop-05', 'Router-01', 'Firewall-01')
            LIMIT 5
        ''')
        print("\nSample logs:")
        for row in cursor.fetchall():
            print(f"User: {row[0]}, Device: {row[1]}, Status: {row[3]}, Log: {row[2][:30]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    check_database() 