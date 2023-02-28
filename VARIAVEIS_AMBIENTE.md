## Configuração de Variáveis de ambiente

Todos os comandos exigem a indicação de uma instância CKAN (ex: https://demo.ckan.org/) e de uma chave válida para autenticação na referida instância. Esta indicação deverá ser realizada através do cadastro de variáveis de ambiente. Para invocação CLI de qualquer comando sem a necessidade de indicar explicitamente estas variáveis recomenda-se utilização dos nomes `CKAN_HOST` e `CKAN_KEY` para cadastro de instância e chave respectivamente. Caso outros nomes sejam utilizados, necessário indicar explicitamente durante a chamada da função desejada, utilizando-se as flags "--ckan-host" e "--ckan-key", conforme demostrado abaixo e ou de maneira mais detalhada na sessão [Uso](#uso).


```bash
# CKAN_HOST=https://demo.ckan.org/
# CKAN_KEY=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização sem necessidade de indicar explicitamente variáveis

$ dpckan dataset create
```

```bash
# CKAN_HOST_PRODUCAO=https://demo.ckan.org/
# CKAN_KEY_PRODUCAO=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização indicando explicitamente variáveis, através flags --ckan-host e --ckan-key

$ dpckan --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO dataset create
```

O cadastro das variáveis de ambiente `CKAN_HOST` e `CKAN_KEY`, necessárias para invocação de cada comando, deverá ser realizada conforme sistema operacional do usuário. Abaixo links de referência para tal:

  * [Windows](https://professor-falken.com/pt/windows/como-configurar-la-ruta-y-las-variables-de-entorno-en-windows-10/)
  * [Linux](https://ricardo-reis.medium.com/vari%C3%A1veis-de-ambiente-no-linux-debian-f677d6ca94c)
  * [Mac](https://support.apple.com/pt-br/guide/terminal/apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac)


Alternativamente, o cadastro destas variáveis de ambiente poderá ser realizado em arquivo ".env", na raiz do conjunto de dados, sendo necessário a inclusão deste ".env" em arquivo ".gitignore", evitando assim a sincronização e consequente publicização destas chaves em repositórios online como [github](https://github.com/), conforme demostrado abaixo:


```bash
# CUIDADO: SOMENTE UTILIZE A OPÇÃO SUGERIDA ABAIXO SE POSSUIR FAMILIARIDADE COM O ASSUNTO, EVITANDO ASSIM PROBLEMAS COM ACESSO DE TERCEIROS NÃO AUTORIZADOS EM SUA INSTÂNCIA CKAN
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE OS ARQUIVO ".env" e ".gitignore" NÃO EXISTIREM NA RAIZ DO CONJUNTO DE DADOS
# CUIDADO: CASO COMANDOS ABAIXO SEJAM EXECUTADOS COM ".env" e ".gitignore" EXISTENTES TODO CONTEÚDO DOS MESMOS SERÁ APAGADO

# Crie arquivo ".env" com estrutura para receber chaves CKAN_HOST e CKAN_KEY
# Após a criação, abra o arquivo e inclua os valores para cada variável

$ echo "CKAN_HOST=''\nCKAN_KEY=''" > .env
```
```bash
# Crie arquivo ".gitignore" com configuração para excluir arquivo ".env" do controle de versão git

$ echo ".env" > .gitignore
```
```bash
# Confira se configuração foi realizada com sucesso
# Comando abaixo deverá mostrar apenas criação/modificação de arquivo ".gitignore", não sendo apresentado nada para arquivo ".env"

$ git status
```