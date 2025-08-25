import re

def validate_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None

def validate_password(password):
    # 基本密码验证 - 至少8个字符
    return len(password) >= 8