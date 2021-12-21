# Variáveis criadas para unificar informações entre os arquivos setup.py e docs/conf.py
# Variáveis author, copyright e licence utilizadas para criação/atualização do arquivo LICENCE.txt (rotina Make durante processo de atualização do pacote "make update-package")
name = 'dpckan'
version = '0.1.12'
author = 'CONTROLADORIA GERAL DO ESTADO DE MINAS GERAIS - CGE/MG'
email_author = 'dadosabertos@cge.mg.gov.br'
description = 'Funções para gestão de pacotes de dados no portal dados.mg.gov.br'
copyright = f'Copyright 2021 {author}'
licence = """\n
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n
"""

def licence_production():
  """
  Rotina para cria/atualiza arquivo LICENCE.txt sempre que a versão do pacote é atualizada
  Chamada durante processo Make de atualização do pacote

  Parameters
  ----------
  Não recebe nenhum parêmetro

  Returns
  -------
  Arquivo LICENCE.txt criado/atualizado

  """
  with open('LICENCE.txt', 'w') as writer:
    for line in range(2):
      if line == 0:
        writer.writelines(copyright)
      else:
        writer.writelines(licence)

if __name__ == '__main__':
  licence_production()
