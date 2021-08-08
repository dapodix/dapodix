import click

from . import __version__, __dapodik_version__
from .peserta_didik import peserta_didik


@click.group("dapodix")
def main():
    pass


main.add_command(peserta_didik, "peserta_didik")


if __name__ == "__main__":
    main()
