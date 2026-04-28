import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查列是否已存在
cursor.execute("PRAGMA table_info(filters)")
columns = [row[1] for row in cursor.fetchall()]

if 'is_usage_record' not in columns:
    cursor.execute("ALTER TABLE filters ADD COLUMN is_usage_record BOOLEAN DEFAULT 0")
    print("Added column: is_usage_record")
else:
    print("Column is_usage_record already exists")

# 将已有使用信息的记录标记为 usage_record
# 导入的数据通常没有 use_location / operator / receivers
cursor.execute("""
    UPDATE filters 
    SET is_usage_record = 1 
    WHERE use_location IS NOT NULL AND use_location != ''
       OR operator IS NOT NULL AND operator != ''
       OR receivers IS NOT NULL AND receivers != ''
""")
print(f"Updated {cursor.rowcount} existing records to is_usage_record=1")

conn.commit()
conn.close()
print("Migration completed.")
