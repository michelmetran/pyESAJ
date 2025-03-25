"""
Módulo para definição de objetos
que serão os parâmetros de input
das pesquisas de processos
"""

import warnings
from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class PesquisaProcessos(BaseModel):
    """
    _summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :raises ValueError: _description_
    :raises Exception: _description_
    :return: _description_
    :rtype: _type_
    """

    instancia: Literal['Primeiro Grau', 'Segundo Grau']
    consultar_por: Literal[
        'Número do Processo',
        'Nome da parte',
        'Documento da Parte',
        'Nome do Advogado',
        'OAB',
        'Nº da Carta Precatória na Origem',
        'Nº do Documento na Delegacia',
        'CDA',
    ]
    numero_unificado: Optional[str] = None
    nome_parte: Optional[str] = None
    nome_parte_pesquisa_nome_completo: Optional[bool] = None
    documento_parte: Optional[str] = None
    nome_advogado: Optional[str] = None
    nome_advogado_pesquisa_nome_completo: Optional[bool] = None
    oab: Optional[str] = None
    n_carta_precatoria_origem: Optional[str] = None
    n_documento_delegacia: Optional[str] = None
    cda: Optional[str] = None

    @model_validator(mode='after')
    def check_instancia(self):
        """
        A pesquisa de processos de 2º grau não permite a 'Consulta Por'
        alguns tipos autorizados nas pesquisas de processos de 1º grau.

        Portanto, faz-se necessária a validação.
        """
        consulta_por_2_grau = [
            'Número do Processo',
            'Nome da parte',
            'Documento da Parte',
            'Nome do Advogado',
            'OAB',
            # 'Nº da Carta Precatória na Origem',
            # 'Nº do Documento na Delegacia',
            # 'CDA'
        ]
        if self.instancia == 'Segundo Grau':
            if self.consultar_por not in consulta_por_2_grau:
                list_str = '\n'.join([f'- {x}' for x in consulta_por_2_grau])
                raise ValueError(
                    f'\n\n'
                    f'Para processos de {self.instancia} a pesquisa só pode ser feita por:\n'
                    f'{list_str}'
                    f'\n\n'
                )
        return self

    @model_validator(mode='after')
    def set_none(self, v):
        """
        Define "None" para as variáveis a depender do parâmetro "consultar_por",
        Mantendo apenas os parâmetros necessários àquela "consulta por".
        """

        dc_consulta_por_depende_de = {
            # Consulta Por: Depende De
            'Número do Processo': [{'nome': 'numero_unificado', 'tipo': str}],
            'Nome da parte': [
                {'nome': 'nome_parte'},
                {'nome': 'nome_parte_pesquisa_nome_completo', 'tipo': bool},
            ],
            'Documento da Parte': [{'nome': 'documento_parte', 'tipo': str}],
            'Nome do Advogado': [
                {'nome': 'nome_advogado', 'tipo': str},
                {'nome': 'nome_advogado_pesquisa_nome_completo', 'tipo': bool},
            ],
            'OAB': [{'nome': 'oab', 'tipo': str}],
            'Nº da Carta Precatória na Origem': [
                {'nome': 'n_carta_precatoria_origem', 'tipo': str}
            ],
            'Nº do Documento na Delegacia': [
                {'nome': 'n_documento_delegacia', 'tipo': str}
            ],
            'CDA': [{'nome': 'cda', 'tipo': str}],
        }

        list_depende_de_atrrib = dc_consulta_por_depende_de[self.consultar_por]
        list_depende_de = [x['nome'] for x in list_depende_de_atrrib]
        # print('*' * 100, list_depende_de)

        # Lista das Variáveis, exceto àquelas genéricas, que não serão definidas como None
        list_vars = [
            k
            for k, v in self.model_fields.items()
            if k not in ['instancia', 'consultar_por']
        ]
        # print('*' * 100, list_vars)

        for var in list_vars:
            if var in list_depende_de and eval(f'self.{var}') is None:
                raise Exception(f'A variável "{var}" precisa ser definida!')

            elif var not in list_depende_de:
                if eval(f'self.{var}') is not None:
                    # Mensagem
                    warnings.warn(
                        message=f'\n'
                        f'Na pesquisa por "{self.consultar_por}" depende dos atributos {list_depende_de}.\n'
                        f'O atributo "{var}" está como "{eval(f"self.{var}")}" e será definido como "None".'
                        f'\n',
                        category=RuntimeWarning,
                    )
                    # Set None
                    setattr(self, var, None)

        return self


if __name__ == '__main__':
    proced = PesquisaProcessos(
        instancia='Segundo Grau',
        # consultar_por='Número do Processo',
        consultar_por='Nome da parte',
        # consultar_por='CDA',
        # numero_unificado='0123479-07.2012.8.26.0100',
        # Parte
        nome_parte='Michel Metran',
        nome_parte_pesquisa_nome_completo=False,
        # documento_parte='43.547.234-74',
        # Advogado
        # nome_advogado='Fernanda Dal Picolo',
        # nome_advogado_pesquisa_nome_completo=True,
        # oab='178.780',
        # Outros
        # n_carta_precatoria_origem='123.456.789',
        # n_documento_delegacia='001.431.473-67',
        # cda='01.432.326-0001/55',
    )
    print(proced)
