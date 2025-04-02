"""
Módulo para definição de objetos
que serão os parâmetros de output
das pesquisas na seção de Intimações

Trata-se da representação dos registros
da tabela que aparece no e-SAJ
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# TODO: Mapear as tarjas
class RecebimentoIntimacoes1Grau(BaseModel):
    """
    Objeto "Intimações" de 1º Grau.

    Muito similar às Intimações de 2º Grau,
    sendo que a única diferença é que existe
    "foro" ao invés de "seção".
    """

    disponibilizacao: Optional[str] = None
    prazo_processual: Optional[int] = None
    numero_processo: Optional[str] = None
    classe_assunto_principal: Optional[str] = None
    movimentacao: Optional[str] = None
    foro: Optional[str] = None
    vara: Optional[str] = None
    especializacao: Optional[str] = None
    cargo: Optional[str] = None

    @field_validator('*')
    def empty_str_to_none(cls, v):
        """
        Se o valor for '', converte para None
        https://github.com/pydantic/pydantic/discussions/2687
        """
        if v == '':
            return None
        return v

    @field_validator('disponibilizacao')
    def convert_to_date(cls, v):
        """
        Converte para datetime, isoformat
        """
        if v == '':
            return None
        return datetime.strptime(v, '%d/%m/%Y').date().isoformat()


class RecebimentoIntimacoes2Grau(BaseModel):
    """
    Objeto "Intimações" de 2º Grau ou Turmas Recursais.

    Muito similar às Intimações de 1º Grau,
    sendo que a única diferença é que existe
    "seção" e "órgão julgador" ao invés de "foro" e "vara".
    """

    disponibilizacao: Optional[str] = date
    prazo_processual: Optional[int] = None
    numero_processo: Optional[str] = None
    classe_assunto_principal: Optional[str] = None
    movimentacao: Optional[str] = None
    secao: Optional[str] = None
    orgao_julgador: Optional[str] = None
    especializacao: Optional[str] = None
    cargo: Optional[str] = None

    @field_validator('*')
    def empty_str_to_none(cls, v):
        """
        Se o valor for '', converte para None
        https://github.com/pydantic/pydantic/discussions/2687
        """
        if v == '':
            return None
        return v

    @field_validator('disponibilizacao')
    def convert_to_date(cls, v):
        """
        Converte para datetime, iso format
        """
        if v == '':
            return None
        return datetime.strptime(v, '%d/%m/%Y').date().isoformat()


class ConsultaIntimacoes2Grau(BaseModel):
    """
    Objeto "Intimações" de 2º Grau ou Turmas Recursais.

    Muito similar às Intimações de 1º Grau,
    sendo que a única diferença é que existe
    "seção" e "órgão julgador" ao invés de "foro" e "vara".

    Utilizado nas Consultas
    """

    disponibilizacao: Optional[str] = date
    data_intimacao: Optional[str] = date
    prazo_processual: Optional[int] = None
    numero_processo: Optional[str] = None
    classe_assunto_principal: Optional[str] = None
    recebido_por: Optional[str] = None
    movimentacao: Optional[str] = None
    # secao: Optional[str] = None
    # orgao_julgador: Optional[str] = None
    especializacao: Optional[str] = None
    cargo: Optional[str] = None

    @field_validator('*')
    def empty_str_to_none(cls, v):
        """
        Se o valor for '', converte para None
        https://github.com/pydantic/pydantic/discussions/2687
        """
        if v == '':
            return None
        return v

    @field_validator('disponibilizacao', 'data_intimacao')
    def convert_to_date(cls, v):
        """
        Converte para datetime, iso format
        """
        if v == '':
            return None

        # É possível que, no menu Consultas, tenham processos sem registro da data de intimação
        # Nessa situação, vem "None"
        elif v is None:
            return None

        return datetime.strptime(v, '%d/%m/%Y').date().isoformat()
        # return datetime.strptime(v, '%d/%m/%Y').date().norma


if __name__ == '__main__':
    # intim = RecebimentoIntimacoes2Grau(
    #     disponibilizacao='24/09/2024',
    #     prazo_processual='2° Grau',
    #     numero_processo='Criminal',
    #     classe_assunto_principal='False',
    #     movimentacao='False',
    #     especializacao='False',
    #     cargo='Ambas',
    # )
    # print(intim)
    # print(intim.disponibilizacao, type(intim.disponibilizacao))

    intim = ConsultaIntimacoes2Grau(
        disponibilizacao='24/09/2024',
        # data_intimacao='24/11/2024',
        data_intimacao=None,
        prazo_processual=10,
        numero_processo='2336412-80.2024.8.26.0000',
        classe_assunto_principal='Revisão Criminal / Roubo Majorado',
        movimentacao='Parecer - Prazo - 10 Dias',
        especializacao='Criminal',
        cargo='020º PROCURADOR DE JUSTIÇA',
    )
    print(intim)
    print(intim.disponibilizacao, type(intim.disponibilizacao))
