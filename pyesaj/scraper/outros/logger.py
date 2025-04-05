"""
Módulo para criar decorator para desabilitar o login em funções.

Isso se faz necessário, pois existem funções que usam a tentativa e erro de encontrar um elemento, para trazer um resultado.
Por exemplo, "não tem resultado" é um retorno quando a função não encontra elementos.

Logo, é necessário desabilitar o logging "não encontrou elementos" para essas funções, deixando-a apenas em funções que é necessário encontrar um elemento, senão é erro....

https://stackoverflow.com/questions/7341064/disable-logging-per-method-function

Michel Metran
Data: 18.12.2024
Atualizado em: 18.12.2024
"""

import functools
import logging
from functools import wraps


def disable_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        result = func(*args, **kwargs)
        logging.disable(logging.NOTSET)
        return result

    return wrapper


def disable_logging_property(func):
    @property
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        result = func(*args, **kwargs)
        logging.disable(logging.NOTSET)
        return result

    return wrapper


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(funcName)s(): %(message)s',
    )
    log = logging.getLogger()

    some_value = 1

    # log.debug("Here's an interesting value: %r" % some_value)
    # log.info("Going great here!")

    @disable_logging
    def my_func1():
        log.debug('This is my_func1()')

    my_func1()
