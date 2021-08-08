import click

from . import __version__, __dapodik_version__
from .peserta_didik import peserta_didik


def main():
    cli = click.CommandCollection("dapodix", sources=[peserta_didik])
    cli()


if __name__ == "__main__":
    main()
