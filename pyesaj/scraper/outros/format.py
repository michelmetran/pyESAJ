"""
Módulo para funções diversas
"""

import logging


def format_number(n_esaj):
    """
    Notei que alguns números podem não estar adequadamente configurados.
    A Procuradoria da Câmara Especial trabalha dessa maneira.

    O Padrão do eSAJ tem 25 números.

    Converte
    De:   1028803-47.2022.8.26.0602/50000
    Para: 1028803-47.2022.8.26.0602
    """
    number_esaj_splitted = n_esaj.strip().split('/')
    n_esaj = number_esaj_splitted[0]

    if len(n_esaj) != 25:
        # print(f'O número tem {len(n_esaj)} caracteres')
        logging.info(
            f'O número do processo não tem 25 caracteres (padrão eSAJ). Tem {len(n_esaj)} caracteres!'
        )

    return n_esaj


if __name__ == '__main__':
    a = format_number(n_esaj='1028803-47.2022.8.26.0602/50000')
    print(a)

    a = format_number(n_esaj='1028803-47.2022.8.26.0602')
    print(a)

    print('8.26' in a)

    # import pyesaj as esaj
    # esaj.outros.format.format_number(n_esaj=)
