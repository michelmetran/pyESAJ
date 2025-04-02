"""
Módulo para componentes que estão em ambas páginas
Constam tanto em "Consulta de Intimações"
Constam também em "Recebimento de Intimações"
"""

import tempfile
import time
import logging
from pathlib import Path
from typing import List, Literal
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from pyesaj.scraper.params.intim.output import RecebimentoIntimacoes1Grau, \
    RecebimentoIntimacoes2Grau, ConsultaIntimacoes2Grau
from pyesaj.scraper.page.components.components import (
    InputModelSearchSet,
    InputModelTree,
)
from pyesaj.scraper.pom import PageElement

from pyesaj.scraper.webdriver import config
from pyesaj.scraper.outros.logger import disable_logging, \
    disable_logging_property


# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


# flake8: noqa:303
# flake8: noqa:E501


class EmNomeDe(PageElement):
    """
    Representa o menu *dropdown* "Em nome de", que define
    qual o perfil do usuário que será utilizado.

    Pode ser pesquisa de intimações recebidas pelo nome do usuário,
    pessoa física, ou a pesquisa pelo
    "Ministério Público do Estado de São Paulo",
    caso o usuário seja funcionário dessa instituição.
    """

    selector_em_nome_de = (By.XPATH, '//select[@id="comboUsuarioReferencia"]')

    def get_options(self) -> List[str]:
        """
        Obtêm opções de preenchimento.
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


class TipoParticipacao(PageElement):
    """
    Representa o campo de *input* "Tipo de Participação", que define
    com qual perfil o usuário fará a consulta.

    A opção desse campo depende da opção selecionada no campo "Em nome de".
    Caso tenha sido definido "Ministério Público do Estado de São Paulo",
    não há necessidade de definir o "Tipo de Participação".
    """

    selector_tipo_participacao = (
        By.XPATH,
        '//select[@id="comboTipoParticipacao"]',
    )

    def __init__(self, driver) -> None:
        super().__init__(driver)
        # self.selector_tipo_participacao =

    def get_options(self, options_delete=None) -> List[str]:
        """
        Obtem opções de preenchimento.
        """
        return self.create_select_options(
            self.selector_tipo_participacao, options_delete
        )

    def set_option(self, option) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        list_options = self.get_options()
        if len(list_options) == 0:
            msg = 'Não há campo "Tipo de Participação" para esse usuário!'
            print(msg)
            # logging.info(msg)

        elif option not in list_options:
            raise ValueError(f'Precisa ser uma opção {list_options}.')

        else:
            self.select(locator=self.selector_tipo_participacao, option=option)


class Instancia(PageElement):
    """
    Representa o *radio button* "Instância".
    """

    grau1_xpath = (By.XPATH, '//input[@id="primeiroGrau"]')
    grau2_xpath = (By.XPATH, '//input[@id="segundoGrau"]')
    grau3_xpath = (By.XPATH, '//input[@id="turmasRecursais"]')

    btn_consultar = (By.XPATH, '//input[@id="pbConsultar"]')
    label_foro_secao = (By.XPATH, '//td[@id="labelForo"]/label')

    def get_selected_option(
        self,
    ) -> (
        Literal['Primeiro Grau']
        | Literal['Segundo Grau']
        | Literal['Turmas Recursais']
    ):
        """
        Obtém instância selecionada.
        """
        # Pega Atributos
        check_1 = self.attribute(locator=self.grau1_xpath, attribute='checked')
        check_2 = self.attribute(locator=self.grau2_xpath, attribute='checked')
        check_3 = self.attribute(locator=self.grau3_xpath, attribute='checked')

        # Avalia quem está com atributo "checked"
        if check_1 is not None:
            return 'Primeiro Grau'

        elif check_2 is not None:
            return 'Segundo Grau'

        elif check_3 is not None:
            return 'Turmas Recursais'

        else:
            raise ValueError(
                'Aparentemente, não há nenhuma instância habilitada.'
            )

    def _get_xpath_instance(
        self,
        instancia: Literal['Primeiro Grau', 'Segundo Grau', 'Turmas Recursais'],
    ):
        """
        Determina qual o xPath de interesse
        Função Privada.
        """
        # instancia = self.get_selected_option()
        # print(f'Instância definida como: {instancia}')

        # Pega o xPath selecionado
        if instancia == 'Primeiro Grau':
            instancia_xpath = self.find(self.grau1_xpath)

        elif instancia == 'Segundo Grau':
            instancia_xpath = self.find(self.grau2_xpath)

        elif instancia == 'Turmas Recursais':
            instancia_xpath = self.find(self.grau3_xpath)

        else:
            raise Exception(f'A instância selecionado é {instancia}')

        return instancia_xpath

    def check_available(
        self,
        instancia: Literal['Primeiro Grau', 'Segundo Grau', 'Turmas Recursais'],
    ):
        """
        Avalia se a opção está disponível para o usuário logado.
        Pode haver instâncias não disponíveis
        """
        time.sleep(1)
        instancia_xpath = self._get_xpath_instance(instancia=instancia)
        # instancia = self.get_selected_option()
        # Valida permissões
        # if self.attribute(instancia_xpath, 'disabled') == 'true':
        if instancia_xpath.get_attribute('disabled') == 'true':
            raise RuntimeError(
                f'Usuário não tem permissão de acesso à instância.'
            )

    def set_option(
        self,
        instancia: Literal['Primeiro Grau', 'Segundo Grau', 'Turmas Recursais'],
    ) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        # Avalia se opção está disponível
        self.check_available(instancia=instancia)

        # Avalia Instância Atualmente Selecionada
        instancia_atual = self.get_selected_option()
        # print(f'Qual a instância atual: {instancia_atual}')
        if instancia_atual not in [
            'Primeiro Grau',
            'Segundo Grau',
            'Turmas Recursais',
        ]:
            raise ValueError(
                f'A instância precisa ser "Primeiro Grau", "Segundo Grau" ou "Turmas Recursais"\n'
                f'Está definido {instancia_atual}'
            )

        # Avalia Instância Desejada
        if instancia not in [
            'Primeiro Grau',
            'Segundo Grau',
            'Turmas Recursais',
        ]:
            raise ValueError(
                f'A instância precisa ser "Primeiro Grau", "Segundo Grau" ou "Turmas Recursais"\n'
                f'Está definido {instancia}'
            )

        # Clica
        instancia_xpath = self._get_xpath_instance(instancia=instancia)
        # print(instancia_xpath.get_attribute(name='id'))
        instancia_xpath.click()

        # Notei que ao mudar para 2º Grau, às vezes o formulário não atualizava
        # Dai se aperta o botão "Consultar", atualiza...
        # Portanto, fiz essa rotina abaixo
        text_label = self.get_text(locator=self.label_foro_secao)
        # print(f'O texto inicial é "{text_label}"')
        tentativa = 0
        n_tentativas = 5
        while (
            instancia in ('Segundo Grau', 'Turmas Recursais')
            and text_label != 'Seção'
            and tentativa <= n_tentativas
        ):
            self.click(locator=self.btn_consultar)
            # print('Cliquei em Consultar')
            time.sleep(5)
            text_label = self.get_text(locator=self.label_foro_secao)
            tentativa += 1
            # print(f'O texto do while é "{text_label}"')


class Foro(InputModelSearchSet):
    """
    Representa o campo de *input* "Foro", que define
    qual o Foro que disponibilizou a intimação.

    Utilizado apenas em intimações de [instância] 1º grau.
    """

    def __init__(self, driver):
        super().__init__(driver)

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

        # Só tem em Primeiro Grau
        intim_inst = Instancia(driver=driver)
        if intim_inst.get_selected_option() != 'Primeiro Grau':
            raise Exception(
                f'Só se define "{self.__class__.__name__}" quando em instância de "Primeiro Grau"'
            )


class Vara(InputModelSearchSet):
    """
    Representa o campo de *input* "Vara", que define
    qual a Vara que disponibilizou a intimação.

    Utilizado apenas em intimações de [instâncias de] 1º grau.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelVara"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="nmVara"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.nmVara"]')
        self.lista_opcoes = None

        # Só tem em Primeiro Grau
        intim_inst = Instancia(driver=driver)
        if intim_inst.get_selected_option() != 'Primeiro Grau':
            raise Exception(
                f'Só se define "{self.__class__.__name__}" quando em instância de "Primeiro Grau"'
            )


class Especializacao(InputModelSearchSet):
    """
    Representa o campo de *input* "Especialização", que define
    qual a Especialização das intimações disponibilizadas.
    """

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelEspecialidade"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="nmEspecialidade"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.nmEspecialidade"]')
        self.lista_opcoes = None
        self.checkbox = (
            By.XPATH,
            '//td[@id="labelEspecialidade"]/following-sibling::td//tr//input[@name="dadosConsulta.filtrarApenasAtoSemEspecialidadeDefinida"]',
        )
        self.check_checkbox = (
            By.XPATH,
            '//td[@id="labelEspecialidade"]/following-sibling::td//tr//input[@id="entity.ato.especialidade.cdEspecialidade"]',
        )

    def apenas_processos_sem_especializacao(self) -> None:
        """
        Habilita o *checkbox* "Filtrar Processos sem Especialização definida".
        """
        attrib = self.attribute(locator=self.check_checkbox, attribute='class')
        # print('Especializa', attrib)
        if attrib.strip() != 'disabled':
            self.click(self.checkbox)


class Cargo(InputModelSearchSet):
    """
    Representa o campo de *input* "Cargo", que define
    qual o Cargo responsável pelas intimações disponibilizadas.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelCargo"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.iframe = (By.XPATH, '//iframe[@id="layerFormConsulta"]')
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="deCargo"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.deCargo"]')
        self.lista_opcoes = None
        self.checkbox = (
            By.XPATH,
            '//td[@id="labelCargo"]/following-sibling::td//tr//input[@name="dadosConsulta.filtrarApenasAtoSemCargo"]',
        )
        self.check_checkbox = (
            By.XPATH,
            '//td[@id="labelCargo"]/following-sibling::td//tr//input[@id="entity.ato.cargo.cdCargo"]',
        )

    def apenas_processos_sem_cargo(self) -> None:
        """
        Habilita o *checkbox* "Filtrar Processos sem Cargo definido".
        """
        attrib = self.attribute(locator=self.check_checkbox, attribute='class')
        # print('Cargo', attrib)
        if attrib.strip() != 'disabled':
            self.click(self.checkbox)


class Processo(PageElement):
    """
    Representa os campos de *input* "Processo", que define
    qual o processo que pertence à intimação disponibilizada.
    """

    processo_xpath = (By.XPATH, '//input[@id="identity.nuProcessoFormat"]')

    def write(self, texto: str) -> None:
        """
        Define o Número do Processo
        """
        self.set(locator=self.processo_xpath, value=texto)

    def clear(self) -> None:
        """
        Limpa o campo text
        """
        self.set(locator=self.processo_xpath, value='')


class NaturezaComunicacao(PageElement):
    """
    Representa o *radio button* "Natureza da comunicação".
    """

    # btn_consultar = (By.XPATH, '//input[@id="pbConsultar"]')
    # label_foro_secao = (By.XPATH, '//td[@id="labelForo"]/label')

    def set_option(
        self, natureza: Literal['Intimação', 'Citação', 'Ambas']
    ) -> None:
        """
        Define a opção para preenchimento do campo.
        """

        dd_natureza = {
            'Intimação': 'radioIntimacao',
            'Citação': 'radioCitacao',
            'Ambas': 'radioIntimacaoCitacao',
        }

        natureza_xpath = self.find(
            (By.XPATH, f'//input[@id="{dd_natureza[natureza]}"]')
        )
        natureza_xpath.click()


class Secao(InputModelSearchSet):
    """
    Representa o campo de *input* "Seção", que define
    qual a Seção que disponibilizou a intimação.

    Utilizado apenas em intimações de [instância] 2º grau.
    Equivalente ao "Foro" utilizado no 1º grau.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelForo"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="deCartorio"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.deCartorio"]')
        self.lista_opcoes = None

        # Só tem em Segundo Grau ou Turmas Recursais
        intim_inst = Instancia(driver=driver)
        instancia = intim_inst.get_selected_option()
        if instancia not in ['Segundo Grau', 'Turmas Recursais']:
            raise Exception(
                f'Só se define "{self.__class__.__name__}" quando em instância de "Segundo Grau" ou "Turmas Recursais"\n'
                f'Está definido "{instancia}"'
            )


class OrgaoJulgador(InputModelSearchSet):
    """
    Representa o campo de *input* "Órgao Julgador", que define
    qual o Órgao Julgador que disponibilizou a intimação.

    Utilizado apenas em intimações de [instância] 2º grau.
    Equivalente à "Vara" utilizado no 1º grau.
    """

    def __init__(self, driver):
        super().__init__(driver)

        self.abre_consulta = (
            By.XPATH,
            '//td[@id="labelVara"]/following-sibling::td//tr//img[@title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//table[@id="tabelaResultado"]//td[@property="nmVara"]',
        )
        self.input_opcao = (By.XPATH, '//input[@id="entity.nmVara"]')
        self.lista_opcoes = None

        # Só tem em Segundo Grau ou Turmas Recursais
        intim_inst = Instancia(driver=driver)
        instancia = intim_inst.get_selected_option()
        if instancia not in ['Segundo Grau', 'Turmas Recursais']:
            raise Exception(
                f'Só se define "{self.__class__.__name__}" quando em instância de "Segundo Grau" ou "Turmas Recursais"\n'
                f'Está definido "{instancia}"'
            )


class Classe(InputModelTree):
    """
    Representa o campo de *input* "Classe", que define
    qual a Classe que pertence a intimação disponibilizada.
    """

    def __init__(self, driver):
        super().__init__(driver)
        # O xPath do "Abre Consulta" é um pouco diferente do padrão
        self.abre_consulta = (
            By.XPATH,
            '//td[@id=""]/following-sibling::td//tr//img[@id="botaoProcurar_classes" and @title="Abre a consulta"]',
        )
        self.btn_selecionar = (
            By.XPATH,
            '//div[@id="classes_treeSelectContainer"]//input[@class="spwBotaoDefaultGrid" and @value="Selecionar"]',
        )
        self.btn_procurar = (
            By.XPATH,
            '//div[@id="classes_treeSelectContainer"]//input[@id="filtroButton"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//ul[@id="classes_tree"]//span[@class="node selectable checkable Unchecked"]',
        )
        self.input_opcao = (
            By.XPATH,
            '//input[@id="classes_treeSelectFilter"]',
        )  #
        self.lista_opcoes = None


class AssuntoPrincipal(InputModelTree):
    """
    Representa o campo de *input* "Assunto Principal", que define
    qual o Assunto Principal que pertence à intimação disponibilizada.
    """

    def __init__(self, driver):
        super().__init__(driver)
        # O XPath do "Abre Consulta" é um pouco diferente do padrão
        self.abre_consulta = (
            By.XPATH,
            '//td[@id=""]/following-sibling::td//tr//img[@id="botaoProcurar_assuntos" and @title="Abre a consulta"]',
        )
        self.linhas_tabela = (
            By.XPATH,
            '//ul[@id="assuntos_tree"]//span[@class="node selectable checkable Unchecked"]',
        )
        self.input_opcao = (
            By.XPATH,
            '//input[@id="assuntos_treeSelectFilter"]',
        )
        self.btn_selecionar = (
            By.XPATH,
            '//div[@id="assuntos_treeSelectContainer"]//input[@class="spwBotaoDefaultGrid" and @value="Selecionar"]',
        )
        self.lista_opcoes = None


class Area(PageElement):
    """
    Representa o menu *dropdown* "Área", que define
    qual a Área que pertence à intimação disponibilizada.
    """

    selector = (By.XPATH, '//select[@id="flArea"]')

    def get_options(self, options_delete=None) -> List[str]:
        """
        Obtem opções de preenchimento.
        """

        return self.create_select_options(self.selector, options_delete)

    def set_option(self, option) -> None:
        """
        Define a opção para preenchimento do campo.
        """
        list_options = self.get_options()
        if option not in list_options:
            raise ValueError(f'Precisa ser uma opção {list_options}')

        self.select(self.selector, option)


class ConsultarIntimacoes(PageElement):
    """
    Representa o botão "Consultar"
    """

    btn_consultar = (
        By.XPATH,
        '//input[@id="pbConsultar"]',
    )
    table_xpath = (
        By.XPATH,
        '//table[@id="Row" and @class="spwTabelaGrid"]',
    )

    def consultar(self) -> None:
        """
        Aperta o botão "Consultar"
        """
        self.click(locator=self.btn_consultar)

    def check_table(self):
        """
        Avalia se tem resultados
        """
        attrib = self.attribute(locator=self.table_xpath, attribute='class')
        if attrib == 'spwTabelaGrid':
            return True
        else:
            return False


# class CheckError(PageElement):
#     """
#     Avalia se o e-SAJ está com algum erro apresentado.
#     """

#     msg_erro = (
#         By.XPATH,
#         '//*[contains(text(),"Não foi possível executar esta operação. Tente novamente mais tarde.")]',
#     )
#     msg_resultado = (
#         By.XPATH,
#         '//div[@id="spwTabelaMensagem"]//table[@class="tabelaMensagem"]',
#     )

#     def has_errors(self) -> bool:
#         """
#         Avalia erro "Não foi possível executar esta operação. Tente novamente mais tarde".
#         """
#         try:
#             # Find Errors
#             tags = self.find_all(locator=self.msg_erro, wait=3)

#             #
#             if len(tags) > 0:
#                 # Mensagem
#                 warnings.warn(
#                     message=f'\n'
#                     f'e-SAJ com problemas!!.\n'
#                     f'"Não foi possível executar esta operação. Tente novamente mais tarde"'
#                     f'\n',
#                     category=RuntimeWarning,
#                 )
#                 return True

#             else:
#                 print(f'Erro: Encontrou Tag!? {len(tags)} registros')
#                 return False

#         except:
#             return False

#     def tem_resultado(self) -> bool:
#         """
#         Avalia o resultado da pesquisa

#         - `True` significa que tem regstros
#         - `False` significa que NÃO tem regstros
#         """
#         try:
#             # Find Errors
#             tags = self.find_all(locator=self.msg_resultado, wait=3)
#             print(tags[0].text)

#             # Se tem
#             if len(tags) == 1 and (
#                 tags[0].text
#                 == 'Atenção\n  Não foram encontrados registros de atos para os parâmetros informados.'
#             ):
#                 # Mensagem
#                 warnings.warn(
#                     message=f'\n'
#                     f'A pesquisa não retornou nenhum resultado.\n'
#                     f'\n',
#                     category=RuntimeWarning,
#                 )
#                 # Se encontra a mensagem, significa que não tem resultado
#                 return False

#             else:
#                 #print('dsdsdsd')
#                 print(print(tags[0].text))
#                 return False

#         except:
#             # Se não encontra a mensagem, significa que tem resultado!
#             return True


class CheckError(PageElement):
    """
    Avalia se o e-SAJ está com algum erro apresentado.
    """

    msg_erro = (
        By.XPATH,
        '//*[contains(text(),"Não foi possível executar esta operação. Tente novamente mais tarde.")]',
    )

    @disable_logging
    def has_errors(self) -> bool:
        """
        Avalia erro "Não foi possível executar esta operação. Tente novamente mais tarde".
        """
        try:
            # Find Errors
            tags = self.find_all(locator=self.msg_erro, wait=3)

            #
            if len(tags) > 0:
                # Mensagem
                logging.warning(
                    msg=f'e-SAJ com problemas: "Não foi possível executar esta operação. Tente novamente mais tarde"'
                )
                return True

            else:
                print(f'Erro: Encontrou Tag!? {len(tags)} registros')
                return False

        except:
            return False


class CheckResults(PageElement):
    """
    Avalia os resultados do e-SAJ.
    """

    msg_resultado = (
        By.XPATH,
        '//div[@id="spwTabelaMensagem"]//table[@class="tabelaMensagem"]',
    )

    table_xpath = (
        By.XPATH,
        '//table[@id="Row" and @class="spwTabelaGrid"]',
    )

    @disable_logging_property
    def tipo_resultado(self):
        """
        Define qual o tipo de resultado
        """

        tipo_resultado_var = None
        n_tentativa = 0

        while tipo_resultado_var is None and n_tentativa <= 10:
            # Tenta encontrar mensagem
            try:
                msg = self.find(locator=self.msg_resultado, wait=0.01)

            except:
                msg = None

            # Tenta encontrar tabela
            try:
                tab = self.find(locator=self.table_xpath, wait=0.01)

            except:
                tab = None

            if tab == None and msg == None:
                tipo_resultado_var = None

            elif tab == None and msg != None:
                tipo_resultado_var = 'Mensagem'

            elif tab != None and msg == None:
                tipo_resultado_var = 'Tabela'

            else:
                tipo_resultado_var = None

            n_tentativa += 1
        return tipo_resultado_var

    @disable_logging_property
    def messages(self) -> list | None:
        """
        Obtem a lista de mensagens
        """
        # Obtem o tipo de Resultado
        tipo_resultado_var = self.tipo_resultado

        # Se é Mensagem
        if tipo_resultado_var == 'Mensagem':
            try:
                tags = self.find_all(locator=self.msg_resultado, wait=3)
                list_messages = []
                for tag in tags:
                    list_values = tag.text.strip().split('\n')
                    list_values = [x.strip() for x in list_values]
                    list_messages.append(': '.join(list_values))

                # Excluí mensagem em braco (usada em formação do HTML)
                list_messages = [msg for msg in list_messages if msg]
                # print('Lista', list_messages)
                return list_messages

            # Se não encontra, é lista vazia
            except Exception as e:
                # print(f"Erro: {e}")
                list_messages = []
                return list_messages

        # Se é Tabela
        elif tipo_resultado_var == 'Tabela':
            list_messages = []
            return list_messages

    @disable_logging
    def tem_resultado(self) -> bool:
        """
        Avalia o resultado da pesquisa

        - `True` significa que tem registros
        - `False` significa que NÃO tem regstros
        """
        messages = self.messages
        # print('A lista de msg é: ', messages)

        # Se não encontra qualquer mensagem, significa que tem resultado!
        if messages == []:
            return True

        # Se encontra alguma mensagem, não tem resultado
        # Ou se faz necessário entender o que ocorre
        elif messages != []:

            if (
                'Atenção: Não foram encontrados registros de atos para os parâmetros informados.'
                in messages
            ):

                # Mensagem
                # logging.warning(msg='A pesquisa não retornou nenhum resultado.')

                # Se encontra a mensagem, significa que não tem resultado
                return False

            else:
                print('Definir erros:', messages)
                raise Exception


class Tabela(PageElement):
    """
    Representa a tabela de resultados
    """

    table_xpath = (By.XPATH, '//table[@id="Row" and @class="spwTabelaGrid"]')

    def get_xpath_rows(self):
        # Cria Lista de xPaths
        list_xpath = [
            f'//table[@id="Row" and @class="spwTabelaGrid"]//tr[@id="linhaRow_{x}"]'
            for x in range(0, 100)
        ]

        # Linhas
        list_xpath_or = ' | '.join(list_xpath)
        rows_xpath = self.find_all(locator=(By.XPATH, list_xpath_or))

        # Results
        # print(f'São {len(rows_xpath)} linhas')
        return rows_xpath

    def get_table(
        self,
        *args,
        **kwargs,
    ) -> (
        List[RecebimentoIntimacoes1Grau]
        | List[RecebimentoIntimacoes2Grau]
        | List[ConsultaIntimacoes2Grau]
    ):
        """
        Obtém a tabela com 20 registros, sendo essa a paginação padrão do e-SAJ.
        """
        # Vê qual a instancia
        # intim_tipo = Instancia(driver=self)
        # instancia = intim_tipo.get_selected_option()
        intim_inst = Instancia(driver=self.driver)
        instancia = intim_inst.get_selected_option()

        # Cria lista com os xPaths das linhas
        rows_xpath = self.get_xpath_rows()

        list_dd = []
        for row in rows_xpath:
            # Pega o Número do Processo
            x_processo = (
                By.XPATH,
                './/td//div[@name_="ato.nuProcessoFormat"]',
                row,
            )

            # Atributos
            x_disponibilizacao = (
                By.XPATH,
                './/td//div[@name_="ato.dtInclusao"]',
                row,
            )
            x_dt_intimacao = (By.XPATH, './/td//div[@name_="dtIntimacao"]', row)
            x_prazo = (By.XPATH, './/td//div[@name_="nuDiasPrazo"]', row)
            x_classe = (
                By.XPATH,
                './/td//div[@name_="classeEAssuntoPrincipaisFormatado"]',
                row,
            )
            x_recebido_por = (
                By.XPATH,
                './/td//div[@name_="usuarioIntimacao.nmUsuario"]',
                row,
            )
            x_mov = (By.XPATH, './/td//div[@name_="ato.deTipoMvProcesso"]', row)
            x_foro = (By.XPATH, './/td//div[@name_="ato.foro.nmForo"]', row)
            x_vara = (By.XPATH, './/td//div[@name_="ato.vara.nmVara"]', row)
            x_sec = (
                By.XPATH,
                './/td//div[@name_="ato.cartorio.deCartorio"]',
                row,
            )
            x_org = (By.XPATH, './/td//div[@name_="ato.vara.nmVara"]', row)
            x_esp = (
                By.XPATH,
                './/td//div[@name_="ato.especialidade.nmEspecialidade"]',
                row,
            )
            x_car = (By.XPATH, './/td//div[@name_="ato.cargo.deCargo"]', row)

            path = urlparse(url=self.driver.current_url).path

            # TODO Mapear tarjas / Cores
            # Notei que existem processos vermelhos no "Consulta"
            # Recebimento de Intimações Eletrônicas ()
            if path == '/intimacoesweb/abrirConsultaAtosNaoRecebidos.do':
                # print(f'Endpoint{path}')
                if instancia == 'Primeiro Grau':
                    list_dd.append(
                        RecebimentoIntimacoes1Grau(
                            disponibilizacao=self.get_text(x_disponibilizacao),
                            prazo_processual=self.get_text(x_prazo),
                            numero_processo=self.get_text(x_processo),
                            classe_assunto_principal=self.get_text(x_classe),
                            movimentacao=self.get_text(x_mov),
                            foro=self.get_text(x_foro),
                            vara=self.get_text(x_vara),
                            especializacao=self.get_text(x_esp),
                            cargo=self.get_text(x_car),
                        )
                    )

                # Quando for Recebimento
                if instancia in ['Segundo Grau', 'Turmas Recursais']:
                    list_dd.append(
                        RecebimentoIntimacoes2Grau(
                            disponibilizacao=self.get_text(x_disponibilizacao),
                            prazo_processual=self.get_text(x_prazo),
                            numero_processo=self.get_text(x_processo),
                            classe_assunto_principal=self.get_text(x_classe),
                            movimentacao=self.get_text(x_mov),
                            secao=self.get_text(x_sec),
                            orgao_julgador=self.get_text(x_org),
                            especializacao=self.get_text(x_esp),
                            cargo=self.get_text(x_car),
                        )
                    )

            # Recebimento de Intimações Eletrônicas
            elif path == '/intimacoesweb/consultarAtosNaoRecebidos.do':
                if instancia == 'Primeiro Grau':
                    list_dd.append(
                        RecebimentoIntimacoes1Grau(
                            disponibilizacao=self.get_text(x_disponibilizacao),
                            prazo_processual=self.get_text(x_prazo),
                            numero_processo=self.get_text(x_processo),
                            classe_assunto_principal=self.get_text(x_classe),
                            movimentacao=self.get_text(x_mov),
                            foro=self.get_text(x_foro),
                            vara=self.get_text(x_vara),
                            especializacao=self.get_text(x_esp),
                            cargo=self.get_text(x_car),
                        )
                    )

                # Quando for Recebimento
                if instancia in ['Segundo Grau', 'Turmas Recursais']:
                    list_dd.append(
                        RecebimentoIntimacoes2Grau(
                            disponibilizacao=self.get_text(x_disponibilizacao),
                            prazo_processual=self.get_text(x_prazo),
                            numero_processo=self.get_text(x_processo),
                            classe_assunto_principal=self.get_text(x_classe),
                            movimentacao=self.get_text(x_mov),
                            secao=self.get_text(x_sec),
                            orgao_julgador=self.get_text(x_org),
                            especializacao=self.get_text(x_esp),
                            cargo=self.get_text(x_car),
                        )
                    )

            # Consulta de Intimações Recebidas
            elif path == '/intimacoesweb/consultarAtosRecebidos.do':
                if instancia in ['Segundo Grau', 'Turmas Recursais']:
                    list_dd.append(
                        ConsultaIntimacoes2Grau(
                            disponibilizacao=self.get_text(x_disponibilizacao),
                            data_intimacao=self.get_text(x_dt_intimacao),
                            prazo_processual=self.get_text(x_prazo),
                            numero_processo=self.get_text(x_processo),
                            classe_assunto_principal=self.get_text(x_classe),
                            recebido_por=self.get_text(x_recebido_por),
                            movimentacao=self.get_text(x_mov),
                            # secao=self.get_text(x_sec),
                            # orgao_julgador=self.get_text(x_org),
                            especializacao=self.get_text(x_esp),
                            cargo=self.get_text(x_car),
                        )
                    )
            else:
                print(path)

        return list_dd

    def select_processos(
        self,
        seleciona_processos: List,
        *args,
        **kwargs,
    ):
        """
        Seleciona os processos na tabela
        """
        # Cria lista com os xPaths das linhas
        rows_xpath = self.get_xpath_rows()

        for row in rows_xpath:
            # Pega o Número do Processo
            x_processo = (
                By.XPATH,
                './/td//div[@name_="ato.nuProcessoFormat"]',
                row,
            )
            processo = self.get_text(x_processo)

            # Se o Processo está na lista, seleciona
            if processo in seleciona_processos:
                x_check_checkbox = (
                    By.XPATH,
                    './/td//input[@type="checkbox"]/../following-sibling::td[@style="display: none"]/input[@name_]',
                    row,
                )
                # Avalia se o CheckBox está marcado. Em caso negativo, clica!
                # Se não encontra o atributo "name", o processo não está selecionado
                if 'cdAto' not in self.attribute(
                    locator=x_check_checkbox, attribute='name'
                ):
                    # Clica
                    x_checkbox = (
                        By.XPATH,
                        './/td//input[@type="checkbox"]',
                        row,
                    )
                    self.click(locator=x_checkbox)

    def count_selected_processos(
        self,
        type_result: Literal['lista', 'numero de registros'],
        *args,
        **kwargs,
    ):
        """
        Conta o número de registros selecionados na tabela
        """
        # Cria lista com os xPaths das linhas
        rows_xpath = self.get_xpath_rows()

        list_dd = []
        for row in rows_xpath:
            # Pega o Número do Processo
            x_processo = (
                By.XPATH,
                './/td//div[@name_="ato.nuProcessoFormat"]',
                row,
            )
            processo = self.get_text(x_processo)

            # Se o Processo está na lista, seleciona
            x_check_checkbox = (
                By.XPATH,
                './/td//input[@type="checkbox"]/../following-sibling::td[@style="display: none"]/input[@name_]',
                row,
            )
            # Avalia se o Checkbox está marcado.
            # Se encontra o atributo "name", o processo está selecionado
            if 'cdAto' in self.attribute(
                locator=x_check_checkbox, attribute='name'
            ):
                list_dd.append(processo)

        if type_result == 'lista':
            return list_dd

        elif type_result == 'numero de registros':
            return len(list_dd)

    def count_all_processos(
        self,
        type_result: Literal['lista', 'numero de registros'],
        *args,
        **kwargs,
    ):
        """
        Conta o número de registros na tabela, selecionados ou não
        """

        rows_xpath = self.get_xpath_rows()

        if type_result == 'lista':
            return rows_xpath

        elif type_result == 'numero de registros':
            return len(rows_xpath)


class Acoes(PageElement):
    """
    Represante os botões que promovem "Ações", tais como:
    - Receber
    - Especializar
    - Exportar
    """

    # btn_define = (
    #     By.XPATH,
    #     '//table[@class="secaoBotoesBody"]//input[@id="definirEspecialidade"]',
    # )
    # btn_define = (
    #     By.XPATH,
    #     '//table[@class="secaoBotoesBody"]//input[@id="definirEspecialidade"]',
    # )
    btn_define = (
        By.XPATH,
        '//table[@class="secaoBotoesBody"]//input[@id="definirEspecialidade" and @value="Definir Especialização e Cargo"]',
    )

    btn_export = (
        By.XPATH,
        '//table[@class="secaoBotoesBody"]//input[@id="exportarArquivo"]',
    )
    btn_receber = (
        By.XPATH,
        '//table[@class="secaoBotoesBody"]//input[@id="pbReceberAtos"]',
    )

    def definir_especializacao_cargo(self) -> None:
        """
        Aperta botão para "Definir Especialização e Cargo"
        """
        # Avaliar se algum processo está selecionado
        self.click(self.btn_define)

    def export_csv(self, *args, **kwargs) -> Path:
        """
        Aperta botão para "Exportar para Arquivo".
        TODO: Fazer funcionar no Chrome
        """

        # Download Path
        download_path = kwargs.get('download_path', False)
        if download_path is False:
            # Temp Path
            temp_path = tempfile.gettempdir()
            project_temp_path = Path(temp_path) / config.TEMP_PATH_NAME

            # Scrapy Path
            scrapy_path = project_temp_path / 'scrapy'
            scrapy_path.mkdir(exist_ok=True, parents=True)

            # Cria Pasta
            download_path = scrapy_path / 'download'
            download_path.mkdir(exist_ok=True, parents=True)
            print('A pasta de download de dados é: ', download_path)

        # Deleta tudo
        list_csvs = list(download_path.rglob('*.csv'))
        start_time = time.time()
        while len(list_csvs) != 0:
            [x.unlink() for x in list_csvs]
            time.sleep(1)
            list_csvs = list(download_path.rglob('*.csv'))

            # Verifica se o tempo limite de 60 segundos foi atingido
            if time.time() - start_time > 60:
                raise Exception(
                    "Tempo limite atingido. O delete não foi concluído."
                )

        # Faz Download
        self.click(self.btn_export)
        list_csvs = list(download_path.rglob('*.csv'))
        start_time = time.time()
        while len(list_csvs) != 1:
            time.sleep(1)
            list_csvs = list(download_path.rglob('*.csv'))

            # Verifica se o tempo limite de 60 segundos foi atingido
            if time.time() - start_time > 60:
                raise Exception(
                    "Tempo limite atingido. O download não foi concluído."
                )

        #
        if len(list(download_path.rglob('*.csv'))) == 1:
            return list(download_path.rglob('*.csv'))[0]

        else:
            raise Exception(
                f'Era pra ter algum um arquivo na pasta\n{download_path}'
            )

    def receber(self) -> None:
        """
        Aperta botão para "Receber Selecionados"
        """
        self.click(self.btn_receber)


if __name__ == '__main__':
    pass
