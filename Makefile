help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

update-package: clean-build build publish-build ## Limpa, constroi e publica nova versão do pacote, necessário ativar ambiente antes de iniciar
	@echo "Não se esqueça de fazer o commit e push para o repositorio online"

clean-build: ## Limpa as pastas build e dist e o arquivo .egg-info, criados para publicação do pacote
	@echo "Limpando pastas e arquivos necessários para publicação do pacote"
	@rm --force --recursive build/
	@rm --force --recursive dist/
	@rm --force --recursive *.egg-info

build: ## Constroi as pastas e arquivos necessários para publicação do pacote
	@echo "Construindo pacote"
	@python setup.py sdist bdist_wheel

publish-build: ## Publica pacote em Pypi
	@echo "Publicando pacote. Caso não tenha atualizado a versão no arquivo setup.py encerre e rode novamente"
	@twine upload dist/*
