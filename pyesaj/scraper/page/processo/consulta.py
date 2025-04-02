"""
Módulo com a página de Consulta de Processos
de 1º e 2º graus

Não precisa, obrigatoriamente, estar logado.
Mas garante melhores permissões.

Os filtros de processos são os mesmos para 1º e 2º graus
Talvez o conteúdo seja diferente.
"""

import warnings
from typing import List, Literal

from selenium.webdriver.common.by import By

from pyesaj.scraper.pom import Page, PageElement


# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


# flake8: noqa:303
# flake8: noqa:E501


class ConsultaProcesso(Page):
    """
    Páginas:
    "Consultas Processuais > Consulta de Processos do 1º Grau"\n
    "Consultas Processuais > Consulta de Processos do 2º Grau"
    """

    url_1grau = 'https://esaj.tjsp.jus.br/cpopg/open.do'
    url_2grau = 'https://esaj.tjsp.jus.br/cposg/open.do'

    def __init__(
        self, driver, grau: Literal['Primeiro Grau', 'Segundo Grau']
    ) -> None:
        super().__init__(driver)

        if grau == 'Primeiro Grau':
            self.go_to(self.url_1grau)

        elif grau == 'Segundo Grau':
            self.go_to(self.url_2grau)

        else:
            raise ValueError("Precisa ser 'Primeiro Grau' ou 'Segundo Grau'")


class ConsultaPor(PageElement):
    """
    Representa o menu *dropdown* "Consulta Por", que define
    qual o tipo de consulta processual que será feita.
    """

    selector_consulta_por = (
        By.XPATH,
        '//form[@name="consultarProcessoForm"]//select[@name="cbPesquisa"]',
    )

    def get_options(self) -> List[str]:
        """
        Obtem opções de preenchimento.
        """

        return self.create_select_options(self.selector_consulta_por)

    def set_option(self, option: str) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        list_options = self.get_options()
        if option not in list_options:
            raise ValueError(f'Precisa ser uma opção {list_options}')

        self.select(self.selector_consulta_por, option)


class NumeroUnificado(PageElement):
    """
    Representa o campo de *input* "Número do Processo",
    no padrão do TJSP.

    Só é possível pesquisar pelo Número do Processo Unificado,
    que contem o ".8.26." ou ".8-26." no meio do número.
    """

    numero_parte1 = (
        By.XPATH,
        '//div[@id="NUMPROC"]//input[@id="numeroDigitoAnoUnificado"]',
    )
    numero_parte3 = (
        By.XPATH,
        '//div[@id="NUMPROC"]//input[@id="foroNumeroUnificado"]',
    )

    def define_numero(self, numero: str) -> None:
        """
        Preenche o Número do Processo Unificado.
        """
        if '.8.26.' in numero:
            numero_split = str(numero).split('.8.26.')

        elif '.8-26.' in numero:
            numero_split = str(numero).split('.8-26.')

        else:
            raise ValueError(
                'O número não tem a sequencia ".8.26." para dividir o número em partes'
            )

        self.set(locator=self.numero_parte1, value=numero_split[0])
        self.set(locator=self.numero_parte3, value=numero_split[1])


class NomeParte(PageElement):
    """
    Representa o campo de *input* "Nome da Parte".
    """

    nome_parte = (By.XPATH, '//input[@id="campo_NMPARTE"]')
    check_box_nome_completo = (
        By.XPATH,
        # '//div[@id="NMPARTE"]//span[@id="pesquisarPorNomeCompleto"]',
        # '//div[@id="NMPARTE"]//span[contains(text(),"Pesquisar por nome completo")]',
        '//div[@id="NMPARTE"]//label',
    )

    def set_nome_parte(self, nome: str) -> None:
        """
        Define o "Nome da parte"
        """
        self.set(locator=self.nome_parte, value=nome)

    def pesquisa_nome_completo(self) -> None:
        """
        Representa o *checkbox* "Pesquisar por nome completo".
        """
        # TODO: Adicionar validação
        self.click(locator=self.check_box_nome_completo)


class DocumentoParte(PageElement):
    """
    Representa o campo de *input* "Documento da Parte".
    """

    nome_parte = (By.XPATH, '//input[@id="campo_DOCPARTE"]')

    def set_documento(self, documento: str) -> None:
        """
        Define "Documento da Parte".
        """
        self.set(locator=self.nome_parte, value=documento)


class NomeAdvogado(PageElement):
    """
    Representa do campo de *input* "Nome do Advogado".
    """

    nome_adv = (By.XPATH, '//input[@id="campo_NMADVOGADO"]')
    check_box_nome_completo = (
        By.XPATH,
        # '//div[@id="NMADVOGADO"]//span[@id="pesquisarPorNomeCompleto"]',
        '//div[@id="NMADVOGADO"]//label',
    )

    def set_nome_adv(self, nome: str) -> None:
        """
        Preenche o campo de *input* "Nome do Advogado".
        """
        self.set(locator=self.nome_adv, value=nome)

    def pesquisa_nome_completo(self) -> None:
        """
        Habilita o *checkbox* "Pesquisar por nome completo".
        """
        # TODO: Ideal fazer uma validação
        self.click(locator=self.check_box_nome_completo)


class OAB(PageElement):
    """
    Representa do campo de *input* "OAB".
    """

    oab = (By.XPATH, '//input[@id="campo_NUMOAB"]')

    def set_documento(self, documento: str) -> None:
        """
        Define a "OAB".
        """
        self.set(locator=self.oab, value=documento)


class NumCartaPrecatoria(PageElement):
    """
    Representa do campo de *input* "Nº da Carta Precatória na Origem".
    """

    nome_parte = (By.XPATH, '//input[@id="campo_PRECATORIA"]')

    def set_documento(self, documento: str) -> None:
        """
        Define o "Nº da Carta Precatória na Origem".
        """
        self.set(locator=self.nome_parte, value=documento)


class NumDocDelegacia(PageElement):
    """
    Representa do campo de *input* "Nº do Documento da Delegacia".
    """

    nome_parte = (By.XPATH, '//input[@id="campo_DOCDELEG"]')

    def set_documento(self, documento: str) -> None:
        """
        Define o "Nº do Documento da Delegacia".
        """
        self.set(locator=self.nome_parte, value=documento)


class CDA(PageElement):
    """
    Representa do campo de *input* "CDA" (Certidão da Dívida Ativa?!).
    """

    nome_parte = (By.XPATH, '//input[@id="campo_NUMCDA"]')

    def set_documento(self, documento: str) -> None:
        """
        Define o "CDA" (Certidão da Dívida Ativa?!).
        """
        self.set(locator=self.nome_parte, value=documento)


class Consultar(PageElement):
    """
    Representa o botão "Consultar"
    """

    btn_consultar_1grau = (
        By.XPATH,
        '//input[@id="botaoConsultarProcessos"]',
    )

    btn_consultar_2grau = (
        By.XPATH,
        '//input[@id="pbConsultar"]',
    )

    def consultar(self, grau: Literal['Primeiro Grau', 'Segundo Grau']) -> None:
        """
        Aperta o botão "Consultar"
        """
        if grau == 'Primeiro Grau':
            self.click(locator=self.btn_consultar_1grau)

        elif grau == 'Segundo Grau':
            self.click(locator=self.btn_consultar_2grau)


class CheckResults(PageElement):
    """
    Avalia o resultado da pesquisa de processos

    """

    msg_results = (
        By.XPATH,
        '//*[contains(text(), "Não existem informações disponíveis para os parâmetros informados.")]',
    )

    def tem_resultado(self) -> bool:
        """
        Avalia o resultado da pesquisa

        - `True` significa que tem regstros
        - `False` significa que NÃO tem regstros
        """
        try:
            # Find Errors
            tags = self.find_all(locator=self.msg_results, wait=3)
            print(tags[0].text)

            # Se tem
            if len(tags) == 1 and (
                tags[0].text
                == 'Não existem informações disponíveis para os parâmetros informados.'
            ):
                # Mensagem
                warnings.warn(
                    message=f'\n'
                            f'A pesquisa não retornou nenhum resultado.\n'
                            f'\n',
                    category=RuntimeWarning,
                )
                # Se encontra a mensagem, significa que não tem resultado
                return False

            else:
                return False

        except:
            # Se não encontra a mensagem, significa que tem resultado!
            return True


if __name__ == '__main__':
    import os
    import time

    from dotenv import load_dotenv

    from pyesaj.scraper import webdriver

    # Credenciais
    load_dotenv()
    USERNAME = os.getenv('USERNAME_TJSP')
    PASSWORD = os.getenv('PASSWORD_TJSP')

    # Cria Driver
    driver2 = webdriver.Firefox(
        # driver_path=paths.driver_path,
        # logs_path=paths.app_logs_path,
        # down_path=paths.driver_path,
        verify_ssl=False,
    )

    # Intimações
    consulta = ConsultaProcesso(driver=driver2, grau='Primeiro Grau')
    # consulta.define_instancia(grau='1º grau')

    # Entra no eSAJ e loga
    # esaj = pyesaj.Login(driver=driver)
    # esaj.login(username=USERNAME, password=PASSWORD)

    # Consultar Por
    por = ConsultaPor(driver=driver2)
    print(por.get_options())
    por.set_option(option='Número do Processo')

    # Número
    num = NumeroUnificado(driver=driver2)
    num.define_numero(numero='0123479-07.2012.8.26.0100')

    # Nome da Parte
    por.set_option(option='Nome da parte')
    nom = NomeParte(driver=driver2)
    nom.set_nome_parte(nome='Michel Metran')
    nom.pesquisa_nome_completo()

    # Documento da Parte
    por.set_option(option='Documento da Parte')
    doc = DocumentoParte(driver=driver2)
    doc.set_documento(documento='324423324')

    # Nome do Advogado
    por.set_option(option='Nome do Advogado')
    adv = NomeAdvogado(driver=driver2)
    adv.set_nome_adv(nome='Zé')
    adv.pesquisa_nome_completo()

    # Nome do Advogado
    por.set_option(option='OAB')
    o = OAB(driver=driver2)
    o.set_documento(documento='324423324')

    # Nº da Carta Precatória na Origem
    por.set_option(option='Nº da Carta Precatória na Origem')
    a2 = NumCartaPrecatoria(driver=driver2)
    a2.set_documento(documento='Cartaprecatoria')

    # Nº do Documento na Delegacia
    por.set_option(option='Nº do Documento na Delegacia')
    a3 = NumDocDelegacia(driver=driver2)
    a3.set_documento(documento='Doc Delegacia')

    # CDA
    por.set_option(option='CDA')
    a4o = CDA(driver=driver2)
    a4o.set_documento(documento='CDA')

    # Nome da Parte
    por.set_option(option='Nome da parte')
    nom = NomeParte(driver=driver2)
    nom.set_nome_parte(nome='Michel Metran')
    nom.pesquisa_nome_completo()

    # Consultar
    con = Consultar(driver=driver2)
    con.consultar()

    time.sleep(2)
    driver2.quit()
