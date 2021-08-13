import click
import random

from dapodik import __semester__

from dapodix import ClickContext, ContextObject
from dapodix.utils import parse_range

from .excel import (
    DATA_INDIVIDU,
    DATA_REGISTRASI,
    DATA_AYAH,
    DATA_IBU,
    DATA_LONGITUDINAL,
    ALL_DATA_INDIVIDU,
)
from .eksport import EksporPesertaDidikCommand
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
@click.option("--semester", default=__semester__, help="Semester id")
@click.pass_context
def peserta_didik(ctx: ClickContext, email: str, password: str, server: str, semester: str):
    ctx.ensure_object(ContextObject)
    ctx.obj.username = email
    ctx.obj.password = password
    ctx.obj.server = server
    ctx.obj.semester = semester
    if ctx.invoked_subcommand is None:
        dapodik = ctx.obj.dapodik
        sekolah = dapodik.sekolah()
        click.echo("Daftar Peserta didik")
        for pd in dapodik.peserta_didik(sekolah_id=sekolah.sekolah_id):
            click.echo(str(pd))


@peserta_didik.command()
@click.option("--sheet", default="Peserta Didik", help="Nama sheet dalam file excel")
@click.option(
    "--header/--no-header",
    default=True,
    help="Tambah header setiap kolom",
)
@click.argument("filepath", type=click.Path(), required=True)
@click.pass_context
def ekspor(ctx: ClickContext, sheet: str, header: bool, filepath: str):
    return EksporPesertaDidikCommand(
        dapodik=ctx.obj.dapodik,
        filepath=filepath,
        sheet=sheet,
        header=header,
    )


@peserta_didik.command()
@click.option("--sheet", default="Peserta Didik", help="Nama sheet dalam file excel")
@click.option(
    "--range",
    required=True,
    help="Baris data yang akan di masukkan misal 1-10",
)
@click.option(
    "--registrasi/--no-registrasi",
    default=True,
    help="Proses registrasi",
)
@click.option(
    "--longitudinal/--no-longitudinal",
    default=True,
    help="Proses data periodik",
)
@click.argument("filepath", type=click.Path(exists=True), required=True)
@click.pass_context
def registrasi(
    ctx: ClickContext,
    filepath: str,
    sheet: str,
    range: str,
    registrasi: bool,
    longitudinal: bool,
):
    return RegistrasiPesertaDidikCommand(
        dapodik=ctx.obj.dapodik,
        filepath=filepath,
        sheet=sheet,
        rows=parse_range(range),
        skip_registrasi=not registrasi,
        skip_longitudinal=not longitudinal,
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
