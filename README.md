# PyperApp

An evolution of [PyperCard](https://pypercard.readthedocs.io/) for the browser.

A spikey work in progress. A though experiment in code. Use at your own risk.

## Developer setup

These instructions are for developers working on developing PyperApp
**itself**. They are **NOT** for folks wishing to develop applications _with_
PyperApp. Instructions for _users of PyperApp_ are in our documentation found
in the `docs` directory of this repository.

Create a clean virtual environment:

```
$ python3 -m venv my_venv
```

Activate it (Linux/OSX):

```
$ source my_venv/bin/active
```

Activate it (Windows):

```
my_venv\Scripts\activate
```

Ensure you have up-to-date versions of packaging tools:

```
$ python3 -m pip install --upgrade pip setuptools wheel
```

Install the requirements needed for local development of this project:

```
$ python3 -m pip install -r requirements.txt
```

On Linux/OSX the `Makefile` contains various shortcuts for common tasks. If
you're a Windows user, please look inside the `Makefile` for the Pythonic
commands we use to fulfil these various tasks.
