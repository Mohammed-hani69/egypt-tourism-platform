from app import app, db
import sqlite3
import os
from models import User, Guide, LanguagePractice, ChatGroup, ChatGroupMember, ChatMessage, TourPlan, TourPlanDestination, TourBooking, TourProgress, TourPhoto

# Function to check if a column exists in a table
def column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns

# Function to check if a table exists in the database
def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

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
        if not table_exists(conn, 'user'):
            print("User table does not exist, skipping migration")
            conn.close()
            return
        
        # Check and add missing columns in user table
        if not column_exists(conn, 'user', 'is_tourist'):
            print("Adding 'is_tourist' column to User table")
            conn.execute('ALTER TABLE user ADD COLUMN is_tourist BOOLEAN DEFAULT 0')
        
        if not column_exists(conn, 'user', 'is_admin'):
            print("Adding 'is_admin' column to User table")
            conn.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
            
        # Check for language_practice table
        if table_exists(conn, 'language_practice'):
            # Check for guide_id column in language_practice table
            if not column_exists(conn, 'language_practice', 'guide_id'):
                print("Adding 'guide_id' column to LanguagePractice table")
                conn.execute('ALTER TABLE language_practice ADD COLUMN guide_id INTEGER')
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print("Database migration complete!")
    except Exception as e:
        print(f"Error during database update: {e}")

# Function to recreate tables with integrity issues
def full_db_setup():
    print("إعداد هيكل قاعدة البيانات الكامل...")
    with app.app_context():
        # إنشاء مجلد instance إذا لم يكن موجودًا
        import os
        if not os.path.exists('instance'):
            os.makedirs('instance')
            
        # حذف وإعادة إنشاء جميع الجداول
        db.drop_all()
        db.create_all()
        print("تم إعادة إنشاء جميع جداول قاعدة البيانات!")

# Run the script
if __name__ == "__main__":
    with app.app_context():
        try:
            # First try to update existing database
            update_database()
            
            # Create all tables that don't exist yet
            db.create_all()
            print("All tables created/updated!")
            
            # Get argument for full reset if provided
            import sys
            if len(sys.argv) > 1 and sys.argv[1] == '--reset':
                print("Performing full database reset...")
                full_db_setup()
                
        except Exception as e:
            print(f"Error during database update: {e}")