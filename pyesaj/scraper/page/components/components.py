"""
Módulo com os componentes gerais,
que são usados em vários filtros do eSAJ
"""

import time
from typing import List

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pyesaj.scraper.pom import PageElement


# flake8: noqa:303
# flake8: noqa:E501


class InputModelSearchSet(PageElement):
    """
    Representa os campos de *input*, onde é possível pesquisar
    as opções por meio de um *pop-up*.
    """

    # xPaths Fixos
    btn_fechar = (By.XPATH, '//input[@id="pbFechar"]')
    btn_selecionar = (By.XPATH, '//input[@id="pbSelecionar"]')
    btn_procurar = (By.XPATH, '//input[@id="pbProcurar"]')
    iframe = (By.XPATH, '//iframe[@id="layerFormConsulta"]')

    def __init__(self, driver):
        super().__init__(driver)
        # xpaths variáveis
        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelForo"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="nmForo"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.nmForo"]')
        self.lista_opcoes = None

    def get_options(self) -> List[str]:
        """
        Obtém opções de preenchimento.
        """

        try:
            self.click(self.abre_consulta)
            self.switch(self.iframe)
            self.lista_opcoes = [
                x.text for x in self.find_all(self.linhas_tabela)
            ]
            self.click(self.btn_fechar)
            return self.lista_opcoes

        except Exception as e:
            self.click(self.btn_fechar)
            raise ValueError('Erro.') from e

        finally:
            self.switch_back()

    def set_option(self, option) -> None:
        """
        Define a opção para preenchimento do campo.
        """

        if self.lista_opcoes is None:
            self.lista_opcoes = self.get_options()

        if option not in self.lista_opcoes:
            raise ValueError(f'Precisa ser uma opção {self.lista_opcoes}')

        try:
            self.click(self.abre_consulta)
            self.switch(self.iframe)
            # self.lista_foros = [x.text for x in self.find_all(self.linhas_tabela)]
            # Insere o Foro no campo de busca
            self.set(self.input_opcao, option)

            # Procura
            self.click(self.btn_procurar)

            # Se a linha for a que eu procuro, Clica!
            # TODO: Aperfeiçoar com BS4 (18.11.2024)
            for row in self.find_all(self.linhas_tabela):
                if row.text == option:
                    row.click()

            # Seleciona
            self.click(self.btn_selecionar)

        except Exception as e:
            raise ValueError(
                f'Precisa ser uma opção {self.lista_opcoes}'
            ) from e

        finally:
            self.switch_back()


class InputModelTree(PageElement):
    """
    Representa os campos de *input*, onde é possível pesquisar
    as opções por meio de um *pop-up* hierárquico.

    Usado apenas na pesquisa de "Classe" e/ou "Assunto Principal".
    """

    def __init__(self, driver):
        super().__init__(driver)
        # Variável
        self.abre_consulta = (
            By.XPATH,
            '//td[@id=""]/following-sibling::td//tr//img[@id="botaoProcurar_classes" and @title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//ul[@id="classes_tree"]//span[@class="node selectable checkable Unchecked"]',
        )
        self.input_opcao = (
            By.XPATH,
            '//input[@id="classes_treeSelectFilter"]',
        )
        self.btn_selecionar = (
            By.XPATH,
            '//div[@id="assuntos_treeSelectContainer"]//input[@class="spwBotaoDefaultGrid" and @value="Selecionar"]',
        )
        self.btn_procurar = (
            By.XPATH,
            '//div[@id="assuntos_treeSelectContainer"]//input[@id="filtroButton"]',
        )
        self.lista_opcoes = None

        # Default
        self.btn_fechar = (
            By.XPATH,
            '//div[@class="blockUI blockMsg blockPage"]//button[@id="popupModalBotaoFechar"]',
        )
        self.msg_loading = (By.XPATH, '//div[@id="popupModalCarregando"]')

    def get_options(self) -> List:
        """
        Obtém opções de preenchimento.
        """

        self.zoom(zoom=100)

        try:
            # Abre a Consulta
            self.click(locator=self.abre_consulta)

            # Aguarda Carregar
            loading = self.find_all(locator=self.msg_loading, wait=0)
            tries = 0
            while len(loading) > 0 and tries <= 12:
                time.sleep(5)
                loading = self.find_all(self.msg_loading, wait=0)
                tries += 1
                print(f'Tentativa #{tries}. Já aguardei 5 segundos')

            # Pega opções para checar
            rows = self.find_all(self.linhas_tabela, wait=0)
            # print(len(rows))
            self.lista_opcoes = [x.text for x in rows]
            return self.lista_opcoes

        except Exception as e:
            raise ValueError('Problemas para obter os itens.') from e
            # CheckError(self).has_errors()

        finally:
            # Fecha a Consulta
            self.click(locator=self.btn_fechar)

    def set_option(self, option) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        self.zoom(zoom=100)
        if self.lista_opcoes is None:
            self.lista_opcoes = self.get_options()

        if option not in self.lista_opcoes:
            raise ValueError(f'Precisa ser uma opção {self.lista_opcoes}')

        try:
            self.click(self.abre_consulta)

            # Aguarda Carregar
            loading = self.find_all(locator=self.msg_loading, wait=0)
            tries = 0
            while len(loading) > 0 and tries <= 12:
                time.sleep(5)
                loading = self.find_all(self.msg_loading, wait=0)
                tries += 1
                print(f'Tentativa #{tries}. Já aguardei 5 segundos')

            # Define o termo a ser pesquisado
            self.set(self.input_opcao, option)

            # Clica em Procurar
            self.click(self.btn_procurar)
            time.sleep(10)

            # Se a linha for a que eu procuro, Clica!
            for row in self.find_all(self.linhas_tabela, wait=0):
                if row.text == option:
                    row.click()
                    break

        except Exception as e:
            raise ValueError('Erro ao definir opção.') from e

        finally:
            # Preciso fazer essa gambiarra pois o eSAJ é uma merda
            # e esconde o botão
            # Em headless deve funcionar sem essa necessidade, mas como
            # não estamos em headless, foi necessário!
            self.zoom(zoom=50)
            time.sleep(2)
            # self.set(locator=self.input_opcao, value=Keys.RETURN)
            # self.click(locator=self.btn_selecionar)
            ActionChains(self.driver).move_to_element(
                self.find(locator=self.btn_selecionar)
            ).click().perform()
            self.zoom(zoom=100)


if __name__ == '__main__':
    pass
