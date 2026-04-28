import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(configs)")
columns = {row[1]: row for row in cursor.fetchall()}

# 添加新列
new_columns = {
    'alert_push_enabled': 'BOOLEAN DEFAULT 0',
    'alert_push_time': 'VARCHAR(10) DEFAULT \'08:00\'',
    'alert_push_receivers': 'VARCHAR(500) DEFAULT \'\''
}

for col_name, col_def in new_columns.items():
    if col_name not in columns:
        cursor.execute(f"ALTER TABLE configs ADD COLUMN {col_name} {col_def}")
        print(f"Added column: {col_name}")
    else:
        print(f"Column {col_name} already exists")

# 如果有旧的 auto_push_enabled 数据，迁移到新字段
if 'auto_push_enabled' in columns:
    cursor.execute("UPDATE configs SET alert_push_enabled = auto_push_enabled WHERE alert_push_enabled IS NULL")
    print("Migrated auto_push_enabled to alert_push_enabled")

if 'auto_push_time' in columns:
    cursor.execute("UPDATE configs SET alert_push_time = auto_push_time WHERE alert_push_time IS NULL OR alert_push_time = ''")
    print("Migrated auto_push_time to alert_push_time")

conn.commit()
conn.close()
print("Migration completed.")
