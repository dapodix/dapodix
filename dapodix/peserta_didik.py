import click
from cachetools import cachedmethod
from operator import attrgetter
from typing import Any, Dict, List

from dapodik import Dapodik
from dapodik.customrest import Wilayah
from dapodik.peserta_didik import PesertaDidik, CreatePesertaDidik
from dapodik.rest import Agama, JenjangPendidikan, Pekerjaan, Penghasilan

from dapodix import ContextObject, ClickContext
from dapodix.utils import get_data_excel, parse_range

DATA_INDIVIDU = {
    "nama": "B",
    "jenis_kelamin": "C",
    "nik": "D",
    "no_kk": "E",
    "tempat_lahir": "F",
    "tanggal_lahir": "G",
    "reg_akta_lahir": "H",
    "agama_id": "I",
    "alamat_jalan": "J",
    "rt": "K",
    "rw": "L",
    "nama_dusun": "M",
    "kode_wilayah": "N",
    "desa_kelurahan": "O",
    "kode_pos": "P",
    "anak_keberapa": "Q",
}

DATA_AYAH = {
    "nama_ayah": "R",
    "nik_ayah": "S",
    "tahun_lahir_ayah": "T",
    "jenjang_pendidikan_ayah": "U",
    "pekerjaan_id_ayah": "V",
    "penghasilan_id_ayah": "W",
}

DATA_IBU = {
    "nama_ibu_kandung": "X",
    "nik_ibu": "Y",
    "tahun_lahir_ibu": "Z",
    "jenjang_pendidikan_ibu": "AA",
    "pekerjaan_id_ibu": "AB",
    "penghasilan_id_ibu": "AC",
}


class RegistrasiPesertaDidik:
    nisn = ""
    kebutuhan_khusus_id = 0
    lintang = 0
    bujur = 0
    jenis_tinggal_id = 1
    alat_transportasi_id = 1
    anak_keberapa = 1
    penerima_kps = 0
    penerima_kip = 0
    layak_pip = 0
    id_layak_pip = None
    kewarganegaraan = "ID"
    no_kks = ""
    no_kps = ""
    no_kip = ""
    nm_kip = 0
    # Data Ayah Kandung
    kebutuhan_khusus_id_ayah = 0
    # Data Ibu Kandung
    kebutuhan_khusus_id_ibu = 0
    # Data Wali
    nama_wali = ""
    nik_wali = ""
    tahun_lahir_wali = ""
    jenjang_pendidikan_wali = 0
    pekerjaan_id_wali = 0
    penghasilan_id_wali = 0
    # Kontak
    nomor_telepon_rumah = ""
    nomor_telepon_seluler = ""
    email = ""

    def __init__(
        self,
        dapodik: Dapodik,
        filepath: str,
        sheet: str,
        rows: List[int],
    ):
        self.dapodik = dapodik
        self.filepath = filepath
        self.sheet = sheet
        self.rows = rows
        self.sekolah = self.dapodik.sekolah()
        self.penghasilan_cache: Dict[tuple, int] = dict()
        self.agama_cache: Dict[str, int] = dict()
        self.kode_wilayah_cache: Dict[str, str] = dict()
        self.jenjang_pendidikan_cache: Dict[str, int] = dict()
        self.pekerjaan_cache: Dict[str, int] = dict()
        self.AGAMA: List[Agama] = self.dapodik.agama()
        self.JENJANG_PENDIDIKAN: List[
            JenjangPendidikan
        ] = self.dapodik.jenjang_pendidikan()
        self.PEKERJAAN: List[Pekerjaan] = self.dapodik.pekerjaan()
        self.PENGHASILAN: List[Penghasilan] = self.dapodik.penghasilan()
        self.start()

    def start(self) -> Dict[int, PesertaDidik]:
        raw_data_individu = get_data_excel(
            self.filepath,
            self.sheet,
            self.rows,
            DATA_INDIVIDU,
        )
        raw_data_ayah = get_data_excel(
            self.filepath,
            self.sheet,
            self.rows,
            DATA_AYAH,
        )
        raw_data_ibu = get_data_excel(
            self.filepath,
            self.sheet,
            self.rows,
            DATA_IBU,
        )
        result: Dict[int, PesertaDidik] = dict()
        for index, data_individu in raw_data_individu.items():
            data_ayah = raw_data_ayah[index]
            data_ibu = raw_data_ibu[index]
            data = self.get_default()
            data.update(self.transform_data_individu(**data_individu))
            data.update(self.transform_data_ayah(**data_ayah))
            data.update(self.transform_data_ibu(**data_ibu))
            result[index] = self.registrasi(data)
        return result

    def registrasi(self, data: dict) -> PesertaDidik:
        pdb = CreatePesertaDidik(
            kode_wilayah_str=data["kode_wilayah"],
            **data,
        )
        return pdb.save(self.dapodik)

    def transform_data_individu(
        self,
        nama: str,
        jenis_kelamin: str,
        agama_id: str,
        kode_wilayah: str,
        tempat_lahir: str,
        reg_akta_lahir: str,
        **kwargs: Any,
    ) -> dict:
        kwargs["nama"] = nama.upper()
        jenis_kelamin = jenis_kelamin.upper()
        assert jenis_kelamin in ("L", "P")
        kwargs["jenis_kelamin"] = jenis_kelamin
        kwargs["agama_id"] = self.parse_agama(agama_id)
        kwargs["tempat_lahir"] = tempat_lahir.upper()
        kwargs["kode_wilayah"] = self.find_kode_wilayah(kode_wilayah)
        if reg_akta_lahir:
            kwargs["reg_akta_lahir"]
        return kwargs

    def transform_data_ayah(
        self,
        tahun_lahir_ayah: str,
        jenjang_pendidikan_ayah: str,
        pekerjaan_id_ayah: str,
        penghasilan_id_ayah: str,
        **kwargs: Any,
    ) -> dict:
        if tahun_lahir_ayah.isdigit():
            kwargs["tahun_lahir_ayah"] = tahun_lahir_ayah
        else:
            kwargs["tahun_lahir_ayah"] = "19" + kwargs["nik_ayah"][10:12]
        kwargs["jenjang_pendidikan_ayah"] = self.parse_jenjang_pendidikan(
            jenjang_pendidikan_ayah
        )
        kwargs["pekerjaan_id_ayah"] = self.parse_pekerjaan(pekerjaan_id_ayah)
        kwargs["penghasilan_id_ayah"] = self.guest_penghasilan(
            penghasilan_id_ayah, kwargs["pekerjaan_id_ayah"]
        )
        return kwargs

    def transform_data_ibu(
        self,
        tahun_lahir_ibu: str,
        jenjang_pendidikan_ibu: str,
        pekerjaan_id_ibu: str,
        penghasilan_id_ibu: str,
        **kwargs: Any,
    ) -> dict:
        if tahun_lahir_ibu.isdigit():
            kwargs["tahun_lahir_ibu"] = tahun_lahir_ibu
        else:
            kwargs["tahun_lahir_ibu"] = "19" + kwargs["nik_ibu"][10:12]
        kwargs["jenjang_pendidikan_ibu"] = self.parse_jenjang_pendidikan(
            jenjang_pendidikan_ibu
        )
        kwargs["pekerjaan_id_ibu"] = self.parse_pekerjaan(pekerjaan_id_ibu)
        kwargs["penghasilan_id_ibu"] = self.guest_penghasilan(
            penghasilan_id_ibu, kwargs["pekerjaan_id_ibu"]
        )
        return kwargs

    @cachedmethod(attrgetter("penghasilan_cache"))
    def guest_penghasilan(self, val: str, pekerjaan: int) -> int:
        if pekerjaan in (90, 98, 1):
            # Tidak bekerja
            return 99
        if val and val.isdigit():
            digit_val = int(val)
            if digit_val <= 0:
                return 99
            for penghasilan in self.PENGHASILAN:
                if penghasilan.batas_atas < digit_val < penghasilan.batas_bawah:
                    return penghasilan.penghasilan_id
                elif (
                    penghasilan.batas_bawah == 0 and digit_val > penghasilan.batas_atas
                ):
                    return penghasilan.penghasilan_id
        elif val:
            for penghasilan in self.PENGHASILAN:
                if val in penghasilan.nama:
                    return penghasilan.penghasilan_id
        return 99

    @cachedmethod(attrgetter("agama_cache"))
    def parse_agama(self, keyword: str) -> int:
        for agama in self.AGAMA:
            if keyword in agama.nama:
                return agama.agama_id
        return 1

    @cachedmethod(attrgetter("kode_wilayah_cache"))
    def find_kode_wilayah(self, keyword: str) -> str:
        wilayah: List[Wilayah] = self.dapodik.kecamatan(keyword)
        return wilayah[0].kode_wilayah

    @cachedmethod(attrgetter("jenjang_pendidikan_cache"))
    def parse_jenjang_pendidikan(self, val: str) -> int:
        for jenjang_pendidikan in self.JENJANG_PENDIDIKAN:
            if val in jenjang_pendidikan.nama:
                return jenjang_pendidikan.jenjang_pendidikan_id
        return 0

    @cachedmethod(attrgetter("pekerjaan_cache"))
    def parse_pekerjaan(self, val: str) -> int:
        for pekerjaan in self.PEKERJAAN:
            if val in pekerjaan.nama:
                return pekerjaan.pekerjaan_id
        return 1

    def get_default(self) -> Dict[str, Any]:
        return {
            "nisn": self.nisn,
            "kebutuhan_khusus_id": self.kebutuhan_khusus_id,
            "lintang": self.lintang,
            "bujur": self.bujur,
            "jenis_tinggal_id": self.jenis_tinggal_id,
            "anak_keberapa": self.anak_keberapa,
            "alat_transportasi_id": self.alat_transportasi_id,
            "penerima_kps": self.penerima_kps,
            "penerima_kip": self.penerima_kip,
            "layak_pip": self.layak_pip,
            "id_layak_pip": self.id_layak_pip,
            "sekolah_id": self.sekolah.sekolah_id,
            "kewarganegaraan": self.kewarganegaraan,
            "no_kks": self.no_kks,
            "no_kps": self.no_kps,
            "no_kip": self.no_kip,
            "nm_kip": self.nm_kip,
            "kebutuhan_khusus_id_ayah": self.kebutuhan_khusus_id_ayah,
            "kebutuhan_khusus_id_ibu": self.kebutuhan_khusus_id_ibu,
            "nama_wali": self.nama_wali,
            "nik_wali": self.nik_wali,
            "tahun_lahir_wali": self.tahun_lahir_wali,
            "jenjang_pendidikan_wali": self.jenjang_pendidikan_wali,
            "pekerjaan_id_wali": self.pekerjaan_id_wali,
            "penghasilan_id_wali": self.penghasilan_id_wali,
            "nomor_telepon_rumah": self.nomor_telepon_rumah,
            "nomor_telepon_seluler": self.nomor_telepon_seluler,
            "email": self.email,
        }


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
