"""
Módulo de Segurança e Autenticação - VERSÃO SIMPLIFICADA
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import hashlib

from app.core.database import get_db, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.usuario import Usuario

# Security scheme para JWT
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash usando SHA256"""
    return hash_password(plain_password) == hashed_password


def hash_password(password: str) -> str:
    """
    Gera hash da senha usando SHA256 (simples e sem limite de tamanho)
    """
    # Usa SHA256 em vez de bcrypt para evitar problemas de tamanho
    return hashlib.sha256(password.encode()).hexdigest()


def get_password_hash(password: str) -> str:
    """Alias para hash_password"""
    return hash_password(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtém usuário atual do token JWT"""
    print(f"🔐 get_current_user() chamado")
    print(f"🔐 Credentials recebidas: scheme={credentials.scheme}, token_prefix={credentials.credentials[:20]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        print(f"🔐 Decodificando token com SECRET_KEY: {SECRET_KEY[:10]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔐 Token decodificado com sucesso: {payload}")
        email: str = payload.get("sub")
        if email is None:
            print(f"❌ Email não encontrado no payload")
            raise credentials_exception
        print(f"✅ Email extraído: {email}")
    except InvalidTokenError as e:
        print(f"❌ InvalidTokenError: {e}")
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        print(f"❌ Usuário {email} não encontrado no banco")
        raise credentials_exception
    
    print(f"✅ Usuário encontrado: {user.email}")
    return user