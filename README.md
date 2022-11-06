# amiga-brain-example

A Cookiecutter template for creating a Farm-ng Amiga Brain app.

This repository provides a complete example of an application cable of driving our Amiga via CAN.

## TL;DR

Install the Cookiecutter Pip package
```bash
    python3 -m pip install --user cookiecutter
```

Clone a template of this repository
```bash
    cookiecutter https://github.com/farm-ng/amiga-brain-example
```

Install dependencies
```bash
    apps/<your-app>/entry.sh
```
Entry.sh will pull down all required dependencies and install your package in editable mode (pip install -e .)

## Configuration

Configure your *.ssh/config*
```
    Host amiga
        HostName <intranet ip address>
        Port 22
        User amiga
        StrictHostKeyChecking no
```
