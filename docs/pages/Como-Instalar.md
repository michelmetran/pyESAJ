Tratando-se de um pacote privado, armazenado no repositório
do [AzureDevOps](https://dev.azure.com/mpsp/Informa%C3%A7%C3%B5es%20Estat%C3%ADsticas/_artifacts/feed/pypi-mpsp/PyPI/pyesaj/),
é necessário instalar previamente o `artifacts-keyring` para obter credenciais
da organização. Caso opte por não usar o `artifacts-keyring`, será necessário
inserir o _username_ (utilizado no MPSP) e o _password_ (que na realidade é o
_Personal Access Token_ - PAT).

```shell
# Install
pip3 install artifacts-keyring

# Install Specific Version
pip3 install pyesaj==0.1.3 --index-url https://pkgs.dev.azure.com/mpsp/Informações%20Estatísticas/_packaging/pypi-mpsp/pypi/simple

# Upgrade
pip3 install pyesaj --upgrade --index-url https://pkgs.dev.azure.com/mpsp/Informações%20Estatísticas/_packaging/pypi-mpsp/pypi/simple

# Uninstall
pip3 uninstall pyesaj
```
