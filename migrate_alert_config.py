"""
迁移脚本：调整预警配置字段
- 新增 alert_sterilization_remaining（剩余灭菌次数预警）
- 废弃 alert_usage_ratio 和 alert_sterilization_ratio（代码中不再使用）
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'filter_mgmt.db')


def migrate():
    if not os.path.exists(DB_PATH):
        print(f'数据库不存在: {DB_PATH}')
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查当前表结构
    cursor.execute("PRAGMA table_info(configs)")
    columns = {row[1] for row in cursor.fetchall()}

    # 添加新列（如果不存在）
    if 'alert_sterilization_remaining' not in columns:
        print('添加列: alert_sterilization_remaining')
        cursor.execute(
            "ALTER TABLE configs ADD COLUMN alert_sterilization_remaining INTEGER DEFAULT 0"
        )
    else:
        print('列 alert_sterilization_remaining 已存在，跳过')

    conn.commit()
    conn.close()
    print('迁移完成')


if __name__ == '__main__':
    migrate()
