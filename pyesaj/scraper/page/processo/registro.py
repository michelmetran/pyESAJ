"""
Módulo com a página do registro de Processos,
ou seja, dados de Partes, Movimentação etc
"""

from selenium.webdriver.common.by import By

from pyesaj.scraper.pom import PageElement


# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


# flake8: noqa:303
# flake8: noqa:E501


class Header(PageElement):
    """
    Representa o Header, ou seja, as informações do processo.
    Deverá servir para processos de Primeiro e Segundo Graus
    """

    # Informação Básica
    classe = (By.XPATH, '//*[@id="classeProcesso"]')
    assunto = (By.XPATH, '//*[@id="assuntoProcesso"]')
    foro = (By.XPATH, '//*[@id="foroProcesso"]')
    vara = (By.XPATH, '//*[@id="varaProcesso"]')
    juiz = (By.XPATH, '//*[@id="juizProcesso"]')

    # Após Clicar em "Ver Mais"
    distribuicao = (By.XPATH, '//*[@id="dataHoraDistribuicaoProcesso"]')
    n_controle = (By.XPATH, '//*[@id="numeroControleProcesso"]')
    area = (By.XPATH, '//*[@id="areaProcesso"]')
    valor_acao = (By.XPATH, '//*[@id="valorAcaoProcesso"]')

    # Outros
    outros_numeros = (
        By.XPATH,
        '//*[@class="unj-label" and contains(text(),"Outros números")]/following-sibling::div',
    )
    local_fisico = (
        By.XPATH,
        '//*[@class="unj-label" and contains(text(),"Local Físico")]/following-sibling::div',
    )
    outros_assuntos = (
        By.XPATH,
        '//*[@class="unj-label" and contains(text(),"Outros assuntos")]/following-sibling::div',
    )

    # Ver Mais
    ver_mais = (
        By.XPATH,
        '//div[@class="unj-entity-header"]//*[@href="#maisDetalhes"]',
    )

    def get_class(self) -> None:
        """
        Define o "Nº do Documento da Delegacia".
        """
        self.clica_ver_mais()
        dd_dados = {
            'classe': self.get_text(locator=self.classe),
            'assunto': self.get_text(locator=self.assunto),
            'foro': self.get_text(locator=self.foro),
            'vara': self.get_text(locator=self.vara),
            'juiz': self.get_text(locator=self.juiz),
            # Ver Mais
            'distribuicao': self.get_text(locator=self.distribuicao, wait=1),
            'n_controle': self.get_text(locator=self.n_controle, wait=1),
            'area': self.get_text(locator=self.area, wait=1),
            'valor_acao': self.get_text(locator=self.valor_acao, wait=1),
            # Outros
            'outros_numeros': self.get_text(
                locator=self.outros_numeros, wait=1
            ),
            'local_fisico': self.get_text(locator=self.local_fisico, wait=1),
            'outros_assuntos': self.get_text(
                locator=self.outros_assuntos, wait=1
            ),
        }

        # Ver Menos / Recolher
        self.clica_ver_menos()
        return dd_dados

    def clica_ver_mais(self):
        if (
            self.attribute(locator=self.ver_mais, attribute='aria-expanded')
            == 'false'
        ):
            self.click(locator=self.ver_mais)

    def clica_ver_menos(self):
        if (
            self.attribute(locator=self.ver_mais, attribute='aria-expanded')
            != 'false'
        ):
            self.click(locator=self.ver_mais)


class Partes(PageElement):
    """
    Representa a Sessão que contem as Partes do Processo.
    Deverá servir para processos de Primeiro e Segundo Graus
    Por ora só funciona para processos de 1º grau!
    """

    # Tabela
    tabela_linhas = (By.XPATH, '//table[@id="tableTodasPartes"]//tbody//tr')

    # Ver Mais
    ver_mais_loc = (
        By.XPATH,
        '//*[@id="divLinksTituloBlocoPartes"]',
    )
    ver_mais = (
        By.XPATH,
        '//*[@id="linkpartes"]//i',
    )

    def get_partes(self) -> None:
        """
        Define o "Nº do Documento da Delegacia".
        """

        self.clica_ver_mais()

        rows = self.find_all(locator=self.tabela_linhas)
        dd = []
        for i in rows:
            list_itens = i.text.strip().split('\n', maxsplit=1)
            for item in list_itens:
                # print(item)

                if item.startswith('Reqte  '):
                    item = item.replace('Reqte  ', '').strip()
                    # print(item)
                    dd.append({'requerente': item})

                if item.startswith('Reqdo  '):
                    item = item.replace('Reqdo  ', '').strip()
                    # print(item)
                    dd.append({'requerido': item})

                if item.startswith('Advogada:  ') or item.startswith(
                    'Advogado:  '
                ):
                    item = (
                        item.replace('Advogada:  ', '')
                        .replace('Advogado:  ', '')
                        .strip()
                    )
                    # print(item)
                    dd.append({'advogado': item})

        self.clica_ver_menos()
        return dd

    def clica_ver_mais(self):
        # aaa = self.find(locator=self.ver_mais)
        # self.script("arguments[0].scrollIntoView();", aaa)
        self.script("scrollBy(0,0);")

        # Vai até o botão do Ver Mais
        self.script(
            "arguments[0].scrollIntoView();",
            self.find(locator=self.ver_mais_loc),
        )
        # Sobe um pouco
        self.driver.execute_script("window.scrollBy(0, -250);")

        if (
            self.attribute(locator=self.ver_mais, attribute='class')
            == 'unj-link-collapse__icon glyph glyph-chevron-down'
        ):
            self.click(locator=self.ver_mais)

            # Vai até o botão do Ver Mais
            self.script(
                "arguments[0].scrollIntoView();",
                self.find(locator=self.ver_mais_loc),
            )
            # Sobe um pouco
            self.driver.execute_script("window.scrollBy(0, -250);")

    def clica_ver_menos(self):
        # Vai até o botão do Ver Mais
        self.script(
            "arguments[0].scrollIntoView();",
            self.find(locator=self.ver_mais_loc),
        )
        # Sobe um pouco
        self.driver.execute_script("window.scrollBy(0, -250);")
        # self.script("scrollBy(0,0);")

        if (
            self.attribute(locator=self.ver_mais, attribute='class')
            != 'unj-link-collapse__icon glyph glyph-chevron-down'
        ):
            self.click(locator=self.ver_mais)

            # Vai até o botão do Ver Mais
            self.script(
                "arguments[0].scrollIntoView();",
                self.find(locator=self.ver_mais_loc),
            )
            # Sobe um pouco
            self.driver.execute_script("window.scrollBy(0, -250);")




class Movimentacao(PageElement):
    """
    Representa a Sessão que contem as Partes do Processo.
    Deverá servir para processos de Primeiro e Segundo Graus
    Por ora só funciona para processos de 1º grau!
    """

    # Tabela
    tabela_linhas = (By.XPATH, '//tbody[@id="tabelaTodasMovimentacoes"]//tr')
    row_data_mov = (By.XPATH, './/td[@class="dataMovimentacao"]')
    row_desc_mov = (By.XPATH, './/td[@class="descricaoMovimentacao"]')

    # Ver Mais
    ver_mais_loc = (
        By.XPATH,
        '//*[@id="divLinksTituloBlocoMovimentacoes"]',
    )

    ver_mais = (
        By.XPATH,
        '//*[@id="linkmovimentacoes"]//i',
    )

    def get_table(self) -> None:
        """
        Define o "Nº do Documento da Delegacia".
        """

        self.clica_ver_mais()

        rows = self.find_all(locator=self.tabela_linhas)
        dd = []
        for row in rows:
            # print(row.text)
            data_xpath = self.row_data_mov + (row,)
            data = self.get_text(locator=data_xpath, wait=3)
            # print(data)

            desc_xpath = self.row_desc_mov + (row,)
            desc = self.get_text(locator=desc_xpath, wait=3)
            # print(desc)

            dd.append({'data_movimentacao': data, 'descricao': desc})

        self.clica_ver_menos()
        return dd

    def clica_ver_mais(self):
        # Vai até o botão do Ver Mais
        self.script(
            "arguments[0].scrollIntoView();",
            self.find(locator=self.ver_mais_loc),
        )
        # Sobe um pouco
        self.driver.execute_script("window.scrollBy(0, -250);")

        if (
            self.attribute(locator=self.ver_mais, attribute='class')
            == 'unj-link-collapse__icon glyph glyph-chevron-down'
        ):

            # Clica no Botão Ver Mais
            self.click(locator=self.ver_mais)

            # Vai até o botão do Ver Mais
            self.script(
                "arguments[0].scrollIntoView();",
                self.find(locator=self.ver_mais_loc),
            )
            # Sobe um pouco
            self.driver.execute_script("window.scrollBy(0, -250);")

    def clica_ver_menos(self):
        # Vai até o botão do Ver Mais
        self.script(
            "arguments[0].scrollIntoView();",
            self.find(locator=self.ver_mais_loc),
        )
        # Sobe um pouco
        self.driver.execute_script("window.scrollBy(0, -250);")

        if (
            self.attribute(locator=self.ver_mais, attribute='class')
            != 'unj-link-collapse__icon glyph glyph-chevron-down'
        ):
            self.click(locator=self.ver_mais)

            # Vai até o botão do Ver Mais
            self.script(
                "arguments[0].scrollIntoView();",
                self.find(locator=self.ver_mais_loc),
            )
            # Sobe um pouco
            self.driver.execute_script("window.scrollBy(0, -250);")




if __name__ == '__main__':
    pass
