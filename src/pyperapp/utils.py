"""
Utility functions used by PyperApp for various tasks. These are called by the
Click based command line tool.
"""
import click
import datetime
import http.server
import os
import requests
import socketserver
import threading
import time
import tomli
import webbrowser
from jinja2 import Environment, FileSystemLoader, select_autoescape


_SRC_PATH = "https://brython.info/src/"
_BRYTHON = "brython.js"
_STDLIB = "brython_stdlib.js"


def _get_brython(target_dir=None):
    """
    Gets the latest version of Brython and the standard library for inclusion
    in PyperApp projects.

    If target_dir is defined, will save the assets in there. Otherwise, will
    save the assets in the current working directory.
    """
    target_path = os.path.abspath(target_dir or "")
    brython_response = requests.get(_SRC_PATH + _BRYTHON)
    with open(os.path.join(target_path, _BRYTHON), "w") as brython_file:
        brython_file.write(brython_response.text)
    stdlib_response = requests.get(_SRC_PATH + _STDLIB)
    with open(os.path.join(target_path, _STDLIB), "w") as stdlib_file:
        stdlib_file.write(stdlib_response.text)


def _get_templates_for(name: str) -> str:
    """
    Returns a string containing the absolute path to the templates for the
    utility function referenced by name.
    """
    template_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "templates", name)
    )
    return Environment(
        loader=FileSystemLoader(template_path), autoescape=select_autoescape()
    )


def _render_templates(templates: Environment, context: dict, target: str):
    """
    Given a template environment and a context, render all the templates, while
    retaining the directory structure found in the templates, to the target
    directory.
    """
    target = os.path.abspath(target)
    # Ensure the target directory exists.
    if not os.path.exists(target):
        os.makedirs(target)
    # Update the global context so all the context values are available in
    # all templates.
    templates.globals = templates.globals | context
    # Render the templates into the target directory based on their own path
    # within the template environment.
    for template_name in templates.list_templates():
        target_file = os.path.join(target, template_name)
        subdir = os.path.dirname(template_name)
        if subdir:
            os.makedirs(os.path.join(target, subdir), exist_ok=True)
        with open(target_file, "w") as output:
            template = templates.get_template(template_name)
            output.write(template.render())


def create(name: str, author: str, description: str, version: str) -> None:
    """
    Given a name, author, description, year and PyperApp version, creates the
    skeleton of a PyperApp, from templates, in a directory created in the
    current working directory, with the same name as the project.
    """
    target = os.path.join(os.getcwd(), name)
    templates = _get_templates_for("create")
    now = datetime.datetime.utcnow()
    context = {
        "name": name,
        "author": author,
        "description": description,
        "version": version,
        "year": now.year,
        "now": now,
    }
    _render_templates(templates, context, target)


def build() -> None:
    """
    Attempts to build the app's assets and bundles them into the `dist`
    subdirectory. This should be a stand-alone browser app.
    """
    try:
        with open("manifest.toml", "rb") as manifest_file:
            manifest = tomli.load(manifest_file)
    except Exception:
        raise RuntimeError(
            _"Could not parse manifest.toml. Are you in a PyperApp directory?"
            )


def run() -> None:
    """
    Attempts to start a simple web-server and start Chrome in "app" mode by
    pointing at the new instance.
    """
    build()
    port = 8888
    try:
        chrome = webbrowser.get("chromium")
    except webbrowser.Error:
        click.echo("You must have Chrome installed.")
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    def start_browser(chrome=chrome, httpd=httpd):
        """
        Inner function to start the browser after a pause, on a new thread.
        """
        time.sleep(0.2)
        chrome.remote_args.append("--window-size=800,600")
        chrome.open_new(f"--app=http://localhost:{port}/index.html")
        time.sleep(0.2)
        httpd.shutdown()

    browser_thread = threading.Thread(target=start_browser)
    browser_thread.start()
    httpd.serve_forever()
