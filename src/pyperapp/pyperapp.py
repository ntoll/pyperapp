#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
PyperApp - it all starts here.

PyperCard inspired applications in your browser via Brython. This module
provides commands for users to set up everything and carry our common tasks.
As `manage.py` is to Django, so `pypr` is to PyperApp.

Copyright © 2020 Nicholas H.Tollervey

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import appdirs
import click
import datetime
import gettext
import importlib
import locale
import logging
import os
import sys
from . import utils


__version__ = importlib.metadata.version("pyperapp")


#: Flag to indicate if the command is being run in verbose mode.
VERBOSE = False
#: The directory containing the utility's log file.
LOG_DIR = appdirs.user_log_dir(appname="pyperapp", appauthor="ntoll")
#: The location of the log file for the utility.
LOGFILE = os.path.join(LOG_DIR, "pyperapp.log")


# Ensure LOG_DIR related directories and files exist.
if not os.path.exists(LOG_DIR):  # pragma: no cover
    os.makedirs(LOG_DIR)


# Setup logging.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logfile_handler = logging.FileHandler(LOGFILE)
log_formatter = logging.Formatter("%(levelname)s: %(message)s")
logfile_handler.setFormatter(log_formatter)
logger.addHandler(logfile_handler)


# Configure language/locale setup.
language_code = locale.getlocale()[0]
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "locale"))
gettext.translation(
    "pyperapp", localedir=localedir, languages=[language_code], fallback=True
).install()


@click.group(help=_("Manage PyperApp projects."))
@click.option(
    "--verbose", is_flag=True, help=_("Comprehensive logging sent to stdout.")
)
@click.version_option(
    version=__version__,
    prog_name="pypr",
    message=_("%(prog)s, a PyperApp management tool. Version %(version)s."),
)
def pypr(verbose):
    """
    Entry point.
    """
    if verbose:
        # Configure additional logging to stdout.
        global VERBOSE
        VERBOSE = True
        verbose_handler = logging.StreamHandler(sys.stdout)
        verbose_handler.setLevel(logging.INFO)
        verbose_handler.setFormatter(log_formatter)
        logger.addHandler(verbose_handler)
        click.echo(_("Logging to {}\n").format(LOGFILE))
    now = datetime.datetime.now()
    logger.info(_("### Started ") + str(now))


@pypr.command(help=_("Create a new PyperApp with the given name."))
@click.argument("name", nargs=1)
def create(name):
    """
    Prompts user for arguments before handing over to the utility function.
    """
    click.echo(_("Creating new PyperApp {}").format(name))
    author = click.prompt(_("Author's name"))
    description = click.prompt(_("A brief project description"))
    utils.create(name, author, description, __version__)
    click.echo(
        _("Your new PyperApp is in the '{}' subdirectory.").format(name)
    )
    click.echo(
        _("Change into the directory and type, 'pypr run' to check it works.")
    )


@pypr.command(help=_("Run the application in the current directory."))
def run():
    """
    Attempts to run the application found in the current directory. Will try to
    find a valid manifest.toml file. If found, will copy the app settings
    somewhere temporary and serve it. Finally, it'll open Chromium in app mode
    for the application.
    """
    utils.run()

if __name__ == "__main__":
    pypr()
