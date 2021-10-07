# Data package manager for CKAN (dpckan)

`dpckan` is a Python package, accessible via the [CLI](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos), used for creating and updating datasets and resources (according to the [Frictionless Data](https://frictionlessdata.io/)) standard of metadata in an instance of [CKAN](https://ckan.org/).

[Additional documentation](https://dpckan.readthedocs.io/en/latest/)

## Installation

`dpckan` is available in the Python Package Index - [PyPI](https://pypi.org/project/dpckan/) and can be installed using the command below:

```bash
# Before executing the command below remember to activate the Python environment
$ pip install dpckan
```

## Setting Environment Variables

All commands require the indication of a CKAN instance (eg https://demo.ckan.org/) and a valid key for authentication in that instance. This indication must be done through the registration of environment variables. For CLI invocation of any command without the need to explicitly indicate these variables, it is recommended to use the names `CKAN_HOST` and `CKAN_KEY` to register instance and key respectively. If other names are used, it is necessary to explicitly indicate them during the call to the desired function, using the flags "--ckan-host" and "--ckan-key", as shown below and/or in more detail in the section [Usage ](#use).


```bash
# CKAN_HOST=https://demo.ckan.org/
# CKAN_KEY=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (CKAN Key for illustrative purposes only)
# Use without the need to explicitly specify variables
$dpckan dataset create

# CKAN_HOST_PRODUCAO=https://demo.ckan.org/
# CKAN_KEY_PRODUCAO=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (CKAN Key for illustrative purposes only)
# Usage by explicitly specifying variables, via --ckan-host and --ckan-key flags
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCTION --ckan-key $CKAN_KEY_PRODUCTION

```

The registration of environment variables `CKAN_HOST` and `CKAN_KEY`, needed for invoking each command, must be performed according to the user's operating system. Below are reference links for this:

  * [Windows](https://professor-falken.com/pt/windows/como-configurar-la-ruta-y-las-variables-de-entorno-en-windows-10/)
  * [Linux](https://ricardo-reis.medium.com/vari%C3%A1veis-de-ambiente-no-linux-debian-f677d6ca94c)
  * [Mac](https://support.apple.com/en-us/guide/terminal/apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac)


Alternatively, the registration of these environment variables can be done in a ".env" file, at the root of the dataset, it being necessary to include this ".env" in a ".gitignore" file, thus avoiding the synchronization and consequent publication of these keys in online repositories such as [github](https://github.com/), as shown below:


```bash
# ONLY USE THE SUGGESTED OPTION BELOW IF YOU ARE FAMILY WITH THE SUBJECT, THUS AVOIDING PROBLEMS WITH ACCESS BY UNAUTHORIZED THIRD PARTIES IN YOUR CKAN INSTANCE
# CAUTION: ONLY RUN THE COMMANDS BELOW IF THE ".env" and ".gitignore" FILES DO NOT EXIST IN THE DATASET ROOT
# CAUTION: IF THE COMMANDS BELOW ARE EXECUTED WITH ".env" and ".gitignore" EXISTING, ALL CONTENT WILL BE DELETED
# CAUTION: ONLY RUN THE COMMANDS BELOW IF YOU ARE SURE AND KNOWLEDGE OF WHAT WILL BE DONE

# Create ".env" file with structure to receive CKAN_HOST and CKAN_KEY keys
# After creation, open the file and include the values ​​for each variable
$ echo "CKAN_HOST=''\nCKAN_KEY=''" > .env

# Create ".gitignore" file with setting to exclude ".env" file from git version control
$ echo ".env" > .gitignore

# Check if the configuration was successful
# Command below should show only creation/modification of ".gitignore" file, nothing being shown for ".env" file
$ git status
```

## Usage

**WARNING: CHECK THE ENVIRONMENT VARIABLES AND THE FILE PATH BEFORE EXECUTING EACH COMMAND. DO NOT COPY AND PASTE THE CODE BLINDLY!**

### Accessing dpckan documentation via terminal

```bash
# General information about the package and its commands
# Using the --help or -h flags will return the same result
$dpckan

# Information about dataset and resource commands
# Using the --help or -h flags will return the same result
$dpckan dataset
$dpckan resource

# Information about dataset subcommands
# Using the -h flag will return the same result
$ dpckan dataset create --help
$ dpckan dataset update --help

# Information about resource subcommands
# Using the -h flag will return the same result
$ dpckan resource create --help
$ dpckan resource update --help
```

### Dataset creation via terminal

- Run the command in the directory where the datapackage.json file is located:

```bash
$dpckan dataset create
```

- Run the command outside the directory where the datapackage.json file is located
  - Modify the last argument with the local path to datapackage.json file

```bash
# Use flag --datapackage
$ dpckan dataset create --datapackage local/path/to/datapackage.json

# Use alias -dp for flag --datapackage
$ dpckan dataset create -dp local/path/to/datapackage.json
```

- Run the command in the directory where the datapackage.json file is located
  - Change the name of the environment variables to your reality

```bash
# Usage flag --ckan-host and --ckan-key
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCTION --ckan-key $CKAN_KEY_PRODUCTION

# Use -H and -k aliases for --ckan-host and --ckan-key flags respectively
$ dpckan dataset create -H $CKAN_HOST_PRODUCTION -k $CKAN_KEY_PRODUCTION
```



### Dataset update via terminal

- Run the command in the directory where the datapackage.json file is located:

```bash
$ dpckan dataset update
```

- Run the command outside the directory where the datapackage.json file is located
  - Modify the last argument with the local path to datapackage.json file

```bash
# Use flag --datapackage
$ dpckan dataset update --datapackage local/path/to/datapackage.json

# Use alias -dp for flag --datapackage
$ dpckan dataset update -dp local/path/to/datapackage.json
```

- Run the command in the directory where the datapackage.json file is located
  - Change the name of the environment variables to your reality):

```bash
# Usage flag --ckan-host and --ckan-key
$ dpckan dataset update --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

# Use -H and -k aliases for --ckan-host and --ckan-key flags respectively
$ dpckan dataset update -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO
```


### Resource creation via terminal

- Run the command in the directory where the datapackage.json file is located
  - Modify the last argument with the name of the resource present in the datapackage.json file that will be created

```bash
$ dpckan resource create --resource-name resource-name

# Use alias -rn for flag --resource-name
$ dpckan resource create -rn resource-name
```

- Run the command outside the directory where the datapackage.json file is located
  - Modify the local path to datapackage.json file and the resource name to your reality

```bash
# Usage --datapackage and --resource-name flags
$ dpckan resource create --datapackage local/path/to/datapackage.json --resource-name resource-name

# Use -dp and -rn aliases for --datapackage and --resource-name flags respectively
$ dpckan resource create -dp local/path/to/datapackage.json -rn resource-name
```

- Run the command in the directory where the datapackage.json file is located
  - Modify the resource name and the name of the environment variables to your reality

```bash
# Usage flags --resource-name, --ckan-host and --ckan-key
$ dpckan resource create --resource-name resource-name --ckan-host $CKAN_HOST_PRODUCTION --ckan-key $CKAN_KEY_PRODUCTION

# Use -rn, -H and -k aliases for --resource-name, --ckan-host and --ckan-key flags respectively
$ dpckan resource create -rn resource-name -H $CKAN_HOST_PRODUCTION -k $CKAN_KEY_PRODUCTION
```


### Resource update via terminal

- Run the command in the directory where the datapackage.json file is located
  - Modify the last arguments with the name and id of the resource present in the datapackage.json file that will be updated

```bash
# Usage flags --resource-name and --resource-id
$ dpckan resource update --resource-name resource-name --resource-id resource-id

# Use -rn and -id aliases for --resource-name and --resource-id flags respectively
$ dpckan resource update -rn resource-name -id resource-id
```

- Run the command outside the directory where the datapackage.json file is located
  - modify the local path to datapackage.json file, the resource name and id to your reality

```bash
# Use flag --datapackage
$ dpckan resource update --datapackage local/path/to/datapackage.json --resource-name resource-name --resource-id resource-id

# Use -dp, -rn and -id aliases for --datapackage,--resource-name and --resource-id flags respectively
$ dpckan resource update -dp local/path/to/datapackage.json -rn resource-name -id resource-id
```

- Run the command in the directory where the datapackage.json file is located
  - Modify the name of the environment variables, the name and id of the resource to your reality

```bash
# Usage flags --ckan-host, --ckan-key, --resource-name and --resource-id
$ dpckan resource update --ckan-host $CKAN_HOST_PRODUCTION --ckan-key $CKAN_KEY_PRODUCTION --resource-name resource-name --resource-id resource-id

# Use -H, -k, -rn and -id aliases for --ckan-host, --ckan-key, --resource-name and --resource-id flags respectively
$ dpckan resource update -H $CKAN_HOST_PRODUCTION -k $CKAN_KEY_PRODUCTION -rn resource-name -id resource-id
```


## Development

### Contribute to the project

- Prerequisites:
    - Python 3.9 or higher

- [Reference documentation showing procedures required for contributing to an open source project](https://www.dataschool.io/how-to-contribute-on-github/)

- Basic steps:
    - Create a project repository fork
    - Clone the repository created in your account after the fork
    - Navigate to the cloned repository on your machine
    - Create and activate a Python virtual environment to use the project

- Create a branch to make the necessary changes
- Push the created branch
- Open a PR explaining the reasons for the change and how it will help in the development of the project

### Update version

As reported in [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), version update on [Pypi](https://pypi.org/) must follow [these steps ](https://github.com/dados-mg/dpckan/issues/6#issuecomment-851678297)

## License

**dpckan** is licensed under the MIT license.
See the [`LICENSE.md`](LICENSE.md) file for more details.
