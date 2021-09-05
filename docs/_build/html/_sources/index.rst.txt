.. dpckan documentation master file, created by
   sphinx-quickstart on Sat May 15 09:39:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bem Vindo à documentação dpckan
======================================

Criar conjunto de dados
--------------------------------------
.. automethod:: dpckan.create_dataset.create(ckan_host, ckan_key, datapackage)

.. automethod:: dpckan.create_dataset.create_cli(ckan_host, ckan_key, datapackage)

Atualizar conjunto de dados
-------------------------------------
.. automethod:: dpckan.update_dataset.update(ckan_host, ckan_key, datapackage)

.. automethod:: dpckan.update_dataset.update_cli(ckan_host, ckan_key, datapackage)

Criar recurso
--------------------------------------
.. automethod:: dpckan.create_resource.create_resource(ckan_host, ckan_key, datapackage, resource_name)

.. automethod:: dpckan.create_resource.create_resource_cli(ckan_host, ckan_key, datapackage, resource_name)

Atualizar recurso
--------------------------------------
.. automethod:: dpckan.update_resource.update_resource(ckan_host, ckan_key, datapackage, resource_id, resource_name)

.. automethod:: dpckan.update_resource.update_resource_cli(ckan_host, ckan_key, datapackage, resource_id, resource_name)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
