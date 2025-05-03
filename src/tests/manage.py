#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Couldn't import Django!")  # noqa: TRY003, EM101

    execute_from_command_line(sys.argv)
