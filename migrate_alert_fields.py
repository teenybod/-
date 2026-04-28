import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(filters)")
columns = [row[1] for row in cursor.fetchall()]

if 'last_sterilization_alert_at' not in columns:
    cursor.execute("ALTER TABLE filters ADD COLUMN last_sterilization_alert_at DATETIME")
    print("Added column: last_sterilization_alert_at")
else:
    print("Column last_sterilization_alert_at already exists")

if 'last_expiry_alert_at' not in columns:
    cursor.execute("ALTER TABLE filters ADD COLUMN last_expiry_alert_at DATETIME")
    print("Added column: last_expiry_alert_at")
else:
    print("Column last_expiry_alert_at already exists")

conn.commit()
conn.close()
print("Migration completed.")
