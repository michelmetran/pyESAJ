"""
Módulo com a página de
"Definir especialização/cargo"
"""

import time
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from pyesaj.scraper.page.components.components import InputModelSearchSet
from pyesaj.scraper.pom import PageElement

# flake8: noqa:303
# flake8: noqa:E501


# class Define(Page):
#     """
#     Página "Intimações On-line > Definir especialização/cargo"
#     """

#     url = 'https://esaj.tjsp.jus.br/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosNaoRecebidosSelecionados.do'

#     def __init__(self, driver):
#         super().__init__(driver)
#         self.go_to(self.url)


class Especializacao(InputModelSearchSet):
    """
    Representa o campo de *input* "Especialização", para definir
    qual a Especialização que a intimação receberá.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td/input[@id="especialidade.nmEspecialidade"]/../following-sibling::td//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="nmEspecialidade"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.nmEspecialidade"]')
        self.lista_opcoes = None

        # Confere se está na página Correta
        path = urlparse(url=self.driver.current_url).path
        if path not in [
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosRecebidosSelecionados.do',
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosNaoRecebidosSelecionados.do',
            # Chega nessa situação/url após dar dois cliques em "Confirmar". 26.11.2024
            '/intimacoesweb/cadastrarEspecialidade.do',
        ]:
            raise Exception(
                'Necessário estar na página "Definir especialização/cargo"'
            )


class Cargo(InputModelSearchSet):
    """
    Representa o campo de *input* "Cargo", para definir
    qual o Cargo que a intimação receberá.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td/input[@id="cargo.deCargo"]/../following-sibling::td//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="deCargo"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.deCargo"]')
        self.lista_opcoes = None

        # Confere se está na página Correta
        path = urlparse(url=self.driver.current_url).path
        if path not in [
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosRecebidosSelecionados.do',
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosNaoRecebidosSelecionados.do',
        ]:
            raise Exception(
                'Necessário estar na página "Definir especialização/cargo"'
            )


class Acoes(PageElement):
    """
    Represante os botões que promovem "Ações", tais como:
    - Confirmar
    - Voltar
    """

    btn_confirmar = (
        By.XPATH,
        '//table[@class="secaoBotoesBody"]//input[@id="definirEspecialidade" and @value="Confirmar"]',
    )
    btn_voltar = (
        By.XPATH,
        '//table[@class="secaoBotoesBody"]//input[@id="voltar"]',
    )

    def confirmar(self) -> None:
        """
        Aperta botão "Confirmar" para definir especialização e cargo indicados.
        """
        self.click(self.btn_confirmar)

    # def voltar(self) -> None:
    #     """
    #     Aperta botão "Voltar".
    #     """
    #     # TODO: Enquanto não chegar na página de volta
    #     path = urlparse(url=self.driver.current_url).path
    #     url_que_desejo_chegar = path in [
    #         '/intimacoesweb/consultarAtosNaoRecebidos.do',
    #         # TODO: Confirmar
    #         # Chute que é essa URL do menu "Consulta"
    #         '/intimacoesweb/consultarAtosRecebidos.do',
    #     ]
    #     # Clica
    #     self.click(self.btn_voltar)

    #     # Aguarda
    #     time.sleep(0.5)

    #     i = 0
    #     while url_que_desejo_chegar is not True and i <= 10:
    #         try:
    #             # Clica pra voltar novamente
    #             self.click(self.btn_voltar)
    #         except:
    #             pass

    #         # Aguarda
    #         time.sleep(0.5)

    #         # Recheck
    #         path = urlparse(url=self.driver.current_url).path
    #         url_que_desejo_chegar = path in [
    #             '/intimacoesweb/consultarAtosNaoRecebidos.do',
    #             # TODO: Confirmar
    #             # Chute que é essa URL do menu "Consulta"
    #             '/intimacoesweb/consultarAtosRecebidos.do',
    #         ]
    #         i += 1

    def voltar(self) -> None:
        """
        Aperta botão "Voltar".
        """

        def url_desejada(path) -> bool:
            """
            Avalia se estou na url que desejo ao apertar o botão voltar
            """
            return path in [
                '/intimacoesweb/consultarAtosNaoRecebidos.do',
                '/intimacoesweb/consultarAtosRecebidos.do',
            ]

        # Clica
        self.click(self.btn_voltar)
        time.sleep(0.5)

        i = 0
        while (
            not url_desejada(urlparse(url=self.driver.current_url).path)
            and i <= 10
        ):
            try:
                self.click(self.btn_voltar)
            except Exception as e:
                print(f"Erro ao clicar no botão voltar: {e}")

            time.sleep(0.5)
            i += 1


class Mensagem(PageElement):
    """
    Representa a mensagem após especializar,
    ou seja, após apertar o botão "confirmar".
    """

    msg = (
        By.XPATH,
        '//div[@id="spwTabelaMensagem"]//td[@id="mensagemRetorno"]',
    )

    def __init__(self, driver):
        super().__init__(driver)

        # Confere se está na página Correta
        path = urlparse(url=self.driver.current_url).path
        if path not in [
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosRecebidosSelecionados.do',
            '/intimacoesweb/abrirTelaDeDefinicaoEspecialidadeParaAtosNaoRecebidosSelecionados.do',
        ]:
            raise Exception(
                f'Necessário estar na página "Definir especialização/cargo"\nEstou na url\n{path}'
            )

    def get_msg(self) -> str:
        """
        Obtém a mensagem após especializar
        Caso não encontre banner, retornará "False".
        """
        try:
            return self.get_text(locator=self.msg)

        except:
            # Não encontrou sequer o banner
            return False

    def sucesso(self) -> bool:
        """
        Avalia se a especialização foi feita com sucesso.
        """
        return self.get_msg() == 'Operação realizada com sucesso'


if __name__ == '__main__':
    pass
