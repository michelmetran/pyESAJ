"""
Módulo para pesquisar
Intimações a serem recebidas
"""

import time
from typing import Union

from selenium import webdriver

import pyesaj as esaj
from pyesaj.scraper.page.intim import CheckError, CheckResults, Recebimento, \
    Consulta
from pyesaj.scraper.params.intim.input import ConsultaIntimacoes, \
    RecebeIntimacoes


def especializa(
    driver: webdriver.Firefox,
    dados: Union[RecebeIntimacoes, ConsultaIntimacoes],
) -> tuple[bool, CheckError, CheckResults]:
    """
    Pesquisa pelas intimações

    Retorna um bool se tem ou não tabela!
    """
    # Vai para página
    if isinstance(dados, RecebeIntimacoes):
        Recebimento(driver=driver)

    elif isinstance(dados, ConsultaIntimacoes):
        Consulta(driver=driver)

    else:
        raise Exception(f'Precisa ser Consulta ou Recebimento, é {type(dados)}')

    # Atributo: Em Nome De
    if dados.em_nome_de is not None:
        intim_em_nome = esaj.scraper.page.intim.EmNomeDe(driver=driver)
        intim_em_nome.set_option(option=dados.em_nome_de)

    # Atributo: Tipo de Participação
    if dados.tipo_participacao is not None:
        intim_tipo = esaj.scraper.page.intim.TipoParticipacao(driver=driver)
        intim_tipo.set_option(option=dados.tipo_participacao)

    # Atributo: Instância
    if dados.instancia is not None:
        intim_inst = esaj.scraper.page.intim.Instancia(driver=driver)
        intim_inst.set_option(instancia=dados.instancia)

    # Atributo: Foro
    if dados.foro is not None:
        intim_foro = esaj.scraper.page.intim.Foro(driver=driver)
        intim_foro.set_option(option=dados.foro)

    # Atributo: Vara
    if dados.vara is not None:
        intim_vara = esaj.scraper.page.intim.Vara(driver=driver)
        intim_vara.set_option(option=dados.vara)

    # Atributo: Seção
    if dados.secao is not None:
        intim_secao = esaj.scraper.page.intim.Secao(driver=driver)
        intim_secao.set_option(option=dados.secao)

    # Atributo: Órgão Julgador
    if dados.orgao_julgador is not None:
        intim_org = esaj.scraper.page.intim.OrgaoJulgador(driver=driver)
        intim_org.set_option(option=dados.orgao_julgador)

    # Atributo: Especialização
    if dados.especializacao is not None:
        intim_esp = esaj.scraper.page.intim.Especializacao(driver=driver)
        intim_esp.set_option(option=dados.especializacao)

    # Atributo: Especialização Checkbox
    if dados.especializacao_nao_definida is True:
        intim_esp = esaj.scraper.page.intim.Especializacao(driver=driver)
        intim_esp.apenas_processos_sem_especializacao()

    # Atributo: Cargo
    if dados.cargo is not None:
        intim_cargo = esaj.scraper.page.intim.Cargo(driver=driver)
        intim_cargo.set_option(option=dados.cargo)

    # Atributo: Cargo Checkbox
    if dados.especializacao_nao_definida is True:
        intim_cargo = esaj.scraper.page.intim.Cargo(driver=driver)
        intim_cargo.apenas_processos_sem_cargo()

    # Atributo: Classe
    if dados.classe is not None:
        intim_classe = esaj.scraper.page.intim.Classe(driver=driver)
        intim_classe.set_option(option=dados.classe)

    # Atributo: Assunto Principal
    if dados.assunto_principal is not None:
        intim_assunto = esaj.scraper.page.intim.AssuntoPrincipal(driver=driver)
        intim_assunto.set_option(option=dados.assunto_principal)

    # Atributo: Área
    if dados.area is not None:
        intim_area = esaj.scraper.page.intim.Area(driver=driver)
        intim_area.set_option(option=dados.area)

    # Atributo: Processo
    if dados.processo is not None:
        intim_proc = esaj.scraper.page.intim.Processo(driver=driver)
        intim_proc.write(texto=dados.processo)

    # Atributo: Natureza de Comunicação
    if dados.natureza_comunicacao is not None:
        intim_nat = esaj.scraper.page.intim.NaturezaComunicacao(driver=driver)
        intim_nat.set_option(natureza=dados.natureza_comunicacao)

    if isinstance(dados, ConsultaIntimacoes):

        # Período: De / Exclusivo do "Consulta"
        if dados.periodo_de is not None:
            intim_per = esaj.scraper.page.intim.consulta.Periodo(driver=driver)
            intim_per.de(data=dados.periodo_de)

        # Período: Até / Exclusivo do "Consulta"
        if dados.periodo_ate is not None:
            intim_per = esaj.scraper.page.intim.consulta.Periodo(driver=driver)
            intim_per.ate(data=dados.periodo_ate)

        # Período: Intervalo / Exclusivo do "Consulta"
        if dados.periodo_de is not None and dados.periodo_ate is not None:
            intim_per = esaj.scraper.page.intim.consulta.Periodo(driver=driver)
            intim_per.define_intervalo(
                de=dados.periodo_de, ate=dados.periodo_ate
            )

        # Atributo: Ciência do Ato / Exclusivo do "Consulta"
        if dados.ciencia_ato is not None:
            intim_cien = esaj.scraper.page.intim.consulta.CienciaAto(
                driver=driver)
            intim_cien.set_option(option=dados.ciencia_ato)

        # Atributo: Situação / Exclusivo do "Consulta"
        if dados.situacao is not None:
            intim_sit = esaj.scraper.page.intim.consulta.Situacao(driver=driver)
            intim_sit.set_option(situacao=dados.situacao)

    # Aguarda
    time.sleep(1)

    # Consulta
    consulta = esaj.scraper.page.intim.ConsultarIntimacoes(driver=driver)
    consulta.consultar()

    # Avalia se tem Resultados
    err = esaj.scraper.page.intim.CheckError(driver=driver)
    # erro = err.has_errors()
    # if erro:
    #     logging.warning(msg=f'Existem erros na consulta')

    res = esaj.scraper.page.intim.CheckResults(driver=driver)
    # tem_res = res.tem_resultado()
    return err, res

    # # Tem erro?
    # if not tem_res:
    #     # logging.info(msg=f'Não existem resultados')
    #     return False, err, res

    # else:
    #     chk_tab = consulta.check_table()
    #     # logging.info(msg=f'Tabel tabela {chk_tab}')
    #     return chk_tab, err, res


if __name__ == '__main__':
    import os

    from dotenv import load_dotenv

    # Credenciais
    load_dotenv()
    USERNAME = os.getenv('USERNAME_TJSP')
    PASSWORD = os.getenv('PASSWORD_TJSP')

    # Cria Driver
    driver2 = esaj.scraper.webdriver.Firefox(verify_ssl=False)

    # Faz Login
    log = esaj.scraper.page.Login(driver=driver2)
    log.login(username=USERNAME, password=PASSWORD)

    # Define
    intim_search = RecebeIntimacoes(
        em_nome_de='Ministério Público do Estado de São Paulo',
        instancia='Segundo Grau',
        especializacao_nao_definida=True,
        cargo_nao_definido=True,
        area='Ambas',
        natureza_comunicacao='Ambas',
    )
    print(intim_search)

    # Intimações
    especializa(driver=driver2, dados=intim_search)

    time.sleep(2)
    driver2.quit()
