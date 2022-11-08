# amiga-brain-example

This repository is designed to streamline the creation of a new application deployable to the Amiga brain.

Please note, to properly utilize this template, please install the Python cookiecutter package from PyPi.
```bash
    python3 -m pip install --user cookiecutter
```

---
## TL;DR :: How to use this

Install the Cookiecutter Pip package
```bash
    python3 -m pip install --user cookiecutter
```

Click on *Use this template* to create a new repository based on this repo

Fill in the details, example below:
* Owner: *<your Github username>*
* Repository Name: hello-amiga (names should be between 4-17 characters)
* Set to Public

Once completed, click *Create repository from template*

When the repository creation process has completed, clone the repo to your local workspace

Your now ready to create your first Kivy app, please choose a name between 4 and 17 characters run the *create app.sh* script
```bash
    ./create_app.sh
```

Enter your full name, press enter and enter your chosen app name as well. Press enter again and once more to accept the formatted package name

Your kivy application has been created under the *apps* directory
```bash
    ls apps/
```

Before any changes, lets see if we can run this app.
```bash
    apps/<your app name>/entry.sh
```

When running the above script, a virtual environment will be created under the *<application>* directory and any dependencies will be installed.

If all goes well, you'll see an empty kivy application on your screen.


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

Copy your SSH key to the Amiga
* If you do not have a key created
    ```bash
        ssh-keygen
    ```
```bash
    ssh-copy-id amiga
```

---
## Customizing an app
==TODO==

---
## Publish an app

To publish an app to the Amiga, run the *sync.sh* script located in the app's folder.
```bash
    apps/==<your app name>==/sync.sh
```

To see your app on the Amiga screen, cause a refresh by tapping the settings screen then pressing the home button on the top right.
