"""
Módulo com a página de cadastro do eSAJ
Para pegar o que o usuário tem autorização para fazer
"""

import re
import time

from selenium.webdriver.common.by import By

from pyesaj.scraper.pom import Page, PageElement


# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


# flake8: noqa:303
# flake8: noqa:E501


class Recebimento(Page):
    """
    Página "Intimações On-line > Recebimento de Intimações Eletrônicas"
    """

    url = 'https://esaj.tjsp.jus.br/intimacoesweb/abrirConsultaAtosNaoRecebidos.do'

    def __init__(self, driver):
        super().__init__(driver)
        self.go_to(self.url)


class Paginacao(PageElement):
    # Paginação Botões
    btn_primeira_pagina = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@title="Primeira página"]',
    )
    btn_pagina_anterior = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@title="Página anterior"]',
    )
    btn_proxima_pagina = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@title="Próxima página"]',
    )
    btn_ultima_pagina = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@title="Última página"]',
    )
    # Páginas
    pagina_atual_xpath = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@id="gridAtosNaoRecebidosUsuario_display"] | //div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//input[@id="gridAtosUsuario_display"]',
    )
    total_paginas_xpath = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//c[@id="gridAtosNaoRecebidosUsuario_nuTotalPags"] | //div[@id="rodapeGridPaginada"]//span[@id="botoesRodapeGrid"]//c[@id="gridAtosUsuario_nuTotalPags"]',
    )
    # Intimações
    n_intimacoes_inferior = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//b[@id="gridAtosNaoRecebidosUsuarioLimInferior"] | //div[@id="rodapeGridPaginada"]//b[@id="gridAtosUsuarioLimInferior"]',
    )
    n_intimacoes_superior = (
        By.XPATH,
        '//div[@id="rodapeGridPaginada"]//b[@id="gridAtosNaoRecebidosUsuarioLimSuperior"] | //div[@id="rodapeGridPaginada"]//b[@id="gridAtosUsuarioLimSuperior"]',
    )
    n_intimacoes_total = (By.XPATH, '//div[@id="rodapeGridPaginada"]')

    def infos(self):
        """
        Pega Página atual
        pega total de páginas
        Vai pra próxima, desde que seja menor que o número total de paginas
        Aguarda carregar
        """
        # Número de Páginas
        num_page_atual = self.attribute(
            locator=self.pagina_atual_xpath, attribute='value'
        )
        num_page_atual = int(num_page_atual)
        num_page_total_atual = self.get_text(self.total_paginas_xpath)
        num_page_total_atual = int(num_page_total_atual)
        # print(f'Páginas: de {num_page_atual} à {num_page_total_atual}')

        # Número de Intimações
        n_inf = self.get_text(locator=self.n_intimacoes_inferior)
        n_sup = self.get_text(locator=self.n_intimacoes_superior)

        # Converte em inteiros
        n_inf = int(n_inf)
        n_sup = int(n_sup)

        # Paginação
        paginacao = self.get_text(locator=self.n_intimacoes_total)
        paginacao = paginacao.split('\n')[0]

        list_results = re.findall(r'de (\w+)', paginacao)
        if len(list_results) == 1:
            n_intimacoes = int(list_results[0])

        else:
            raise ValueError(
                'Problema na obtenção do número total de intimações.'
            )
        # print(f'Intimações: de {n_inf} à {n_sup} ({n_intimacoes})')
        return {
            'num_intimacoes_de': n_inf,
            'num_intimacoes_até': n_sup,
            'num_intimacoes_total': n_intimacoes,
            'num_pagina_atual': num_page_atual,
            'num_pagina_total': num_page_total_atual,
        }

    def proxima_pagina(self) -> int:
        """
        Pega Página atual
        pega total de páginas
        Vai pra próxima, desde que seja menor que o númeor total de paginas
        Aguarda carregar
        """
        pages_info = self.infos()
        n_pagina_inicio = pages_info['num_pagina_atual']
        n_pagina_atual = pages_info['num_pagina_atual']
        n_pagina_quero = pages_info['num_pagina_atual'] + 1
        n_pagina_total = pages_info['num_pagina_total']

        if n_pagina_atual == n_pagina_total:
            print('Já estou na última página')
            return n_pagina_atual

        if (
            n_pagina_inicio < n_pagina_total
            and n_pagina_inicio < n_pagina_quero
        ):

            while n_pagina_atual != n_pagina_quero:
                # Avança
                self.click(locator=self.btn_proxima_pagina)
                time.sleep(2)

                # Pega Página
                n_pagina_atual = self.infos()['num_pagina_atual']
                n_pagina_changed = self.infos()['num_pagina_atual']
                print(
                    f'Estava na página {n_pagina_inicio}. Vim para {n_pagina_changed}'
                )
            return n_pagina_atual

        if n_pagina_atual > n_pagina_total:
            raise RuntimeError('Como estou em uma página que não existe?')

    def volta_pagina(self) -> int:
        """
        Pega Página atual
        pega total de páginas
        Vai pra próxima, desde que seja menor que o número total de paginas
        Aguarda carregar
        """
        pages_info = self.infos()
        n_pagina_inicio = pages_info['num_pagina_atual']
        n_pagina_atual = pages_info['num_pagina_atual']
        n_pagina_quero = pages_info['num_pagina_atual'] - 1
        n_pagina_total = pages_info['num_pagina_total']

        if n_pagina_inicio == 1:
            print('Já estou na primeira página')
            return n_pagina_atual

        if (
            # n_pagina_inicio <= n_pagina_total
            # and n_pagina_inicio > n_pagina_quero
            n_pagina_total
            >= n_pagina_inicio
            > n_pagina_quero
        ):

            while n_pagina_atual != n_pagina_quero:
                # Retrocede
                self.click(locator=self.btn_pagina_anterior)
                time.sleep(2)

                # Pega Página
                n_pagina_atual = self.infos()['num_pagina_atual']
                n_pagina_changed = self.infos()['num_pagina_atual']
                print(
                    f'Estava na página {n_pagina_inicio}. Vim para {n_pagina_changed}'
                )
            return n_pagina_atual

        if n_pagina_atual > n_pagina_total:
            raise RuntimeError('Como estou em uma página que não existe?')

    def vai_primeira(self) -> int:
        """
        Vai para a primeira página.
        """
        pages_info = self.infos()
        # n_pagina_inicio = pages_info['num_pagina_atual']
        n_pagina_atual = pages_info['num_pagina_atual']
        n_pagina_quero = 1
        # n_pagina_total = pages_info['num_pagina_total']

        while n_pagina_atual != n_pagina_quero:
            self.click(locator=self.btn_primeira_pagina)
            time.sleep(2)

            # Pega Página
            n_pagina_atual = self.infos()['num_pagina_atual']
        return n_pagina_atual

    def vai_ultima(self):
        """
        Vai para a última página.
        """
        pages_info = self.infos()
        # n_pagina_inicio = pages_info['num_pagina_atual']
        n_pagina_atual = pages_info['num_pagina_atual']
        # n_pagina_quero = 1
        n_pagina_quero = pages_info['num_pagina_total']

        while n_pagina_atual != n_pagina_quero:
            self.click(locator=self.btn_ultima_pagina)
            time.sleep(2)

            # Pega Página
            n_pagina_atual = self.infos()['num_pagina_atual']
        return n_pagina_atual


if __name__ == '__main__':
    import os

    from dotenv import load_dotenv

    import pyesaj as esaj

    # Credenciais
    load_dotenv()
    USERNAME = os.getenv('USERNAME_TJSP')
    PASSWORD = os.getenv('PASSWORD_TJSP')

    # Cria Driver
    driver = esaj.webdriver.Firefox(verify_ssl=False)

    # Entra no eSAJ e loga
    log = esaj.page.Login(driver=driver)
    log.login(username=USERNAME, password=PASSWORD)

    # Intimações
    intim = esaj.page.intim.Recebimento(driver=driver)

    intim_em_nome = esaj.page.intim.EmNomeDe(driver=driver)
    intim_em_nome.set_option(option='Ministério Público do Estado de São Paulo')

    # Instância: 1º Grau
    intim_inst = esaj.page.intim.Instancia(driver=driver)
    intim_inst.set_option(instancia='Primeiro Grau')

    # # Foro
    # intim_foro = esaj.page.intim.recebe.Foro(driver=driver)
    # print(intim_foro.get_options())
    # intim_foro.set_option(option='Foro de Campinas')
    #
    # # Vara
    # intim_vara = esaj.page.intim.recebe.Vara(driver=driver)
    # print(intim_vara.get_options())
    # intim_vara.set_option(option='2ª Vara de Família e Sucessões')
    #
    # # Especialização
    # intim_esp = esaj.page.intim.recebe.Especializacao(driver=driver)
    # print(intim_esp.get_options())
    # intim_esp.set_option(option='Registros Públicos')

    # Instância: 2º Grau
    intim_inst = esaj.page.intim.Instancia(driver=driver)
    intim_inst.set_option(instancia='Segundo Grau')

    # Seção
    intim_secao = esaj.page.intim.Secao(driver=driver)
    print(intim_secao.get_options())
    intim_secao.set_option(option='Direito Privado 2')

    # Órgão Julgador
    # intim_org = esaj.page.intim.recebe.OrgaoJulgador(driver=driver)
    # print(intim_org.get_options())

    # Consultar
    consulta = pyesaj.scraper.page.intim.recebe.ConsultarIntimacoes(driver=driver)
    consulta.consultar()
    time.sleep(5)

    # Paginação
    pag = pyesaj.scraper.page.intim.recebe.Paginacao(driver=driver)
    print(pag.infos())

    time.sleep(5)
    driver.quit()
