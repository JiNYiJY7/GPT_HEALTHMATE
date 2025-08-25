import sqlite3
import hashlib
from datetime import datetime

def init_db():
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建聊天记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT,
            bot_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 创建症状记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS symptom_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptom TEXT NOT NULL,
            severity INTEGER,
            notes TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, email, password):
    from auth import hash_password
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    from auth import hash_password
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = c.fetchone()
    conn.close()
    
    if user and user[1] == hash_password(password):
        return user[0]  # 返回用户ID
    return None

def save_chat_history(user_id, user_message, bot_response):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)",
        (user_id, user_message, bot_response)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT user_message, bot_response, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    history = c.fetchall()
    conn.close()
    return history

def save_symptom_record(user_id, symptom, severity, notes):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO symptom_records (user_id, symptom, severity, notes) VALUES (?, ?, ?, ?)",
        (user_id, symptom, severity, notes)
    )
    conn.commit()
    conn.close()

def get_symptom_history(user_id, limit=10):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT symptom, severity, notes, recorded_at FROM symptom_records WHERE user_id = ? ORDER BY recorded_at DESC LIMIT ?",
        (user_id, limit)
    )
    history = c.fetchall()
    conn.close()
    return history