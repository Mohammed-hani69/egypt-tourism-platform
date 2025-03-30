from app import app, db
import sqlite3
import os

# Function to check if a column exists in a table
def column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns

# Main function to update the database
def update_database():
    # Get the database path from app config
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    
    # Only proceed if using SQLite
    if not db_uri.startswith('sqlite:///'):
        print(f"Database is not SQLite, it's: {db_uri}")
        return
    
    # Extract the path from the URI
    db_path = db_uri.replace('sqlite:///', '')
    
    # For relative paths in the URI
    if not os.path.isabs(db_path):
        db_path = os.path.join(app.instance_path, db_path)
    
    print(f"Using database at: {db_path}")
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        print(f"Database file does not exist at {db_path}")
        return
    
    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        
        # Check if user table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if not cursor.fetchone():
            print("User table does not exist, skipping migration")
            conn.close()
            return
        
        # Check and add missing columns
        if not column_exists(conn, 'user', 'is_tourist'):
            print("Adding 'is_tourist' column to User table")
            conn.execute('ALTER TABLE user ADD COLUMN is_tourist BOOLEAN DEFAULT 0')
        
        if not column_exists(conn, 'user', 'is_admin'):
            print("Adding 'is_admin' column to User table")
            conn.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print("Database migration complete!")
    except Exception as e:
        print(f"Error connecting to database: {e}")

# Run the script
if __name__ == "__main__":
    with app.app_context():
        try:
            update_database()
            # Create all tables (this will create missing tables without affecting existing ones)
            db.create_all()
            print("All tables created/updated!")
        except Exception as e:
            print(f"Error during database update: {e}")