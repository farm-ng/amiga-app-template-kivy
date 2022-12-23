# amiga-app-template

This repository is designed to streamline the creation of a new application deployable to the Amiga brain.

For the most up-to-date documentation on using this template repository, please refer to:

[amiga.farm-ng.com - **Developing Custom Applications**](https://amiga.farm-ng.com/docs/brain/brain-apps)

---

## Create a repository from this template

Click on green *Use this template* button (top right) to create a new repository based on this repo

Fill in the details, example below:
* Owner: *username*
* Repository Name: hello-amiga (names should be between 4-17 characters)
* Set to Public

Once completed, click *[Create repository from template]*

When the repository creation process has completed, you have two options:

1. Work in your local workspace.
2. Work in a remote Remote-SSH session using in vs-code.

In both cases you will have to clone the created repository from above

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

## Project structure

In vs-code, you can see the project structure on the left side in the `EXPLORER`:

Below are listed the most important components.

```bash
repository-name/  # Root level of the project.
├── libs/ # Contains private libraries.
|   └── project_name/
|       ├── ops.py  # e.g a operators submodule
|       └── project_name_subpackage/
|           └── utils.py  # e.g a utilities submodule
├── src/ # Contains all code needed to run the main gui application.
|   ├── assets/  # Contains files needed to run the application
|   |   └── app_logo.png  # static images or images for buttons.
|   ├── res/  # Contains the layout files and UI strings.
|   |   └── main.kv  # main ui layout in Kivy languague
|   └── main.py  # Is the main entry point for the gui application.
├── test/  # Contains code for test of the private libs.
|   └── test_dummy.py  # sets of unit test.
├── entry.sh
|    # The script to setup the project, create a virtual env. and install dependencies.
└── setup.cfg
    # The file containing the metadata of the package, including the name, versioning, etc. Learn more here: https://setuptools.pypa.io/en/latest/userguide/declarative_config.html

```

## How to setup the project

Before any changes, lets see if we can run this app locally on your system.

```bash
cd YOUR_REPOSITORY/
./entry.sh  # install and run
```

When running the above script, a virtual environment `venv` will be created and any dependencies will be installed.

If all goes well, you'll see an dummy kivy application on your screen.

## Customizing an app

In order to customize an app we leverage the `setup.cfg` that contains all the metadata and package configuration. More: https://setuptools.pypa.io/en/latest/userguide/declarative_config.html

The most important first steps are to modify the metadata of the project and dependencies:

1. Inside the `setup.cfg` file, adjust the fields under the tag `[metadata]`
    * For basic users, the package name  goes in the `name` field, and must match with the directory name right under the `libs/` directory.
    * For advanced users, you can modify as much is complaint with Python `setuptools`.
2. Adjust the package dependencies
    * Include whatever extra dependency you need in the `install_requires` field.
    * Our only requirements are:
        * `wheel`: for packaging the app.
        * `kivy`: to generate the graphical user interface (GUI).
        * `farm-ng-amiga`: the Farm-ng Amiga public SDK.

In case you face issues, connect with us and the community:
* https://discourse.farm-ng.com/c/support/5



## Development and Debug an app

The workflow for development is pretty much the same as any standard gui application.

1. Make changes in the code.
2. Run the code with the play button in vs-code.
    - [Optionally] Add a breakpoint to any line and use the Debug Console to interact.
3. Go to step 1)


## [Optional] Test your application

In order to validate your functionality, we suggest to add test cases for the internal `libs/[package_name]`
located under `test/test_[test_name].py`.

To launch the tests: `pytest test/`
To run specific tests: `pytest test/test_dummy.py::TestDummy::test_add`


---
## SSH Configuration

Configure your *.ssh/config*
```
Host amiga
    HostName <intranet ip address>
    Port 22
    User amiga
    StrictHostKeyChecking no
```

`<intranet ip address>` can be found on the bottom right of the Amiga Brain screen.

Copy your SSH key to the Amiga
* If you do not have a key created
    ```bash
    ssh-keygen
    ```
```bash
ssh-copy-id amiga
```

---
