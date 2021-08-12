import click

from dapodik import __dapodik_version__, __semester__, __tahun_ajaran__

from . import __version__
from .peserta_didik import peserta_didik


@click.group("dapodix")
def main():
    pass


main.add_command(peserta_didik, "peserta-didik")


@main.command()
def version():
    click.echo(f"Dapodix versi {__version__}")
    click.echo(f"Untuk dapodik {__dapodik_version__}")
    click.echo(f"Semester : {__semester__}")
    click.echo(f"Tahun ajaran : {__tahun_ajaran__}")


if __name__ == "__main__":
    main()
