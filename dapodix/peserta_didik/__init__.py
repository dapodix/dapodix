import click
import random

from dapodix import ClickContext, ContextObject
from dapodix.utils import parse_range

from .random_longitudinal import RandomLongitudinal
from .registrasi import RegistrasiPesertaDidikCommand


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
    ctx: ClickContext,
    filepath: str,
    sheet: str,
    range: str,
):
    return RegistrasiPesertaDidikCommand(
        dapodik=ctx.obj.dapodik, filepath=filepath, sheet=sheet, rows=parse_range(range)
    )


@peserta_didik.command()
@click.option("--tinggi-badan", required=True)
@click.option("--berat-badan", required=True)
@click.option("--lingkar-kepala", required=True)
@click.option("--jarak-rumah", required=True)
@click.option("--jarak-ke-waktu", type=int, required=True)
@click.pass_context
def random_longitudinal(
    ctx: ClickContext,
    tinggi_badan: str,
    berat_badan: str,
    lingkar_kepala: str,
    jarak_rumah: str,
    jarak_ke_waktu: int,
):
    return RandomLongitudinal(
        dapodik=ctx.obj.dapodik,
        tinggi=lambda: random.choice(parse_range(tinggi_badan)),
        berat=lambda: random.choice(parse_range(berat_badan)),
        lingkar_kepala=lambda: random.choice(parse_range(lingkar_kepala)),
        jarak_rumah=lambda: random.choice(parse_range(jarak_rumah)),
        jarak_waktu=jarak_ke_waktu,
    )
