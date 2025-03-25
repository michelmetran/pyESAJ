"""
Módulo com a página de cadastro do eSAJ
Para pegar o que o usuário tem autorização para fazer
"""

from typing import List

from selenium.webdriver.common.by import By

from pyesaj.scraper.params import perfil
from pyesaj.scraper.pom import Page


# flake8: noqa:E501


class GerenciamentoPerfis(Page):
    """
    Página "Cadastro > Gerenciamento de Perfis"
    """

    url = 'https://esaj.tjsp.jus.br/esajperfil/abrirGerenciamentoDePerfis.do'
    perfis = (By.XPATH, '//div[@class="titPerfil"]')

    def __init__(self, driver) -> None:
        super().__init__(driver)
        # Vai para a página
        self.go_to(self.url)

    def obtem_perfis(self) -> List[perfil.Perfil]:
        """
        Obtém perfis de acesso do usuário logado.
        """

        # Itera pelos Perfis
        list_perfis = []
        for item in self.find_all(locator=self.perfis):
            # Define Variáveis
            # Precisei definir aqui pois tem o "item" que é variável
            perfis_atrib = (By.XPATH, './input', item)
            perfis_description = (
                By.XPATH,
                './../div[@class="contPerfil" and @style="display: block;"]',
                item,
            )
            open_profile = (By.XPATH, './/img[@class="setaCima"]', item)
            close_profile = (
                By.XPATH,
                './/img[@class="setaBaixo" and @style="display: inline;"]',
                item,
            )

            # Profile Name
            print(item.text)

            # Pega atributo: se está habilitado
            authorization = self.attribute(
                locator=perfis_atrib, attribute='checked'
            )
            if authorization == 'true':
                authorization_fix = True

            else:
                authorization_fix = False

            # Abre Perfil
            self.click(open_profile)

            # Lê conteúdo: Descrição e Observação
            msg = self.get_text(perfis_description)

            # Ajusta Descrição
            msgs = msg.split('\n', maxsplit=1)
            if isinstance(msgs, list) and len(msgs) > 1:
                desc = msgs[0].strip().strip('\n')
                obs = msgs[1].strip().strip('\n')

            else:
                desc = msg.strip().strip('\n')
                obs = None

            # Fecha Perfil
            self.click(close_profile)

            # Apensa Perfil
            list_perfis.append(
                perfil.Perfil(
                    perfil=item.text,
                    autorizado=authorization_fix,
                    descricao=desc,
                    observacao=obs,
                )
            )

        return list_perfis


class DadosCadastrais(Page):
    """
    Página "Cadastro > Dados Cadastrais"
    """

    url = 'https://esaj.tjsp.jus.br/esajperfil/abrirEdicaoDeDadosDoUsuario.do'
    nome = (By.XPATH, '//input[@id="identity.nmUsuario"]')
    nome_social = (By.XPATH, '//input[@id="identity.nmSocial"]')
    email = (By.XPATH, '//input[@id="identity.deEmail"]')
    email_altenativo = (By.XPATH, '//input[@id="identity.deEmailAlternativo"]')
    cpf = (By.XPATH, '//input[@id="identity.nuCpfCnpj"]')
    rg = (By.XPATH, '//input[@id="identity.nuRg"]')
    rg_orgao_emissor = (By.XPATH, '//input[@id="identity.deOrgaoemissor"]')
    telefone = (By.XPATH, '//input[@id="identity.nuTelefone"]')
    celular = (By.XPATH, '//input[@id="identity.nuCelular"]')
    sexo_masculino = (
        By.XPATH,
        '//input[@id="id_esajperfil.label.usuario.tpGenero.masculino"]',
    )
    sexo_feminino = (
        By.XPATH,
        '//input[@id="id_esajperfil.label.usuario.tpGenero.feminino"]',
    )

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.go_to(url=self.url)

    def obtem_dados(self) -> perfil.Cadastro:
        """
        Obtém dados cadastrais do usuário logado.
        """

        # Sexo
        masc = self.attribute(locator=self.sexo_masculino, attribute='checked')
        fem = self.attribute(locator=self.sexo_feminino, attribute='checked')
        if masc == 'true' and fem is None:
            sexo = 'Masculino'

        elif masc is None and fem == 'true':
            sexo = 'Feminino'

        else:
            sexo = None

        return perfil.Cadastro(
            nome=self.attribute(self.nome, attribute='value'),
            nome_social=self.attribute(self.nome_social, attribute='value'),
            email=self.attribute(self.email, attribute='value'),
            email_alternativo=self.attribute(
                self.email_altenativo, attribute='value'
            ),
            cpf=self.attribute(self.cpf, attribute='value'),
            rg=self.attribute(self.rg, attribute='value'),
            rg_orgao_emissor=self.attribute(
                self.rg_orgao_emissor, attribute='value'
            ),
            telefone=self.attribute(self.telefone, attribute='value'),
            celular=self.attribute(self.celular, attribute='value'),
            genero=sexo,
        )


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
    driver_ff = esaj.scraper.webdriver.Firefox(verify_ssl=False)

    # Entra no eSAJ e loga
    log = esaj.scraper.page.Login(driver=driver_ff)
    log.login(username=USERNAME, password=PASSWORD)

    # Cadastro
    esaj_perfil = esaj.scraper.page.GerenciamentoPerfis(driver=driver_ff)
    perfis = esaj_perfil.obtem_perfis()
    print(perfis)

    dados_cadastrais = esaj.scraper.page.DadosCadastrais(driver=driver_ff)
    dados = dados_cadastrais.obtem_dados()
    print(dados)

    time.sleep(5)
    driver_ff.close()
