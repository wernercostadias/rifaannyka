#!/usr/bin/env python3
import sys

from config.settings_loader import configure_django_settings


def main():
    configure_django_settings()
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
