Para instanciar um _webdriver_ para interagir com o _e-SAJ_, basta instanciá-lo conforme abaixo.

```python
import pyesaj.scraper as esaj

# Instancia Driver/Navegador
driver = esaj.webdriver.Firefox(verify_ssl=False)

# Login
log = esaj.page.Login(driver=driver)
log.login_1_etapa(username='name@email.com', password='********')
```

<br>

---

## _Scripts_

Na pasta `docs/scripts` do repositório [pyESAJ](https://github.com/michelmetran/pyESAJ) é possível encontrar formas de utilização do pacote.
