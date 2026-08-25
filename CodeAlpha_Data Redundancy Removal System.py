import sqlite3

class DataRedundancySystem:
    def __init__(self, db_name="cloud_database.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initializes the SQLite cloud database table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_key TEXT UNIQUE,
                payload TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def check_redundancy(self, data_key):
        """Checks if the data key already exists in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records WHERE data_key = ?", (data_key,))
        row = cursor.fetchone()
        conn.close()
        return row is not None  # True if redundant, False if unique

    def add_data(self, data_key, payload):
        """Validates and appends only unique, verified data entries."""
        if self.check_redundancy(data_key):
            print(f"❌ Redundant Data Detected: '{data_key}' already exists. Skipping insertion.")
            return False
        
        # Validation mechanism passed, append to database
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO records (data_key, payload, status) VALUES (?, ?, ?)", 
                           (data_key, payload, "Verified"))
            conn.commit()
            conn.close()
            print(f"✅ Success: Unique data entry '{data_key}' added to the cloud database.")
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False

# --- Testing the System ---
if __name__ == "__main__":
    db_system = DataRedundancySystem()

    # Simulating data entries
    db_system.add_data("user_101", "Sensor Data A")
    db_system.add_data("user_102", "Sensor Data B")
    
    # Trying to insert duplicate data
    db_system.add_data("user_101", "Duplicate Sensor Data A")