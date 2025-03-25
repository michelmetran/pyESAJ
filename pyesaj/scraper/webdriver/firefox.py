"""
Módulo para usar driver do FireFox

Michel Metran
Data: mar.2023
Atualizado em: mar.2023
"""

import tempfile
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from pyesaj.scraper.webdriver import config
from pyesaj.scraper.webdriver import gecko


class Firefox(webdriver.Firefox):
    """
    Cria driver customizado do Selenium

    :param webdriver: _description_
    :type webdriver: _type_
    """

    def __init__(
            self,
            # driver_path: Path,
            # logs_path: Path,
            # down_path: Path,
            *args,
            **kwargs,
    ):
        """
        - verify_ssl
        - headless
        - download_path

        :param my_driver_path: _description_
        :type my_driver_path: pathlib
        :param my_logs_path: _description_
        :type my_logs_path: pathlib
        """

        # Parameters
        verify_ssl = kwargs.get('verify_ssl', True)
        headless = kwargs.get('headless', False)
        self.download_path = kwargs.get('download_path', False)

        # Temp Path
        temp_path = tempfile.gettempdir()
        project_temp_path = Path(temp_path) / config.TEMP_PATH_NAME

        # Scrapy Path
        scrapy_path = project_temp_path / 'scrapy'
        scrapy_path.mkdir(exist_ok=True, parents=True)

        # Driver Path
        self.driver_path = scrapy_path / 'driver'
        self.driver_path.mkdir(exist_ok=True, parents=True)

        # Logs Path
        self.logs_path = scrapy_path / 'logs'
        self.logs_path.mkdir(exist_ok=True, parents=True)

        # Services
        geckodriver = gecko.Gecko()
        gecko_path = geckodriver.get_path_geckodriver(verify_ssl=verify_ssl)

        # Logs
        logs_filepath = self.logs_path / 'geckodriver.log'

        # Services
        my_service = FirefoxService(
            executable_path=gecko_path, log_path=logs_filepath
        )

        # Options
        my_options = FirefoxOptions()
        if headless:
            my_options.add_argument('--headless')

        # Download Path
        if self.download_path is False:
            # Cria Pasta
            self.download_path = scrapy_path / 'download'
            self.download_path.mkdir(exist_ok=True, parents=True)

        # Define pasta de Download
        my_options.set_preference(
            'browser.download.dir', str(self.download_path)
        )

        my_options.set_preference('intl.accept_languages', 'pt-BR, pt')
        my_options.set_preference('browser.download.folderList', 2)
        my_options.set_preference(
            'browser.download.manager.showWhenStarting', False
        )
        my_options.set_preference('pdfjs.disabled', True)
        my_options.set_preference('plugin.scan.Acrobat', '99.0')
        my_options.set_preference('plugin.scan.plid.all', False)
        my_options.set_preference(
            'browser.helperApps.showOpenOptionForPdfJS', False
        )
        my_options.set_preference('browser.download.forbid_open_with', True)
        my_options.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'application/octet-stream, application/pdf',
        )
        # Quando é necessário fazer repost about: config
        # https://superuser.com/questions/1410598/disable-firefox-must-send-information-that-will-repeat-any-action-dialog-box
        my_options.set_preference(
            'dom.confirm_repost.testing.always_accept', True
        )

        # Driver
        # my_driver = super(Driver, self)
        # my_driver.__init__(service=my_service, options=my_options)
        super().__init__(service=my_service, options=my_options)
        self.maximize_window()

    def add_extension_xpath(self) -> None:
        """
        Adiciona xPath extension
        """

        # Temp Path
        temp_path = tempfile.gettempdir()
        project_temp_path = Path(temp_path) / config.TEMP_PATH_NAME

        # Scrapy Path
        scrapy_path = project_temp_path / 'scrapy'
        scrapy_path.mkdir(exist_ok=True, parents=True)

        # Adds Path
        adds_path = scrapy_path / 'adds'
        adds_path.mkdir(exist_ok=True, parents=True)

        # Add-ons Xpath
        xpath_path = adds_path / 'xpath.xpi'
        xpath_path = xpath_path.absolute().resolve()

        # Download
        if not xpath_path.is_file():
            r = requests.get(
                url=config.URL_ADDONS_XPATH, timeout=60, verify=False
            )

            with open(xpath_path, 'wb') as f:
                f.write(r.content)

        # Add
        self.install_addon(str(xpath_path), temporary=True)


if __name__ == '__main__':
    import time

    # from pyesaj import paths

    # Instancia Driver
    driver = Firefox(headless=False, verify_ssl=False, )

    # Add xPath Extension
    driver.add_extension_xpath()

    driver.get(url='https://www.uol.com.br/')
    time.sleep(3)
    driver.quit()

    gecko = gecko.Gecko()
    gecko_p = gecko.get_path_geckodriver()
    print(gecko_p)
