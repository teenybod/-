import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# filter_models 表
for col_name, col_type in [
    ('updated_at', 'DATETIME'),
    ('unit', 'VARCHAR(50)'),
    ('supplier', 'VARCHAR(200)'),
    ('feishu_record_id', 'VARCHAR(100)'),
]:
    cursor.execute("PRAGMA table_info(filter_models)")
    columns = [row[1] for row in cursor.fetchall()]
    if col_name not in columns:
        cursor.execute(f"ALTER TABLE filter_models ADD COLUMN {col_name} {col_type}")
        print(f"Added column to filter_models: {col_name}")
    else:
        print(f"Column {col_name} already exists in filter_models")

# filters 表
for col_name, col_type in [
    ('updated_at', 'DATETIME'),
    ('feishu_record_id', 'VARCHAR(100)'),
]:
    cursor.execute("PRAGMA table_info(filters)")
    columns = [row[1] for row in cursor.fetchall()]
    if col_name not in columns:
        cursor.execute(f"ALTER TABLE filters ADD COLUMN {col_name} {col_type}")
        print(f"Added column to filters: {col_name}")
    else:
        print(f"Column {col_name} already exists in filters")

# configs 表
for col_name, col_type in [
    ('feishu_bitable_app_token', 'VARCHAR(100)'),
    ('feishu_bitable_table_id', 'VARCHAR(100)'),
    ('feishu_bitable_sync_enabled', 'BOOLEAN'),
    ('feishu_bitable_sync_interval', 'INTEGER'),
]:
    cursor.execute("PRAGMA table_info(configs)")
    columns = [row[1] for row in cursor.fetchall()]
    if col_name not in columns:
        cursor.execute(f"ALTER TABLE configs ADD COLUMN {col_name} {col_type}")
        print(f"Added column to configs: {col_name}")
    else:
        print(f"Column {col_name} already exists in configs")

conn.commit()
conn.close()
print("Migration completed.")
