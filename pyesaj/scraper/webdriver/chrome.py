"""
Módulo para usar driver do Chrome

Michel Metran
Data: 24.10.2024
Atualizado em: 24.10.2024
"""

import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pathlib import Path
from pyesaj.scraper.webdriver import config

# from selenium.webdriver.chrome.service import Service as ChromeService


class Chrome(webdriver.Chrome):
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
        """
        # Parameters
        headless = kwargs.get('headless', False)
        self.download_path = kwargs.get('download_path', False)

        # Temp Path
        temp_path = tempfile.gettempdir()
        project_temp_path = Path(temp_path) / config.TEMP_PATH_NAME

        # Scrapy Path
        scrapy_path = project_temp_path / 'scrapy'
        scrapy_path.mkdir(exist_ok=True, parents=True)

        # Download Path
        if self.download_path is False:
            # Cria Pasta
            self.download_path = scrapy_path / 'download'
            self.download_path.mkdir(exist_ok=True, parents=True)

        # my_service = ChromeService()
        # print(str(self.download_path))
        # print(self.download_path)
        # print(self.download_path.is_dir())
        # print(str(self.download_path) + os.path.sep)

        # Options
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')

        # Se tem Modo Anônimo, o download não funciona adequadamente
        # options.add_argument('--incognito')

        # Certificados
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        # options.add_argument('--disable-logging')
        # Remove a mensagem "Chrome is being controlled by automated test software"
        # que aparece quando o Chrome é iniciado pelo Selenium.
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        # Desativa a extensão de automação do Chrome que é carregada por
        # padrão quando o Chrome é iniciado pelo Selenium.
        # Isso ajuda a evitar que sites detectem que o navegador está
        # sendo controlado por um script de automação.
        options.add_experimental_option('useAutomationExtension', False)

        options.add_experimental_option(
            'prefs',
            {
                'credentials_enable_service': False,
                'profile.password_manager_enabled': False,
                'download.default_directory': str(self.download_path),
                # + os.path.sep,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
            },
        )

        if headless is True:
            options.add_argument('--headless')

        super().__init__(
            # service=my_service,
            options=options
        )
        self.maximize_window()


if __name__ == '__main__':
    from pathlib import Path

    from selenium.webdriver.common.by import By

    import pyesaj as esaj

    # # Credenciais
    # load_dotenv()
    # USERNAME = os.getenv('USERNAME_TJSP')
    # PASSWORD = os.getenv('PASSWORD_TJSP')
    # Instancia Driver
    driver = esaj.webdriver.Chrome(headless=False)

    driver.get(url='https://filesamples.com/formats/csv')

    print('vai pra botão')
    btn = driver.find_element(
        By.XPATH, '//a[@href="/samples/document/csv/sample4.csv"]'
    )
    print('clica!')
    btn.click()

    # # Login
    # log = esaj.page.Login(driver=driver)
    # log.login(username=USERNAME, password=PASSWORD)

    # # Intimações
    # processo = '2336412-80.2024.8.26.0000'

    # # Define
    # intim_search = esaj.params.intim.input.ConsultaIntimacoes(
    #     em_nome_de='Ministério Público do Estado de São Paulo',
    #     instancia='Segundo Grau',
    #     # secao='Direito Criminal',
    #     # orgao_julgador='17ª Câmara de Direito Privado B',
    #     # especializacao='Criminal',
    #     # especializacao_nao_definida=True,
    #     # cargo='Secretaria ProcCriminal',
    #     # cargo_nao_definido=True,
    #     # assunto_principal='10527 - Livros / Jornais / Periódicos',
    #     area='Ambas',
    #     ciencia_ato='Todos',
    #     natureza_comunicacao='Ambas',
    #     situacao='Ambas',
    #     processo=processo,
    # )

    # dados = intim_search
    # print(intim_search)

    # # Vai para página
    # esaj.page.intim.Consulta(driver=driver)

    # # Atributo: Em Nome De
    # if dados.em_nome_de is not None:
    #     intim_em_nome = esaj.page.intim.EmNomeDe(driver=driver)
    #     intim_em_nome.set_option(option=dados.em_nome_de)

    # # Atributo: Tipo de Participação
    # if dados.tipo_participacao is not None:
    #     intim_tipo = esaj.page.intim.TipoParticipacao(driver=driver)
    #     intim_tipo.set_option(option=dados.tipo_participacao)

    # # Atributo: Instância
    # if dados.instancia is not None:
    #     intim_inst = esaj.page.intim.Instancia(driver=driver)
    #     intim_inst.set_option(instancia=dados.instancia)

    # # Atributo: Foro
    # if dados.foro is not None:
    #     intim_foro = esaj.page.intim.Foro(driver=driver)
    #     intim_foro.set_option(option=dados.foro)

    # # Atributo: Vara
    # if dados.vara is not None:
    #     intim_vara = esaj.page.intim.Vara(driver=driver)
    #     intim_vara.set_option(option=dados.vara)

    # # Atributo: Seção
    # if dados.secao is not None:
    #     intim_secao = esaj.page.intim.Secao(driver=driver)
    #     intim_secao.set_option(option=dados.secao)

    # # Atributo: Órgão Julgador
    # if dados.orgao_julgador is not None:
    #     intim_org = esaj.page.intim.OrgaoJulgador(driver=driver)
    #     intim_org.set_option(option=dados.orgao_julgador)

    # # Atributo: Especialização
    # if dados.especializacao is not None:
    #     intim_esp = esaj.page.intim.Especializacao(driver=driver)
    #     intim_esp.set_option(option=dados.especializacao)

    # # Atributo: Especialização Checkbox
    # if dados.especializacao_nao_definida is True:
    #     intim_esp = esaj.page.intim.Especializacao(driver=driver)
    #     intim_esp.apenas_processos_sem_especializacao()

    # # Atributo: Cargo
    # if dados.cargo is not None:
    #     intim_cargo = esaj.page.intim.Cargo(driver=driver)
    #     intim_cargo.set_option(option=dados.cargo)

    # # Atributo: Cargo Checkbox
    # if dados.especializacao_nao_definida is True:
    #     intim_cargo = esaj.page.intim.Cargo(driver=driver)
    #     intim_cargo.apenas_processos_sem_cargo()

    # # Atributo: Classe
    # if dados.classe is not None:
    #     intim_classe = esaj.page.intim.Classe(driver=driver)
    #     intim_classe.set_option(option=dados.classe)

    # # Atributo: Assunto Principal
    # if dados.assunto_principal is not None:
    #     intim_assunto = esaj.page.intim.AssuntoPrincipal(driver=driver)
    #     intim_assunto.set_option(option=dados.assunto_principal)

    # # Atributo: Área
    # if dados.area is not None:
    #     intim_area = esaj.page.intim.Area(driver=driver)
    #     intim_area.set_option(option=dados.area)

    # # Período: De
    # if dados.periodo_de is not None:
    #     intim_per = esaj.page.intim.consulta.Periodo(driver=driver)
    #     intim_per.de(data=dados.periodo_de)

    # # Período: Até
    # if dados.periodo_ate is not None:
    #     intim_per = esaj.page.intim.consulta.Periodo(driver=driver)
    #     intim_per.ate(data=dados.periodo_ate)

    # # Período: Intervalo
    # if dados.periodo_de is not None and dados.periodo_ate is not None:
    #     intim_per = esaj.page.intim.consulta.Periodo(driver=driver)
    #     intim_per.define_intervalo(de=dados.periodo_de, ate=dados.periodo_ate)

    # # Atributo: Processo
    # if dados.processo is not None:
    #     intim_proc = esaj.page.intim.Processo(driver=driver)
    #     intim_proc.write(texto=dados.processo)

    # # Atributo: Ciência do Ato
    # if dados.ciencia_ato is not None:
    #     intim_cien = esaj.page.intim.consulta.CienciaAto(driver=driver)
    #     intim_cien.set_option(option=dados.ciencia_ato)

    # # Atributo: Natureza de Comunicação
    # if dados.natureza_comunicacao is not None:
    #     intim_nat = esaj.page.intim.NaturezaComunicacao(driver=driver)
    #     intim_nat.set_option(natureza=dados.natureza_comunicacao)

    # # Atributo: Situação
    # if dados.situacao is not None:
    #     intim_sit = esaj.page.intim.consulta.Situacao(driver=driver)
    #     intim_sit.set_option(situacao=dados.situacao)

    # # Aguarda
    # time.sleep(2)

    # # Consulta
    # consulta = esaj.page.intim.ConsultarIntimacoes(driver=driver)
    # consulta.consultar()

    # # Tabela
    # tab = esaj.page.intim.Tabela(driver=driver)
    # tab.get_table(
    #     # instancia=instancia,
    #     seleciona_processos=[processo],
    # )

    # acao = esaj.page.intim.Acoes(driver=driver)
    # csv_filepath = acao.export_csv()
    # print(csv_filepath)

    # driver.quit()
