"""
_summary_

:raises Exception: _description_
:return: _description_
:rtype: _type_
"""

import platform
import tarfile
import tempfile
from pathlib import Path
from zipfile import ZipFile

import requests

from pyesaj.scraper.webdriver import config


class Gecko:
    """
    _summary_
    """

    def __init__(self) -> None:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """

        # Temp Path
        temp_path = tempfile.gettempdir()
        project_temp_path = Path(temp_path) / config.TEMP_PATH_NAME

        # Scrapy Path
        scrapy_path = project_temp_path / 'scrapy'
        scrapy_path.mkdir(exist_ok=True, parents=True)

        # Driver Path
        self.driver_path = scrapy_path / 'driver'
        self.driver_path.mkdir(exist_ok=True, parents=True)

        # Drivers por Sistema Operacional
        if platform.system() == 'Windows':
            gecko_win_filepath = self.driver_path / 'geckodriver.exe'
            if gecko_win_filepath.is_file():
                self.has_geckodriver = True

            elif not gecko_win_filepath.is_file():
                self.has_geckodriver = False

        elif platform.system() == 'Linux':
            gecko_linux_filepath = self.driver_path / 'geckodriver'
            if gecko_linux_filepath.is_file():
                self.has_geckodriver = True

            elif not gecko_linux_filepath.is_file():
                self.has_geckodriver = False

    def _get_geckodriver(self, verify_ssl: bool):
        """
        Faz o download do geckodriver!

        :return:
        """

        # print(gecko_zip_filepath)
        if not self.has_geckodriver:
            if platform.system() == 'Windows':
                # Download do geckodriver
                r = requests.get(
                    config.URL_GECKODRIVER_WINDOWS,
                    timeout=60,
                    verify=verify_ssl,
                )

                # Save
                name_gecko = Path(config.URL_GECKODRIVER_WINDOWS).name
                gecko_zip_filepath = self.driver_path / name_gecko
                with open(gecko_zip_filepath, 'wb') as f:
                    f.write(r.content)

                # Extract
                with ZipFile(gecko_zip_filepath, 'r') as zip_ref:
                    zip_ref.extractall(self.driver_path)

            elif platform.system() == 'Linux':
                # Download do geckodriver
                r = requests.get(
                    config.URL_GECKODRIVER_LINUX, timeout=60, verify=verify_ssl
                )

                # Save
                name_gecko = Path(config.URL_GECKODRIVER_LINUX).name
                gecko_zip_filepath = self.driver_path / name_gecko
                with open(gecko_zip_filepath, 'wb') as f:
                    f.write(r.content)

                # Extract
                with tarfile.open(gecko_zip_filepath, 'r') as tar_ref:
                    tar_ref.extractall(self.driver_path)

        elif self.has_geckodriver:
            print(f'Geckodriver already in {self.driver_path}')

    def get_path_geckodriver(self, verify_ssl: bool = False) -> Path | str:
        """
        dddd
        """

        # Faz download se for necessário
        self._get_geckodriver(verify_ssl=verify_ssl)

        # Path
        if platform.system() == 'Windows':
            _gecko_path = self.driver_path / 'geckodriver.exe'
            _gecko_path = _gecko_path.resolve().as_posix().replace('/', '\\')
            return _gecko_path

        elif platform.system() == 'Linux':
            _gecko_path = self.driver_path / 'geckodriver'
            return _gecko_path

        else:
            raise Exception(f'Ajustar para plataforma {platform.system()}')


if __name__ == '__main__':
    import time

    from pyesaj import webdriver

    # Instancia Driver
    driver = webdriver.Firefox(
        # driver_path=paths.driver_path,
        # logs_path=paths.app_logs_path,
        # down_path=paths.driver_path,
        headless=False,
        verify_ssl=False,
    )
    # Add xPath Extension
    driver.add_extension_xpath()
    driver.get(url='https://www.uol.com.br/')
    time.sleep(3)
    driver.quit()

    gecko = Gecko()
    gecko_path = gecko.get_path_geckodriver()
    print(gecko_path)
