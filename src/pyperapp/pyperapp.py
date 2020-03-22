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
import sys
import argparse


def pypr(argv=None):
    """
    Entry point.

    Will print help text if the optional first argument is "help". Otherwise,
    reads the commands and acts as necessary.
    """
    if argv is None:
        argv = sys.argv[1:]
    print("Hello, world!", argv)


if __name__ == "__main__":
    pypr(sys.argv[1:])
