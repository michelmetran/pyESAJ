"""
Módulo para definição de objetos
que serão obtidos na página de Gerenciamento de Perfis
Cadastro
"""

from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, field_validator


class Cadastro(BaseModel):
    """
    Objeto "Cadastro"
    """

    nome: str
    nome_social: Optional[str] = None
    email: EmailStr
    email_alternativo: Optional[EmailStr] = None
    cpf: str
    rg: Optional[str] = None
    rg_orgao_emissor: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    genero: Literal['Masculino', 'Feminino']

    @field_validator('*')
    def empty_str_to_none(cls, v):
        """
        Se o valor for '', converte para None
        https://github.com/pydantic/pydantic/discussions/2687
        """
        if v == '':
            return None
        return v


class Perfil(BaseModel):
    """
    Objeto "Perfil"
    """

    perfil: str
    autorizado: bool
    descricao: str
    observacao: Optional[str] = None


if __name__ == '__main__':
    perfil = Perfil(
        perfil='Distribuidor Intimações MP - Primeira Instância',
        autorizado=True,
        descricao='Este perfil permite que você tenha acesso aos serviços restritos do Portal e-SAJ, como Intimações Online e Consulta de Processos',
        observacao='Locais de atuação:\nTodos os Foros e Varas',
    )
    print(perfil)
    print(perfil.perfil)

    cad = Cadastro(
        nome='Michel Metran',
        genero='Masculino',
        email='michel@mail.com.br',
        cpf='meu cpf',
        rg='',
    )
    print(cad.email)
