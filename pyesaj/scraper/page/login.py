"""
Módulo com a página de login
"""

from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from pyesaj.scraper.pom import Page, PageElement


class Username(PageElement):
    """
    Representa o campo de *input* "CPF/CNPJ",
    necessário para acessar o e-SAJ.
    """

    input_username = (By.XPATH, '//input[@id="usernameForm"]')
    nome_usuario = (By.XPATH, '//span[@id="identificacao"]/strong')

    def set_username(self, username: str) -> None:
        """
        Define o "usuário" para logar no e-SAJ.
        """
        self.set(self.input_username, username)

    def get_username(self) -> str:
        """
        Obtem o "usuário" logado no e-SAJ.
        """
        return self.get_text(self.nome_usuario)


class Password(PageElement):
    """
    Representa o campo de *input* "Senha", necessário para acessar
    o e-SAJ.
    """

    input_password = (By.XPATH, '//input[@id="passwordForm"]')

    def set_password(self, password) -> None:
        """
        Define a "senha" para logar no e-SAJ.
        """
        self.set(self.input_password, password)


class Token(PageElement):
    """
    Representa o campo de *input* "Senha", necessário para acessar
    o e-SAJ.
    """

    input_token = (By.XPATH, '//input[@id="tokenInformado"]')

    def set_token(self, token) -> None:
        """
        Define a "senha" para logar no e-SAJ.
        """
        self.set(self.input_token, token)


class Login(Page):
    """
    Página "eSAJ > Login"
    https://esaj.tjsp.jus.br/sajcas/login
    """

    url = 'https://esaj.tjsp.jus.br/esaj/portal.do?servico=740000'
    identificar_se = (By.XPATH, "//a[text()='Identificar-se']")
    btn_entrar = (By.XPATH, '//input[@id="pbEntrar"]')
    btn_enviar_token = (By.XPATH, '//button[@id="btnEnviarToken"]')

    msg_login = (
        By.XPATH,
        '//table[@class="tabelaMensagem"]//td[@id="mensagemRetorno"]',
    )
    msg_token = (
        By.XPATH,
        '//div[@id="avisoTokenInvalido"]',
    )

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.go_to(url=self.url)
        self.user = None

    def login_1_etapa(self, username, password) -> None:
        user = Username(self.driver)
        passwd = Password(self.driver)

        if user.get_username() == 'Identificar-se':
            # Clica em Identificar-se
            self.click(self.identificar_se)

            # Insere Parâmetros
            user.set_username(username=username)
            passwd.set_password(password=password)

            # Faz o Login
            self.click(self.btn_entrar)

        else:
            # Define Variável
            self.user = user.get_username()

            # Mensagem
            print(f'Olá "{self.user}", você já estava logado no e-SAJ!')

    def login_2_etapa(self, token: int | str) -> None:
        user = Username(self.driver)
        token_obj = Token(self.driver)

        if user.get_username() == 'Identificar-se':
            # Define o Token
            token_obj.set_token(token=str(token))

            # Clica em "Enviar" token
            self.click(self.btn_enviar_token)

            # Tentativa de trabalhar com a inserção de um token errado
            # try:
            #     msg = self.get_text(locator=self.msg_token, wait=3)
            # except:
            #     msg = ''
            #
            # if msg == 'O código informado está inválido. Verifique sua caixa de e-mail para conferir o código que foi enviado ou tente reenviar o código novamente.':
            #     raise Exception(msg)

            # Define Variável
            self.user = user.get_username()

            # Pega URL
            path = urlparse(url=self.driver.current_url).path

            # Se logou!
            if path == '/esaj/portal.do':
                print(f'Olá "{self.user}", você está logado no e-SAJ!')

            # Se não logou!
            elif path == '/sajcas/login':
                msg = self.get_text(locator=self.msg_login)
                if msg == 'Usuário e/ou senha inválidos':
                    raise Exception(msg)

        else:
            # Define Variável
            self.user = user.get_username()

            # Mensagem
            print(f'Olá "{self.user}", você já estava logado no e-SAJ!')

    # def login(self, username, password) -> None:
    #     """
    #     Faz o login
    #     Usado até 24/03/2025, quando não havia login em duas etapas
    #     """
    #
    #     user = Username(self.driver)
    #     passwd = Password(self.driver)
    #
    #     if user.get_username() == 'Identificar-se':
    #         # Clica em Identificar-se
    #         self.click(self.identificar_se)
    #
    #         # Insere Parâmetros
    #         user.set_username(username=username)
    #         passwd.set_password(password=password)
    #
    #         # Faz o Login
    #         self.click(self.btn_entrar)
    #
    #         # Define Variável
    #         self.user = user.get_username()
    #
    #         # Pega URL
    #         path = urlparse(url=self.driver.current_url).path
    #
    #         # Se logou!
    #         if path == '/esaj/portal.do':
    #             print(f'Olá "{self.user}", você está logado no e-SAJ!')
    #
    #         # Se não logou!
    #         elif path == '/sajcas/login':
    #             msg = self.get_text(locator=self.msg_login)
    #             if msg == 'Usuário e/ou senha inválidos':
    #                 raise Exception(msg)
    #
    #     else:
    #         # Define Variável
    #         self.user = user.get_username()
    #
    #         # Mensagem
    #         print(f'Olá "{self.user}", você já estava logado no e-SAJ!')


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
    driver2 = esaj.scraper.webdriver.Firefox(
        # driver_path=paths.driver_path,
        # logs_path=paths.app_logs_path,
        # down_path=paths.driver_path,
        # headless=False,
        verify_ssl=False
    )

    # Faz Login
    log = esaj.scraper.page.Login(driver=driver2)

    # Não é mais usado
    # log.login(username=USERNAME, password=PASSWORD)

    # Etapa 1
    log.login_1_etapa(username=USERNAME, password=PASSWORD)

    # Etapa 2
    log.login_2_etapa(token=365745)

    # Username(driver).set_username(username=USERNAME)

    time.sleep(1)
    # print('Agora eu dou refresh')
    # driver2.refresh()

    print('Agora eu fecho')
    driver2.quit()
