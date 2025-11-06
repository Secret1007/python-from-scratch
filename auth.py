from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWT 配置
SECRET_KEY = "your-secret-key-here-change-in-production"  # 密钥（生产环境要改成随机的）
ALGORITHM = "HS256"  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token 过期时间（30分钟）

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None