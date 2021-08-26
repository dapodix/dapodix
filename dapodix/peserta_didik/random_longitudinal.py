import click
from random import randint
from typing import Callable, List

from dapodik import Dapodik, __semester__
from dapodik.peserta_didik import PesertaDidik, PesertaDidikLongitudinal
from dapodik.sekolah import Sekolah


class RandomLongitudinal:
    def __init__(
        self,
        dapodik: Dapodik,
        tinggi: Callable[[], int] = lambda: randint(125, 160),
        berat: Callable[[], int] = lambda: randint(20, 75),
        lingkar_kepala: Callable[[], int] = lambda: randint(20, 40),
        jarak_rumah: Callable[[], int] = lambda: randint(0, 20),
        jarak_waktu: int = 5,
    ):
        self.dapodik = dapodik
        self._tinggi = tinggi
        self._berat = berat
        self._lingkar_kepala = lingkar_kepala
        self._jarak_rumah = jarak_rumah
        self.jarak_waktu = jarak_waktu
        self.sekolah: Sekolah = self.dapodik.sekolah()
        if self.sekolah:
            click.echo(f"Berhasil login @{self.sekolah.nama}")
        self.PESERTA_DIDIK: List[PesertaDidik] = self.dapodik.peserta_didik(
            self.sekolah.sekolah_id,
            limit=1000000,
        )
        click.echo(f"Berhasil memuat peserta didik sebanyak {len(self.PESERTA_DIDIK)}")
        try:
            self.start()
        except Exception as e:
            click.echo(f"Terjadi error : {e}")
            raise e

    def tinggi(self) -> int:
        return self._tinggi()

    def berat(self) -> int:
        return self._berat()

    def lingkar_kepala(self) -> int:
        return self._lingkar_kepala()

    def jarak_rumah(self) -> int:
        return self._jarak_rumah()

    def get_new_longitudinal(
        self, peserta_didik: PesertaDidik
    ) -> PesertaDidikLongitudinal.Create:
        jarak_rumah = self.jarak_rumah()
        if jarak_rumah > 0:
            jarak_rumah_ke_sekolah_km = 0
            jarak_rumah_ke_sekolah = 2
        else:
            jarak_rumah_ke_sekolah_km = jarak_rumah
            jarak_rumah_ke_sekolah = 1
        jarak_waktu = jarak_rumah * self.jarak_waktu
        if peserta_didik.anak_keberapa > 1:
            saudara = peserta_didik.anak_keberapa - 1
        else:
            saudara = 0
        return PesertaDidikLongitudinal.Create(
            peserta_didik_id=peserta_didik.peserta_didik_id,
            tinggi_badan=self.tinggi(),
            berat_badan=self.berat(),
            jarak_rumah_ke_sekolah_km=jarak_rumah_ke_sekolah_km,
            jarak_rumah_ke_sekolah=jarak_rumah_ke_sekolah,
            waktu_tempuh_ke_sekolah=jarak_waktu // 60,
            menit_tempuh_ke_sekolah=jarak_waktu % 60,
            jumlah_saudara_kandung=saudara,
            lingkar_kepala=self.lingkar_kepala(),
        )

    def start(self):
        total = 0
        for peserta_didik in self.PESERTA_DIDIK:
            old_longitudinal: List[
                PesertaDidikLongitudinal
            ] = self.dapodik.peserta_didik_longitudinal(peserta_didik.peserta_didik_id)
            if self.check_longitudinals(old_longitudinal):
                click.echo(f"Lewati {peserta_didik} longitudinal sudah ada")
                continue
            longitudinal = self.get_new_longitudinal(peserta_didik)
            new_longitudinal = peserta_didik.create_longitudinal(longitudinal)
            click.echo(f"Longitudinal {peserta_didik} : {new_longitudinal}")
            total += 1
        if total > 0:
            click.echo(
                f"Berhasil membuat data longitudinal sebanyak {total} peserta didik"
            )
        else:
            click.echo(f"Semua peserta didik sudah memiliki data longitudinal")

    def check_longitudinals(
        self, longitudinals: List[PesertaDidikLongitudinal]
    ) -> bool:
        for longitudinal in longitudinals:
            if longitudinal.semester_id == __semester__:
                return True
        return False
