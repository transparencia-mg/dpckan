Change Log
==========

0.1.22 (29/08/2023)
------------------
- Melhora processo de criação/atualização datastore

0.1.21 (07/03/2023)
------------------
- Possibilita atualização de conjuntos privados

0.1.20 (16/02/2023)
------------------
- Fixa versões de pacotes dependentes - erro de atualização versão frictionless 5

0.1.19 (22/11/2022)
------------------
- Melhora mensagens de log informando qual host está sendo utilizado

0.1.18 (02/04/2022)
------------------
- Adiciona flag --exit-code
- Bug Fix na chamada da função `dataset update` que não estava atualizando metadados do conjunto

0.1.17 (14/03/2022)
------------------
- Bug Fix na chamada da função `resource_update` dentro de `dataset_update`

0.1.16 (14/03/2022)
------------------
- Inclusão função `dpckan dataset get`
- Correções flag `--datastore`
- Correções `dpckan resource create`

0.1.15 (21/02/2021)
------------------
- Registra ids de recursos publicados apenas na instância CKAN e não mais no arquivo datapackage.json local
- Revisa/simplifica documentação CLI
- Modifica chamada das funções

0.1.14 (27/12/2021)
------------------
- Corrige funcionamento da flag para acionamento do datastore nunca produzir efeitos
- Altera nome da flag para acionamento do datastore durante criação e atualização de conjunto de dados de metadata para datastore

0.1.13 (22/12/2021)
------------------
-  Remove extended do nome do arquivo extended_datapackage.json durante criação de recursos datapackage.json

0.1.12 (21/12/2021)
------------------
- Adiciona Flag metadata para acionamento datastore durante criação e atualização de conjunto de dados

0.1.11 (01/12/2021)
------------------
- Adicionando encoding para subir arquivos README, CONTRIBUTING e CHANGELOG para CKAN
- Atualizando metadado do conjunto caso apenas datapackage.json sofra modificações

0.1.10 (12/11/2021)
------------------
- Dataset update primeira versão, atualizando recursos e metadados modificados
- Pequenas refatorações

0.1.9 (12/11/2021)
------------------
- Correção pacote ipdb importado erradamente

0.1.8 (12/11/2021)
------------------
- Apaga propriedade ckan_hosts apenas da instância CKAN desejada
- Expansão schema e dialetic presentes no recurso datapackage.json importados na instância CKAN

0.1.7 (11/11/2021)
------------------
- Melhoria da implementação da documentação do conjunto de dados publicados no CKAN

0.1.6 (11/11/2021)
------------------
- Validando a existência da proprieda owner_org do arquivo datapackage.json
- Validando a existência do valor da propriedade owner_org do arquivo datapackage.json na instância do CKAN desejada

0.1.5 (11/11/2021)
------------------
- Melhoria de documentação click (--help)
- Inclusão de flag --stop para interromper execução em caso de falha de validação frictionless

0.1.4 (08/11/2021)
------------------
- Separação pacotes de desenvolvimento (requirements.txt) de pacotes de utilização (setup.py)
- Inclusão frictionless validate como validações

0.1.3 (20/10/2021)
------------------
- Erro de publicação desta versão

0.1.2 (20/10/2021)
------------------
- Update python-dotenv

0.1.1 (08/09/2021)
------------------
- Revisão documentação README.md
- Revisão documentação docstrings
- Revisão estrutura testes

0.1.0 (23/08/2021)
------------------
- Criação dos comandos cli para criação e atualização de datasets
- Criação dos comandos cli para criação e atualização de recursos
- Melhoria da documentação

0.0.1.9020 (09/06/2021)
------------------
- Publicação de documentação online do pacote
- Correção de bugs e exclusão de códigos repetidos ao longo do projeto


0.0.1.9000 (06/05/2021)
------------------
- Lançamento primeira versão de teste do pacote
