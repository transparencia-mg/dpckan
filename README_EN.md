# Data package manager for CKAN (dpckan)

`dpckan` is a Python package, accessible via the [CLI](https://en.wikipedia.org/wiki/Command-line_interface) interface, used for creating and updating datasets and resources (documented according to the [Frictionless Data](https://frictionlessdata.io/)) metadata standard in an instance of [CKAN](https://ckan.org/).

[Additional documentation](https://dpckan.readthedocs.io/en/latest/)

## Installation

`dpckan` is available in the Python Package Index - [PyPI](https://pypi.org/project/dpckan/) and can be installed using the command below:

```bash
# Before executing the command below remember that Python environment must be active
$ pip install dpckan
```

## Setting Environment Variables

All commands require the indication of a CKAN instance (eg https://demo.ckan.org/) and a valid key for authentication in that instance. This indication must be done through the registration of environment variables. For CLI invocation of any command without the need to explicitly indicate these variables, it is recommended to use the names `CKAN_HOST` and `CKAN_KEY` to register instance and key respectively. If other names are used, it is necessary to explicitly indicate during the call of the desired function, using the flags "--ckan-host" and "--ckan-key", as shown below and/or in more detail in the section [Usage ](#use).


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

The registration of environment variables `CKAN_HOST` and `CKAN_KEY`, necessary for invoking each command, must be performed according to the user's operating system. Below are reference links for this:

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

### Interrupting execution in case of frictionless validation errors

During the execution of the dpckan commands the `frictionless` library will be used to [validate](https://framework.frictionlessdata.io/docs/guides/validation-guide) local dataset via `frictionless validate`. Errors during this validation will be reported to the user but they will only interrupt execution if the `--stop` flag is passed as a parameter, as shown below:

```bash
$ dpckan dataset create --stop
```

### Creating and Updating a Dataset via Terminal

- To create a dataset, run the command in the directory where the datapackage.json file is located:

```bash
$dpckan dataset create
```

- And to update the dataset, execute the command in the directory where the datapackage.json file is located:

```bash
$ dpckan dataset update
```



### Creating and Updating Resources via Terminal

- To create a resource, run the following command in the directory where the datapackage.json file is located. Don't forget to modify the last argument with the name of the resource present in the datapackage.json file that will be created

```bash
$ dpckan resource create --resource-name resource-name

# Use alias -rn for flag --resource-name
$ dpckan resource create -rn resource-name
```


- To update a resource, run the following command in the directory where the datapackage.json file is located. Don't forget to modify the last arguments with the name and id of the resource present in the datapackage.json file that will be updated

```bash
# Usage flags --resource-name and --resource-id
$ dpckan resource update --resource-name resource-name --resource-id resource-id

# Use -rn and -id aliases for --resource-name and --resource-id flags respectively
$ dpckan resource update -rn resource-name -id resource-id
```

### Using flags

- It is possible to update a dataset or resource outside the directory where the datapackage.json file is located using the `--datapackage` or `-dp` flag as below:

```bash
# Use flag --datapackage
$ dpckan resource update --datapackage local/path/to/datapackage.json --resource-name resource-name --resource-id resource-id

# Use -dp, -rn and -id aliases for --datapackage,--resource-name and --resource-id flags respectively
$ dpckan resource update -dp local/path/to/datapackage.json -rn resource-name -id resource-id
```
- We can use the flags `-H` for `CKAN_HOST`, `-k` for `CKAN_KEY`, `-rn` for `--resource_name` and `-id` for `--resource_id`

- You can also use `CKAN_KEY` and `CKAN_HOST` with the name and id of a resource to update it, for example:

```bash
# Usage flags --ckan-host, --ckan-key, --resource-name and --resource-id
$ dpckan resource update --ckan-host $CKAN_HOST_PRODUCTION --ckan-key $CKAN_KEY_PRODUCTION --resource-name resource-name --resource-id resource-id

# Use -H, -k, -rn and -id aliases for --ckan-host, --ckan-key, --resource-name and --resource-id flags respectively
$ dpckan resource update -H $CKAN_HOST_PRODUCTION -k $CKAN_KEY_PRODUCTION -rn resource-name -id resource-id
```

For more examples, see the [documentation](https://dpckan.readthedocs.io/en/latest/)


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
