"""
Módulo para definição de objetos
que serão os parâmetros de input
das pesquisas na seção de Intimações

TODO: Avaliar o uso
https://stackoverflow.com/questions/76537360/initialize-one-of-two-pydantic-models-depending-on-an-init-parameter
"""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class RecebeIntimacoes(BaseModel):
    """
    Parâmetros de pesquisa de Intimações das instâncias do tipo:
    - 1º Grau
    - 2º Grau
    - Turmas Recursais
    """

    # TODO: Fazer com que seja possível definir a classe programaticamente.
    em_nome_de: Literal['Ministério Público do Estado de São Paulo', 'Outros']
    tipo_participacao: Optional[str] = None
    instancia: Literal['Primeiro Grau', 'Segundo Grau', 'Turmas Recursais']

    # TODO: Não pode marcar Vara se não marcar Foro
    foro: Optional[str] = None  # Exclusivo 1° Grau
    vara: Optional[str] = None  # Exclusivo 1° Grau

    # TODO: Não pode marcar Órgão Julgador se não marcar Seção
    secao: Optional[str] = None  # Exclusivo 2° Grau
    orgao_julgador: Optional[str] = None  # Exclusivo 2° Grau

    especializacao: Optional[str] = None
    especializacao_nao_definida: Optional[bool] = False
    cargo: Optional[str] = None
    cargo_nao_definido: Optional[bool] = False
    classe: Optional[str] = None  # Exclusivo 2° Grau
    assunto_principal: Optional[str] = None  # Exclusivo 2° Grau
    area: Literal['Ambas', 'Cível', 'Criminal']
    processo: Optional[str] = None
    natureza_comunicacao: Literal['Intimação', 'Citação', 'Ambas']

    @model_validator(mode='after')
    def check_especializacao(self):
        """
        Precisa ter "Especialização" ou
        "Especialização Não Definida".

        Não pode ter os dois!

        https://github.com/pydantic/pydantic/issues/506
        """
        if self.especializacao and self.especializacao_nao_definida:
            raise ValueError(
                'Foram definidas as variáveis "Especialização" e "Especialização não Definida" como "True".\n'
                'Só pode ser definida uma dessas duas variáveis ou definir como "False".'
            )
        return self

    @model_validator(mode='after')
    def check_cargo(self):
        """
        Precisa ter "Especialização" ou
        "Especialização Não Definida".

        Não pode ter os dois!

        https://github.com/pydantic/pydantic/issues/506
        """
        if self.cargo and self.cargo_nao_definido:
            raise ValueError(
                'Foram definidas as variáveis "Cargo" e "Cargo não Definido" como "True".\n'
                'Só pode ser definida uma dessas duas variáveis ou definir como "False".'
            )
        return self

    @field_validator('foro', 'vara', check_fields=False)
    def set_none(cls, v, info: ValidationInfo):
        """
        Define "None" caso seja de 2º grau
        """
        if info.data['instancia'] in ('Segundo Grau', 'Turmas Recursais'):
            return None
        return v

    @field_validator(
        'secao',
        'orgao_julgador',
        'classe',
        'assunto',
        'area',
        check_fields=False,
    )
    def set_none_2(cls, v, info: ValidationInfo):
        """
        Define "None" caso seja de 1° grau
        """
        if info.data['instancia'] == 'Primeiro Grau':
            return None
        return v


class ConsultaIntimacoes(BaseModel):
    """
    Parâmetros de pesquisa de Intimações das instâncias do tipo:
    - 1º Grau
    - 2º Grau
    - Turmas Recursais
    """

    # TODO: Fazer com que seja possível definir a classe programaticamente.
    em_nome_de: Literal['Ministério Público do Estado de São Paulo', 'Outros']
    tipo_participacao: Optional[str] = None
    instancia: Literal['Primeiro Grau', 'Segundo Grau', 'Turmas Recursais']

    # TODO: Não pode marcar Vara se não marcar Foro
    foro: Optional[str] = None  # Exclusivo 1° Grau
    vara: Optional[str] = None  # Exclusivo 1° Grau

    # TODO: Não pode marcar Órgão Julgador se não marcar Seção
    secao: Optional[str] = None  # Exclusivo 2° Grau
    orgao_julgador: Optional[str] = None  # Exclusivo 2° Grau

    especializacao: Optional[str] = None
    especializacao_nao_definida: Optional[bool] = False
    cargo: Optional[str] = None
    cargo_nao_definido: Optional[bool] = False
    classe: Optional[str] = None  # Exclusivo 2° Grau
    assunto_principal: Optional[str] = None  # Exclusivo 2° Grau
    area: Literal['Ambas', 'Cível', 'Criminal']
    periodo_de: Optional[date] = None
    periodo_ate: Optional[date] = None
    processo: Optional[str] = None
    ciencia_ato: Literal['Todos', 'Automática', 'Portal']
    natureza_comunicacao: Literal['Intimação', 'Citação', 'Ambas']
    situacao: Literal['Cumprida', 'Pendente', 'Ambas']

    @model_validator(mode='after')
    def check_especializacao(self):
        """
        Precisa ter "Especialização" ou
        "Especialização Não Definida".

        Não pode ter os dois!

        https://github.com/pydantic/pydantic/issues/506
        """
        if self.especializacao and self.especializacao_nao_definida:
            raise ValueError(
                'Foram definidas as variáveis "Especialização" e "Especialização não Definida" como "True".\n'
                'Só pode ser definida uma dessas duas variáveis ou definir como "False".'
            )
        return self

    @model_validator(mode='after')
    def check_cargo(self):
        """
        Precisa ter "Cargo" ou
        "Cargo Não Definido".

        Não pode ter os dois!

        https://github.com/pydantic/pydantic/issues/506
        """
        if self.cargo and self.cargo_nao_definido:
            raise ValueError(
                'Foram definidas as variáveis "Cargo" e "Cargo não Definido" como "True".\n'
                'Só pode ser definida uma dessas duas variáveis ou definir como "False".'
            )
        return self

    @field_validator('foro', 'vara', check_fields=False)
    def set_none(cls, v, info: ValidationInfo):
        """
        Define "None" caso seja de 2º grau
        """
        if info.data['instancia'] in ('Segundo Grau', 'Turmas Recursais'):
            return None
        return v

    @field_validator(
        'secao',
        'orgao_julgador',
        'classe',
        'assunto',
        'area',
        check_fields=False,
    )
    def set_none_2(cls, v, info: ValidationInfo):
        """
        Define "None" caso seja de 1° grau
        """
        if info.data['instancia'] == 'Primeiro Grau':
            return None
        return v


if __name__ == '__main__':
    #
    intim_search = RecebeIntimacoes(
        em_nome_de='Ministério Público do Estado de São Paulo',
        # foro='sss',
        # vara='232323213',
        #instancia='Primeiro Grau',
        instancia='Segundo Grau',
        # especializacao='Criminal',
        especializacao_nao_definida=True,
        cargo_nao_definido=True,
        area='Ambas',
        natureza_comunicacao='Ambas',
    )

    # intim_search = ConsultaIntimacoes(
    #     em_nome_de='Ministério Público do Estado de São Paulo',
    #     # foro='sss',
    #     # vara='232323213',
    #     instancia='Primeiro Grau',
    #     # especializacao='Criminal',
    #     especializacao_nao_definida=True,
    #     cargo_nao_definido=True,
    #     area='Ambas',
    #     natureza_comunicacao='Ambas',
    #     ciencia_ato='Todos',
    #     situacao='Ambas',
    # )

    print(intim_search)
    # print(intim_search.em_nome_de)
    print(intim_search.foro)
    print(intim_search.vara)
    print(intim_search.instancia)
    print(intim_search.area)
