host_flag_='''
  Host or link to CKAN's instance wanted.
  Example: https://dados.mg.gov.br.
  Not required if CKAN_HOST environment variable is defined.
  '''
key_flag_='''
  CKAN key of the user for the CKAN's environment wanted.
  Not required if CKAN_KEY environment variable is defined.]
  '''
datapackage_flag_='''
  Local path to datapackage.json file.
  Not required if the command run in the same directory as the datapackage.json file
  '''
resource_id_flag_='''
  Resource id to update in CKAN's instance.
  Last part of the resource's URL.
  '''
resource_name_flag_='''
  Name of the resource to be updated.
  Resource's property `name` within the datapackage.json file
  '''
stop_flag_='If provided, stops execution if frictionless validation returns an error'
