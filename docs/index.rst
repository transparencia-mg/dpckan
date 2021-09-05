.. dpckan documentation master file, created by
   sphinx-quickstart on Sat May 15 09:39:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bem Vindo à documentação dpckan
======================================

Criar conjunto de dados
--------------------------------------
.. automodule:: dpckan.create_dataset
   :members:

.. automethod:: dpckan.create_dataset.create_cli(ckan_host, ckan_key, datapackage)

Atualizar conjunto de dados
-------------------------------------
.. automodule:: dpckan.update_dataset
   :members:

.. automethod:: dpckan.update_dataset.update_cli(ckan_host, ckan_key, datapackage)

Criar recurso
--------------------------------------
.. automodule:: dpckan.create_resource
   :members:

.. automethod:: dpckan.create_resource.create_resource_cli(ckan_host, ckan_key, datapackage, resource_name)

Atualizar recurso
--------------------------------------
.. automodule:: dpckan.update_resource
   :members:

.. automethod:: dpckan.update_resource.update_resource_cli(ckan_host, ckan_key, datapackage, resource_id, resource_name)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
