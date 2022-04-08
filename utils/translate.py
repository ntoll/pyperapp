#!python3
"""
Translation related utility functions for the PyperApp project. Based on those
created for the Mu project.
"""
import os
import pathlib
import re
import subprocess
import sys


_exported = {}
_PARENT_DIR = pathlib.Path(os.path.dirname(__file__)).parent.absolute()
_MODULE = os.path.join(_PARENT_DIR, "src", "pyperapp")
_LOCALE_DIR = os.path.join(_MODULE, "locale")
_MESSAGES_POT_FILENAME = os.path.join(_LOCALE_DIR, "messages.pot")


def export(function):
    """
    Decorator to tag certain functions as exported, meaning
    that they show up as a command, with arguments, when this
    file is run.
    """
    _exported[function.__name__] = function
    return function


def _translate_lang(lang):
    """
    Returns `value` from `lang` expected to be like 'LANG=value'.
    """
    match = re.search(r"^LANG=(.*)$", lang)
    if not match:
        raise RuntimeError("Need LANG=xx_XX argument.")
    value = match.group(1)
    if not value:
        raise RuntimeError("Need LANG=xx_XX argument.")
    return value


def _translate_filenames():
    """
    Returns a sorted list of filenames with translatable strings.
    """
    py_filenames = []
    for dirname, _, filenames in os.walk(_MODULE):
        py_filenames.extend(
            os.path.join(dirname, fn) for fn in filenames if fn.endswith(".py")
        )
    return sorted(py_filenames)


def _translate_extract():
    """
    Creates the message catalog template messages.pot file.
    """
    cmd = [
        "pybabel",
        "extract",
        "-o",
        _MESSAGES_POT_FILENAME,
        *_translate_filenames(),
    ]
    return subprocess.run(cmd).returncode


@export
def translate_begin(lang=""):
    """
    Create/update a pyperapp.po file for translation.
    """
    lang = _translate_lang(lang)
    result = _translate_extract()
    if result != 0:
        raise RuntimeError("Failed creating the messages catalog file.")

    po_filename = os.path.join(
        _LOCALE_DIR,
        lang,
        "LC_MESSAGES",
        "pyperapp.po",
    )
    update = os.path.exists(po_filename)
    cmd = [
        "pybabel",
        "update" if update else "init",
        "-i",
        _MESSAGES_POT_FILENAME,
        "-o",
        po_filename,
        f"--locale={lang}",
    ]
    result = subprocess.run(cmd).returncode

    print(
        "{action} {po_filename}.".format(
            action="Updated" if update else "Created",
            po_filename=repr(po_filename),
        )
    )
    print(
        "Review its translation strings "
        "and finalize with 'make translate_done'."
    )


@export
def translate_done(lang=""):
    """
    Compile translation strings in pyperapp.po to a pyperapp.mo file.
    """
    lang = _translate_lang(lang)

    lc_messages_dirname = os.path.join(
        _LOCALE_DIR,
        lang,
        "LC_MESSAGES",
    )
    po_filename = os.path.join(lc_messages_dirname, "pyperapp.po")
    mo_filename = os.path.join(lc_messages_dirname, "pyperapp.mo")
    cmd = [
        "pybabel",
        "compile",
        "-i",
        po_filename,
        "-o",
        mo_filename,
        f"--locale={lang}",
    ]
    return subprocess.run(cmd).returncode


def main(command="help", *args):
    """
    Dispatch on command name, passing all remaining parameters to the
    module-level function.
    """
    try:
        function = _exported[command]
    except KeyError:
        raise RuntimeError("No such command: %s" % command)
    else:
        return function(*args)


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
