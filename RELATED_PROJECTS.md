## Projetos relacionados
Por que utilizar `dpckan`?
`dpckan` permite que o usuário carregue e atualize conjuntos de dados e recursos em uma instância CKAN de forma remota, via CLI. Sem o `dpckan`, um usuário precisaria logar na plataforma CKAN manualmente e carregar os recursos e conjuntos de dados um por um. Para grandes quantidades de dados, isso não é prático.
Outros pacotes implementam integrações Frictionless-CKAN:
- [ckanext-datapackager](https://github.com/frictionlessdata/ckanext-datapackager): extensão CKAN para importar/exportar Data Packages, mas funciona apenas com Python 2.7
- [frictionless-py](https://framework.frictionlessdata.io/docs/tutorials/formats/ckan-tutorial/): plugin CKAN que mapeia os Data Packages do Frictionless no formato utilizado pelo CKAN, mas que não possui o acesso remoto à aplicação.
- [datapackage-pipelines-ckan](https://github.com/frictionlessdata/datapackage-pipelines-ckan): pipelines de processamento de Data Packages do Frictionless para CKAN, não são atualizados há algum tempo.

`dpckan` integra todas essas funcionalidades em um pacote fácil de usar.


## Related projects 
Why should I use `dpckan`?
`dpckan` allows the user to upload and update CKAN datasets and resources remotely from the command line outside the CKAN application. Without `dpckan`, the user would have to manually log in to the CKAN application and upload the resources and data packages one by one. For large amounts of data, that is impractical. 
Other packages integrate Frictionless and CKAN:
- [ckanext-datapackager](https://github.com/frictionlessdata/ckanext-datapackager): CKAN extension for importing/exporting Data Packages, but works only with Python 2.7
- [frictionless-py](https://framework.frictionlessdata.io/docs/tutorials/formats/ckan-tutorial/): CKAN plugin that maps the Frictionless Data Packages to CKAN format but doesn't account for the remote access
- [datapackage-pipelines-ckan](https://github.com/frictionlessdata/datapackage-pipelines-ckan): Data Package Pipelines processors for CKAN, but it hasn't been updated in a while.

`dpckan` integrates all of these features in an easy-to-use package.



