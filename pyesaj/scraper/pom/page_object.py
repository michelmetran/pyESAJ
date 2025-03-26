"""
Módulo com a página base do projeto
utilizando a estrutura de Page Object Model (POM)
"""

import logging
import time
from abc import ABC
from typing import List, Optional, Union

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class SeleniumObject:
    """
    Guarda os métodos do Selenium
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    def go_to(self, url) -> None:
        """
        Abre a página web definida na variável `url`.
        Avalia se o `driver` já está na página solicitada e,
        em caso negativo, acessa a página.
        """
        if self.driver.current_url != url:
            self.driver.get(url)

        # Avalia se entrou na página e ela carregou completamente
        page_state = self.driver.execute_script('return document.readyState;')
        n_try = 0
        while page_state != 'complete' and n_try < 60 * 2:
            time.sleep(1)
            page_state = self.driver.execute_script(
                'return document.readyState;'
            )
            n_try += 1

    def find(self, locator: tuple, wait: float = 60) -> WebElement:
        """
        Encontra algum
        """
        if len(locator) == 2:
            start_point = self.driver

        elif len(locator) == 3:
            start_point = locator[2]
            locator = locator[0:2]

        else:
            raise ValueError('Erro no input da tupla')

        try:
            if wait != 0:
                elem = WebDriverWait(start_point, wait).until(
                    EC.presence_of_element_located((locator))
                )
            else:
                # Asterisco serve para desempacotar os parâmetros de input
                elem = start_point.find_element(*locator)

        except Exception as e:
            logging.error(
                f'e-SAJ parece não ter carregado corretamente os elemento!. Veja erro:\n{e}'
            )

        return elem

    def find_all(self, locator: tuple, wait: int = 60) -> List[WebElement]:
        """
        Encontra todos
        """
        if len(locator) == 2:
            start_point = self.driver

        elif len(locator) == 3:
            start_point = locator[2]
            locator = locator[0:2]

        else:
            raise ValueError('Erro no input da tupla')

        try:
            if wait != 0:
                elem = WebDriverWait(start_point, wait).until(
                    EC.presence_of_all_elements_located((locator))
                )
            else:
                # Asterisco serve para desempacotar os parâmetros de input
                elem = start_point.find_elements(*locator)

        except Exception as e:
            logging.error(
                f'e-SAJ parece não ter carregado corretamente os elemento!. Veja erro:\n{e}'
            )

        return elem

    def set(self, locator, value) -> None:
        """
        Define algum campo para preenchimento

        Vi o conceito de aguardar em:
        https://stackoverflow.com/questions/73169697/how-to-wait-for-text-value-to-show-using-selenium-python
        """
        self.find(locator).clear()
        self.find(locator).send_keys(value)

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value(locator, text_=value)
        )

    def click(self, locator) -> None:
        """
        Clica em algum botão
        """
        self.find(locator).click()

    def get_text(self, locator, *args, **kwargs) -> str:
        """
        Pego text
        """
        wait = kwargs.get('wait', 60)
        try:
            return self.find(locator, wait).text.strip()

        except:
            return None

    def attribute(self, locator, attribute):
        """
        Pega atributo
        """
        return self.find(locator).get_attribute(attribute)

    def create_select_options(
        self,
        locator,
        options_delete: Union[Optional[str], Optional[List[str]]] = None,
    ) -> List[str]:
        """
        Cria uma lista das opções em forma de texto
        É possível passar parâmetro opções para excluir itens da lista
        """
        try:
            selector = Select(self.find(locator))
            list_options = [x.text for x in selector.options]

        except Exception as e:
            logging.error(f'e-SAJ não carregou opções. Erro  {e}')

        if options_delete is None:
            options_delete = ['-- Selecione --', '']

        elif isinstance(options_delete, list):
            options_delete.extend(['-- Selecione --', ''])

        list_options = list(
            set([x for x in list_options if x not in options_delete])
        )
        list_options.sort()
        return list_options

    def select(self, locator, option) -> None:
        """
        Seleciona uma opção
        """
        selector = Select(self.find(locator))
        selector.select_by_visible_text(option)

    def switch(self, locator) -> None:
        """
        _summary_
        """
        iframe_xpath = self.find(locator)
        self.driver.switch_to.frame(iframe_xpath)

    def switch_back(self) -> None:
        """
        _summary_
        """
        self.driver.switch_to.default_content()

    def zoom(self, zoom):
        self.driver.execute_script(f"document.body.style.zoom='{zoom}%'")

    def script(self, script, *arg):
        self.driver.execute_script(script, *arg)


class Page(ABC, SeleniumObject):
    """
    Modelo Padrão de Página
    """

    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver
        # self._reflection()

    # def _reflection(self):
    #     """
    #     Define qual o driver nos PageElements
    #     """
    #     for atributo in dir(self):
    #         atributo_real = getattr(self, atributo)
    #         print(atributo, atributo_real)
    #         if isinstance(atributo_real, PageElement):
    #             atributo_real.driver = self.driver


class PageElement(ABC, SeleniumObject):
    """
    Modelo Padrão dos Elementos das Páginas
    """

    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver


if __name__ == '__main__':
    import time

    from selenium.webdriver.common.by import By

    from pyesaj import webdriver

    #
    my_driver = webdriver.Firefox(
        # driver_path=paths.driver_path,
        # logs_path=paths.app_logs_path,
        # down_path=paths.driver_path,
        verify_ssl=False,
    )

    my_driver.get('https://www.youtube.com/watch?v=KM90nnkt-5w')
    print('-' * 100)

    #
    page = Page(driver=my_driver)
    page.go_to('https://www.youtube.com/')

    page.find(locator=(By.XPATH, '//div'))

    time.sleep(2)
    my_driver.quit()
