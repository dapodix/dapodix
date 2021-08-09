import click
from dapodix import ClickContext, ContextObject
from dapodix.utils import parse_range

from .registrasi import RegistrasiPesertaDidik


@click.group(name="peserta_didik", invoke_without_command=True)
@click.option("--email", required=True, help="Email dapodik")
@click.option(
    "--password",
    required=True,
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password dapodik",
)
@click.option("--server", default="http://localhost:5774/", help="URL aplikasi dapodik")
@click.pass_context
def peserta_didik(ctx: ClickContext, email: str, password: str, server: str):
    ctx.ensure_object(ContextObject)
    ctx.obj.username = email
    ctx.obj.password = password
    ctx.obj.server = server
    if ctx.invoked_subcommand is None:
        dapodik = ctx.obj.dapodik
        sekolah = dapodik.sekolah()
        click.echo("Daftar Peserta didik")
        for pd in dapodik.peserta_didik(sekolah_id=sekolah.sekolah_id):
            click.echo(str(pd))


@peserta_didik.command()
@click.option("--sheet", default="Peserta Didik", help="Nama sheet dalam file excel")
@click.option(
    "--range",
    required=True,
    help="Baris data yang akan di masukkan misal 1-10",
)
@click.argument("filepath", type=click.Path(exists=True), required=True)
@click.pass_context
def registrasi(
    ctx,
    filepath: str,
    sheet: str,
    range: str,
):
    return RegistrasiPesertaDidik(
        dapodik=ctx.obj.dapodik, filepath=filepath, sheet=sheet, rows=parse_range(range)
    )
