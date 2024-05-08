import sqlite3

def create_or_open_database(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn

def insert_user(conn, name, age):
    """在表中插入一条新用户记录"""
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    return c.lastrowid  # 返回新插入记录的ID

db_path = 'example.db'

# 确保数据库和表存在
conn = create_or_open_database(db_path)

# 插入新用户记录
user_id = insert_user(conn, 'John Doe', 28)
print(f"Inserted user with ID: {user_id}")

# 关闭数据库连接
conn.close()
