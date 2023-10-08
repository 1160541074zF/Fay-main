import sqlite3

# 连接到数据库（如果不存在，将创建一个新的数据库文件）
conn = sqlite3.connect('../gui/Ecarebot.db')

# 创建一个游标对象，用于执行SQL命令
cursor = conn.cursor()

# 创建表格用于存储记录
cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_recognition_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        user_id INTEGER,
        recognition_time TIMESTAMP
    )
''')

# 提交更改并关闭连接
conn.commit()
conn.close()
