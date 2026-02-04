"""
Rotas de Contas (CRUD Completo)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.conta import Conta
from app.schemas.schemas import ContaCreate, ContaUpdate, ContaResponse, MessageResponse

router = APIRouter(prefix="/contas", tags=["Contas"])


@router.get("/", response_model=List[ContaResponse])
def list_contas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todas as contas do usuário autenticado (READ)
    """
    print(f"✅ GET /contas - Usuário autenticado: {current_user.email}")
    contas = db.query(Conta).filter(
        Conta.id_usuario == current_user.id_usuario
    ).offset(skip).limit(limit).all()
    print(f"✅ Retornando {len(contas)} contas")
    return contas


@router.get("/{id_conta}", response_model=ContaResponse)
def get_conta(
    id_conta: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Busca conta por ID (READ)
    Apenas contas do usuário autenticado
    """
    conta = db.query(Conta).filter(
        Conta.id_conta == id_conta,
        Conta.id_usuario == current_user.id_usuario
    ).first()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conta com ID {id_conta} não encontrada"
        )
    return conta


@router.post("/", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
def create_conta(
    conta_data: ContaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria nova conta (CREATE)
    Requer autenticação JWT
    """
    try:
        # Validação: verifica se já existe conta com mesmo nome para este usuário
        conta_existente = db.query(Conta).filter(
            Conta.nome == conta_data.nome,
            Conta.id_usuario == current_user.id_usuario
        ).first()
        
        if conta_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe uma conta com o nome '{conta_data.nome}'"
            )
        
        # Validação: verifica se o tipo é válido
        tipos_validos = ["corrente", "poupanca", "investimento", "digital", "carteira"]
        if conta_data.tipo.lower() not in tipos_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo inválido. Use um dos seguintes: {', '.join(tipos_validos)}"
            )
        
        # Cria nova conta associada ao usuário autenticado
        new_conta = Conta(
            nome=conta_data.nome,
            saldo=conta_data.saldo_inicial,
            tipo=conta_data.tipo.lower(),
            id_usuario=current_user.id_usuario
        )
        
        db.add(new_conta)
        db.commit()
        db.refresh(new_conta)
        
        print(f"✅ Conta '{new_conta.nome}' criada com sucesso para usuário {current_user.email}")
        
        return new_conta
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar conta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.put("/{id_conta}", response_model=ContaResponse)
def update_conta(
    id_conta: int,
    conta_data: ContaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza conta existente (UPDATE)
    Requer autenticação JWT
    """
    conta = db.query(Conta).filter(
        Conta.id_conta == id_conta,
        Conta.id_usuario == current_user.id_usuario
    ).first()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conta com ID {id_conta} não encontrada"
        )
    
    # Atualiza apenas campos fornecidos
    update_data = conta_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(conta, field, value)
    
    db.commit()
    db.refresh(conta)
    
    return conta


@router.delete("/{id_conta}", response_model=MessageResponse)
def delete_conta(
    id_conta: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deleta conta (DELETE)
    Requer autenticação JWT
    """
    conta = db.query(Conta).filter(
        Conta.id_conta == id_conta,
        Conta.id_usuario == current_user.id_usuario
    ).first()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conta com ID {id_conta} não encontrada"
        )
    
    db.delete(conta)
    db.commit()
    
    return {
        "message": "Conta deletada com sucesso",
        "detail": f"Conta {conta.nome} (ID: {id_conta}) foi removida"
    }