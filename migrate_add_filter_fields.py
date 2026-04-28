import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查列是否已存在
cursor.execute("PRAGMA table_info(filters)")
columns = [row[1] for row in cursor.fetchall()]

if 'use_process_name' not in columns:
    cursor.execute("ALTER TABLE filters ADD COLUMN use_process_name VARCHAR(100)")
    print("Added column: use_process_name")
else:
    print("Column use_process_name already exists")

if 'record_max_sterilization' not in columns:
    cursor.execute("ALTER TABLE filters ADD COLUMN record_max_sterilization INTEGER")
    print("Added column: record_max_sterilization")
else:
    print("Column record_max_sterilization already exists")

conn.commit()
conn.close()
print("Migration completed.")
