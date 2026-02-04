"""
Schemas Pydantic para validacao e serializacao de dados
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date


# ============================================================================
# SCHEMAS DE USUARIO
# ============================================================================

class UsuarioBase(BaseModel):
    """Schema base para usuario"""
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """Schema para criacao de usuario"""
    senha: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    """Schema para atualizacao de usuario"""
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6)


class UsuarioResponse(UsuarioBase):
    """Schema de resposta de usuario"""
    id_usuario: int
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE AUTENTICACAO
# ============================================================================

class Token(BaseModel):
    """Schema de resposta do token"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema de requisicao de login"""
    email: str
    senha: str


# ============================================================================
# SCHEMAS DE CONTA
# ============================================================================

class ContaBase(BaseModel):
    """Schema base para conta"""
    nome: str = Field(..., min_length=1, max_length=100)
    tipo: str = Field(..., min_length=1, max_length=50)
    saldo_inicial: float = Field(default=0.0, ge=0)


class ContaCreate(BaseModel):
    """Schema para criacao de conta"""
    nome: str = Field(..., min_length=1, max_length=100)
    tipo: str = Field(..., min_length=1, max_length=50)
    saldo_inicial: float = Field(default=0.0, ge=0)


class ContaUpdate(BaseModel):
    """Schema para atualizacao de conta"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)


class ContaResponse(BaseModel):
    """Schema de resposta de conta"""
    id_conta: int
    id_usuario: int
    nome: str
    tipo: str
    saldo: float
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE CATEGORIA
# ============================================================================

class CategoriaBase(BaseModel):
    """Schema base para categoria"""
    nome: str = Field(..., min_length=1, max_length=100)
    tipo: str = Field(..., min_length=1, max_length=50)


class CategoriaCreate(CategoriaBase):
    """Schema para criacao de categoria"""
    pass


class CategoriaUpdate(BaseModel):
    """Schema para atualizacao de categoria"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)


class CategoriaResponse(CategoriaBase):
    """Schema de resposta de categoria"""
    id_categoria: int
    id_usuario: int
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE TRANSACAO
# ============================================================================

class TransacaoBase(BaseModel):
    """Schema base para transacao"""
    descricao: str = Field(..., min_length=1, max_length=200)
    valor: float = Field(..., gt=0)
    tipo: str = Field(..., min_length=1, max_length=50)


class TransacaoCreate(TransacaoBase):
    """Schema para criacao de transacao"""
    id_conta: int
    id_categoria: int
    data: Optional[date] = None


class TransacaoUpdate(BaseModel):
    """Schema para atualizacao de transacao"""
    descricao: Optional[str] = Field(None, min_length=1, max_length=200)
    valor: Optional[float] = Field(None, gt=0)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    id_categoria: Optional[int] = None


class TransacaoResponse(TransacaoBase):
    """Schema de resposta de transacao"""
    id_transacao: int
    id_conta: int
    id_categoria: int
    id_usuario: int
    data: date
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE RESPOSTA GENERICOS
# ============================================================================

class MessageResponse(BaseModel):
    """Schema para mensagens de resposta"""
    message: str
    detail: Optional[str] = None
