"""
Módulo para pesquisar processos
"""

import time

from selenium import webdriver

import pyesaj as esaj
from pyesaj.scraper.params.processo.input import PesquisaProcessos


def pesquisa(driver: webdriver.Firefox, dados: PesquisaProcessos) -> None:
    """
    Pesquisa pelas intimações
    """
    # Vai para página
    esaj.scraper.page.processo.ConsultaProcesso(driver=driver, grau=dados.instancia)

    # Define Parâmetro de Pesquisa
    por = esaj.scraper.page.processo.ConsultaPor(driver=driver)
    # print(por.get_options())
    por.set_option(option=dados.consultar_por)

    # Número
    if dados.numero_unificado is not None:
        num = esaj.scraper.page.processo.NumeroUnificado(driver=driver)
        num.define_numero(numero=dados.numero_unificado)

    if dados.nome_parte is not None:
        nome = esaj.scraper.page.processo.NomeParte(driver=driver)
        nome.set_nome_parte(nome=dados.nome_parte)
        if dados.nome_parte_pesquisa_nome_completo is True:
            nome.pesquisa_nome_completo()

    # Documento da Parte
    if dados.documento_parte is not None:
        doc = esaj.scraper.page.processo.DocumentoParte(driver=driver)
        doc.set_documento(documento=dados.documento_parte)

    # Nome do Advogado
    if dados.nome_advogado is not None:
        nome = esaj.scraper.page.processo.NomeAdvogado(driver=driver)
        nome.set_nome_adv(nome=dados.nome_advogado)
        if dados.nome_advogado_pesquisa_nome_completo is True:
            nome.pesquisa_nome_completo()

    # OAB
    if dados.oab is not None:
        oab = esaj.scraper.page.processo.OAB(driver=driver)
        oab.set_documento(documento=dados.oab)
        # if dados.nome_advogado_pesquisa_nome_completo is True:
        #     nome.pesquisa_nome_completo()

    # Número da Carta Precatória na Origem
    if dados.n_carta_precatoria_origem is not None:
        carta = esaj.scraper.page.processo.NumCartaPrecatoria(driver=driver)
        carta.set_documento(documento=dados.n_carta_precatoria_origem)

    # Nº do Documento na Delegacia
    if dados.n_documento_delegacia is not None:
        deleg = esaj.scraper.page.processo.NumDocDelegacia(driver=driver)
        deleg.set_documento(documento=dados.n_documento_delegacia)

    # CDA
    if dados.cda is not None:
        cda = esaj.scraper.page.processo.CDA(driver=driver)
        cda.set_documento(documento=dados.cda)

    # Consultar
    con = esaj.scraper.page.processo.Consultar(driver=driver)
    con.consultar(grau=dados.instancia)


if __name__ == '__main__':
    # import os

    # from dotenv import load_dotenv

    # Credenciais
    # load_dotenv()
    # USERNAME = os.getenv('USERNAME_TJSP')
    # PASSWORD = os.getenv('PASSWORD_TJSP')

    # Cria Driver
    driver2 = esaj.scraper.webdriver.Firefox(verify_ssl=False)

    # Faz Login
    # log = esaj.page.Login(driver=driver)
    # log.login(username=USERNAME, password=PASSWORD)

    # Define
    proced = PesquisaProcessos(
        instancia='Segundo Grau',
        # consultar_por='Número do Processo',
        consultar_por='Nome da parte',
        # consultar_por='CDA',
        # numero_unificado='0123479-07.2012.8.26.0100',
        # Parte
        nome_parte='Michel Metran da Silva',
        nome_parte_pesquisa_nome_completo=True,
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

    # Intimações
    pesquisa(driver=driver2, dados=proced)

    time.sleep(2)
    driver2.quit()
