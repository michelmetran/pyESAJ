Tratando-se de um pacote com as dependência gerenciadas pelo [Poetry](https://python-poetry.org/), para criar o ambiente de desenvolvimento basta dar o comando abaixo.

```shell
# Instala os pacotes definidos no pyproject.toml
poetry install

# Instala os pacotes, adicionando os pacotes necessários pra documentação
poetry install --with docs
```

<br>

---

## Documentação

A documentação do projeto foi feita usando o [MkDocs](https://www.mkdocs.org/), com _deploy_ no [Read The Docs](https://app.readthedocs.org/).
