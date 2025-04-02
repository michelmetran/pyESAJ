"""
Módulo com a página de
"Consulta de Intimações Recebidas"
"""

from datetime import date, datetime
from typing import List, Literal, Union

from selenium.webdriver.common.by import By

from pyesaj.scraper.pom import Page, PageElement


# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# from typing import Literal
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By


class Consulta(Page):
    """
    Página "Intimações On-line > Consulta de Intimações Recebidas"
    """

    url = 'https://esaj.tjsp.jus.br/intimacoesweb/abrirConsultaAtosRecebidos.do'

    def __init__(self, driver):
        super().__init__(driver)
        self.go_to(self.url)


class Periodo(PageElement):
    """
    Representa o menu *dropdown* "Em nome de", que define
    qual o perfil do usuário que será utilizado.

    Pode ser pesquisa de intimações recebidas pelo nome do usuário,
    pessoa física, ou a pesquisa pelo
    "Ministério Público do Estado de São Paulo",
    caso o usuário seja funcionário dessa instituição.
    """

    dt_inicio = (By.XPATH, '//input[@name="dadosConsulta.dtInicioPeriodo"]')
    dt_fim = (By.XPATH, '//input[@name="dadosConsulta.dtFimPeriodo"]')

    def de(self, data: Union[date, str]):
        """
        Define a Data de Início do período de consulta.
        Precisa estar em formato *date* ou *str*, no padrão "%d/%m/%Y".
        """
        if isinstance(data, str):
            data = datetime.strptime(data, '%d/%m/%Y').date()

        elif isinstance(data, date):
            pass

        else:
            raise Exception(
                'Precisa ser formato date ou str no padrão "%d/%m/%Y"'
            )

        self.set(self.dt_inicio, data.strftime(format='%d/%m/%Y'))

    def ate(self, data: Union[date, str]):
        """
        Define a Data Fim do período de consulta.
        Precisa estar em formato *date* ou *str*, no padrão "%d/%m/%Y".
        """
        if isinstance(data, str):
            data = datetime.strptime(data, '%d/%m/%Y').date()

        elif isinstance(data, date):
            pass

        else:
            raise Exception(
                'Precisa ser formato date ou str no padrão "%d/%m/%Y"'
            )

        # data_inicio = self.get_text(locator=self.dt_inicio)

        # print('Data Início ', data_inicio)
        self.set(self.dt_fim, data.strftime(format='%d/%m/%Y'))

    def define_intervalo(self, de, ate):
        """
        Define a Data de Início e Fim do período de consulta.
        As datas precisam estar em formato *date* ou *str*, no padrão "%d/%m/%Y".
        """

        if isinstance(de, str):
            de = datetime.strptime(de, '%d/%m/%Y').date()

        elif isinstance(de, date):
            pass

        else:
            raise Exception(
                'Precisa ser formato date ou str no padrão "%d/%m/%Y"'
            )

        if isinstance(ate, str):
            ate = datetime.strptime(ate, '%d/%m/%Y').date()

        elif isinstance(ate, date):
            pass

        else:
            raise Exception(
                'Precisa ser formato date ou str no padrão "%d/%m/%Y"'
            )

        # Avalia se o
        if de <= ate:
            pass

        elif de > ate:
            raise Exception(
                'Data de início precisa ser menor ou igual que data fim!'
            )

        # Define
        self.de(data=de)
        self.ate(data=ate)


class CienciaAto(PageElement):
    """
    Representa o menu *dropdown* "Ciência do Ato", que define
    qual o tipo da ciência do ato desejada.
    """

    selector_em_nome_de = (
        By.XPATH,
        '//select[@name="dadosConsulta.formaCienciaIntimacao"]',
    )

    def get_options(self) -> List[str]:
        """
        Obtém opções de preenchimento.
        """
        return self.create_select_options(self.selector_em_nome_de)

    def set_option(self, option) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        list_options = self.get_options()
        if option not in list_options:
            raise ValueError(f'Precisa ser uma opção {list_options}')

        self.select(self.selector_em_nome_de, option)


class Situacao(PageElement):
    """
    Representa o *radio button* "Situação".
    """

    cumprida = (
        By.XPATH,
        '//input[@name="entity.ato.flCumprido" and @value="S"]',
    )
    pendente = (
        By.XPATH,
        '//input[@name="entity.ato.flCumprido" and @value="N"]',
    )
    ambas = (By.XPATH, '//input[@name="entity.ato.flCumprido" and @value]')

    def set_option(
        self, situacao: Literal['Cumprida', 'Pendente', 'Ambas']
    ) -> None:
        """
        Define a opção para preenchimento do campo.
        """

        if situacao == 'Cumprida':
            self.click(locator=self.cumprida)

        elif situacao == 'Pendente':
            self.click(locator=self.pendente)

        elif situacao == 'Ambas':
            all = self.find_all(locator=self.ambas)
            all[2].click()


if __name__ == '__main__':
    import os
    import time

    from dotenv import load_dotenv

    import pyesaj as esaj

    # Credenciais
    load_dotenv()
    USERNAME = os.getenv('USERNAME_TJSP')
    PASSWORD = os.getenv('PASSWORD_TJSP')

    # Cria Driver
    driver2 = esaj.scraper.webdriver.Firefox(verify_ssl=False)

    # Entra no eSAJ e loga
    log = esaj.scraper.page.Login(driver=driver2)
    log.login_1_etapa(username=USERNAME, password=PASSWORD)
    time.sleep(30)

    # Consulta Intimações
    esaj.scraper.page.intim.Consulta(driver=driver2)

    # em_nome = esaj.scraper.page.intim.consulta.EmNomeDe(driver=driver)
    # print(em_nome.get_options())

    time.sleep(5)
    driver2.quit()
