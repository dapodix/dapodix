import click
from typing import List

from dapodik import Dapodik
from dapodik.sekolah import Sekolah
from dapodik.peserta_didik import PesertaDidik, RegistrasiPesertaDidik

from dapodix.utils import parse_date


class TanggalMasukCommand:
    def __init__(self, dapodik: Dapodik, tanggal: str):
        self.dapodik = dapodik
        self.tanggal = parse_date(tanggal)
        self.sekolah = self.dapodik.sekolah()
        self.peserta_didik: List[PesertaDidik] = self.dapodik.peserta_didik(
            sekolah_id=self.sekolah.sekolah_id
        )

    def update_registrasi(self):
        for pd in self.peserta_didik:
            if not pd.tanggal_masuk_sekolah:
                click.echo(f"Lewati {pd} tidak memiliki tanggal masuk sekolah")
                continue
