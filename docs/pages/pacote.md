Para o presente projeto optou-se por utilizar o Page Object Model.

O **_Page Object Model_** (POM) foi inicialmente descrito
por [Martin Fowler](https://martinfowler.com/bliki/PageObject.html) sob o nome
_Windown Driver_. No entanto, o termo
_**Page Object**_ foi popularizado pelo _framework_ de testes
_web_ [Selenium](https://www.selenium.dev/), e desde então
se tornou o nome geralmente utilizado.

O POM é um _design pattern_ que encapsula a interface de uma página _web_ em uma
classe orientada a objetos, permitindo
que os testes interajam com a página através de métodos específicos, em vez de
manipular diretamente os elementos HTML.
Isso ajuda a reduzir a duplicação de código e facilita a manutenção dos testes
quando a interface do usuário muda.

| _If you have WebDriver APIs in your test methods, you're doing it wrong_.

[Simon Stewart](https://github.com/shs96c) PageObject

<br>

Assistindo aos
vídeos [Page Object Model In Selenium WebDriver | Introduction](https://www.youtube.com/watch?v=dtmqIHsPPug) (
vídeo
curto, de
11', de uma indiana) que dá uma introdução teórica sobre o POM e continua
com [Page ObjectModel In Selenium WebDriver using By Locator](https://www.youtube.com/watch?v=UxgxiJ0pGkY),
ficou claro
que é possível criar o POM de duas maneiras distintas:

- **By Locator**
- **By PageFactory Class**

<br>

---

## POM em _python_

No
vídeo [What Is Page Object Model? | pytest Framework Tutorial | Part-IX | LambdaTest](https://www.youtube.com/watch?v=8C6FNN4VK9g)
há um exemplo muito interessante desse _design pattern_. O exemplo está tb
disponível no
repositório [PytestTutorials](https://github.com/RexJonesII/PytestTutorials).

<br>

---

### Dunossauro

Além disso tem o material do Eduardo Mendes, que é excelente.

- [Selenium com Python #12 - Padrão Page Object](https://www.youtube.com/watch?v=WhZHZ_RYzxw)
  e [Selenium com Python #13 - Padrão Page object p.II](https://www.youtube.com/watch?v=KM90nnkt-5w)
- [dunossauro/curso-python-selenium](https://github.com/dunossauro/curso-python-selenium)
- [Selenium com Python #13 - Padrão Page object p.II](https://www.youtube.com/watch?v=KM90nnkt-5w)

<br>

---

### Outras Referência

- [6 | Page Object Model | Selenium Python](https://www.youtube.com/watch?v=0kHbK5iZkN0)
- [Boost Your Web Scraping Efficiency: Learn How to Clear Cache in Python Selenium](https://medium.com/@meiyee715/boost-your-web-scraping-efficiency-learn-how-to-clear-cache-in-python-selenium-c6425dacd6a0)
- [gunesmes/page-object-python-selenium](https://github.com/gunesmes/page-object-python-selenium)
  é um _repo_ com um modelo de _PageObjectModel_
- [Measure and Optimize Page Load Time With Selenium](https://www.lambdatest.com/blog/how-to-measure-page-load-times-with-selenium/)

<br>

---

## Outros Projetos

Existem outros projetos para raspar dados dos Tribunais.

- Há um pacote de R
  chamado [jjesusfilho/tjsp](https://github.com/jjesusfilho/tjsp),
  do [José de Jesus Filho](https://github.com/jjesusfilho), que obtém dados do
  TJSP para fazer estudos de **jurimetria**.
- O projeto [courtsbr/esaj](http://courtsbr.github.io/esaj), também em R, por
  exemplo faz o
  _download_
  das páginas do e-SAJ em formato _.html_. Não serve para meu propósito, mas
  pareceu interessante.

<br>

Há outros projetos disponíveis
no [GitHub](https://github.com/search?q=esaj&type=repositories) contendo "
e-SAJ".
