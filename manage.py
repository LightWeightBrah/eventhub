#!/usr/bin/env python
"""Narzędzie wiersza poleceń Django do zadań administracyjnych."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventhub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nie można zaimportować Django. Czy środowisko wirtualne .venv jest aktywne "
            "i czy zainstalowano zależności (pip install -r requirements.txt)?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
