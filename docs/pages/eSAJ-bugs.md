# _Bugs_

Durante o desenvolvimento da aplicação, foi possível encontrar alguns erros e _bugs_ no sistema e-SAJ.
Seria importante reportar estes erros à [Secretaria de Tecnologia da Informação](https://www.tjsp.jus.br/Secretarias) do TJSP, com a finalidade de que os erros fossem corrigidos.

<br>

---

## Número Total de Intimações

![Paginacao](/.attachments/bug-paginacao.png)

Notei que o número total de intimações está com erro.

No exemplo a seguir a tabela demonstra que são apresentadas as intimações de 121 até 135, de um total de 134.

O número 134 está errado! Temos, na realidade, 135 intimações.

<br>

---

## Redirecionamento Errado do Número da Página

Na página de [Recebimento de Intimações](https://esaj.tjsp.jus.br/intimacoesweb/consultarAtosNaoRecebidos.do), após filtrar um determinado conjunto de intimações, ao navegar pelas páginas utilizando as setas, avançando e retrocedendo no número de páginas está tudo certo. Os controles funcionam conforme esperado.

Contudo, ao inserir um número de página e apertar o tecla "Enter" o usuário é redirecionado para uma página fora do escopo do "Recebimento de Intimações", inpossibilitando a navegação por esses
