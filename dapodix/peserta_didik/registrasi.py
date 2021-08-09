from cachetools import cachedmethod
from operator import attrgetter
from typing import Any, Dict, List, Optional

from dapodik import Dapodik, __semester__
from dapodik.customrest import Wilayah
from dapodik.peserta_didik import (
    CreatePesertaDidik,
    PesertaDidik,
    PesertaDidikLongitudinal,
    RegistrasiPesertaDidik,
)
from dapodik.rest import (
    Agama,
    JenisCita,
    JenisHobby,
    JenisPendaftaran,
    JenjangPendidikan,
    Pekerjaan,
    Penghasilan,
)
from dapodik.sekolah import Sekolah

from dapodix.utils import get_data_excel

DATA_INDIVIDU = {
    "nisn": "B",
    "nama": "C",
    "jenis_kelamin": "D",
    "nik": "E",
    "no_kk": "F",
    "tempat_lahir": "G",
    "tanggal_lahir": "H",
    "reg_akta_lahir": "I",
    "agama_id": "J",
    "alamat_jalan": "K",
    "rt": "L",
    "rw": "M",
    "nama_dusun": "N",
    "kode_wilayah": "O",
    "desa_kelurahan": "P",
    "kode_pos": "Q",
    "anak_keberapa": "R",
    "nomor_telepon_seluler": "AE",
    "email": "AF",
}

DATA_REGISTRASI = {
    "nipd": "A",
    "jenis_pendaftaran_id": "AG",
    "tanggal_masuk_sekolah": "AH",
    "sekolah_asal": "AI",
    "id_hobby": "AJ",
    "id_cita": "AK",
    "a_pernah_paud": "AL",
    "a_pernah_tk": "AM",
}

DATA_LONGITUDINAL = {
    "tinggi_badan": "AN",
    "berat_badan": "AO",
    "lingkar_kepala": "AP",
    "jarak_rumah_ke_sekolah": "AQ",
    "menit_tempuh_ke_sekolah": "AR",
    "jumlah_saudara_kandung": "AS",
}

DATA_AYAH = {
    "nama_ayah": "S",
    "nik_ayah": "T",
    "tahun_lahir_ayah": "U",
    "jenjang_pendidikan_ayah": "V",
    "pekerjaan_id_ayah": "W",
    "penghasilan_id_ayah": "X",
}

DATA_IBU = {
    "nama_ibu_kandung": "Y",
    "nik_ibu": "Z",
    "tahun_lahir_ibu": "AA",
    "jenjang_pendidikan_ibu": "AB",
    "pekerjaan_id_ibu": "AC",
    "penghasilan_id_ibu": "AD",
}


class RegistrasiPesertaDidikCommand:
    JARAK_KE_MENIT = 5
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
        self.sekolah: Sekolah = self.dapodik.sekolah()
        # Individu
        self.agama_cache: Dict[str, int] = dict()
        self.kode_wilayah_cache: Dict[str, str] = dict()
        # Orang tua
        self.penghasilan_cache: Dict[tuple, int] = dict()
        self.jenjang_pendidikan_cache: Dict[str, int] = dict()
        self.pekerjaan_cache: Dict[str, int] = dict()
        # Registrasi
        self.cita_cache: Dict[str, int] = dict()
        self.hobby_cache: Dict[str, int] = dict()
        self.pendaftaran_cache: Dict[str, int] = dict()
        # INDIVIDU
        self.AGAMA: List[Agama] = self.dapodik.agama()
        # ORANG TUA
        self.JENJANG_PENDIDIKAN: List[
            JenjangPendidikan
        ] = self.dapodik.jenjang_pendidikan()
        self.PEKERJAAN: List[Pekerjaan] = self.dapodik.pekerjaan()
        self.PENGHASILAN: List[Penghasilan] = self.dapodik.penghasilan()
        # REGISTRASI
        self.CITA: List[JenisCita] = self.dapodik.jenis_cita()
        self.HOBBY: List[JenisHobby] = self.dapodik.jenis_hobby()
        self.PENDAFTARAN: List[JenisPendaftaran] = self.dapodik.jenis_pendaftaran()

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
        peserta_didik_baru: Dict[int, PesertaDidik] = dict()
        for index, data_individu in raw_data_individu.items():
            data_ayah = raw_data_ayah[index]
            data_ibu = raw_data_ibu[index]
            data = self.get_default()
            data.update(self.transform_data_individu(**data_individu))
            data.update(self.transform_data_ayah(**data_ayah))
            data.update(self.transform_data_ibu(**data_ibu))
            peserta_didik = self.tambah_peserta_didik(data)
            peserta_didik._dapodik = self.dapodik
            peserta_didik_baru[index] = peserta_didik
        raw_data_registrasi = get_data_excel(
            self.filepath,
            self.sheet,
            self.rows,
            DATA_REGISTRASI,
        )
        for index, data_registrasi in raw_data_registrasi.items():
            data = self.get_default_registrasi()
            data.update(self.transform_data_registrasi(**data_registrasi))
            peserta_didik = peserta_didik_baru[index]
            peserta_didik_baru[index] = self.registrasi_peserta_didik(
                data, peserta_didik
            )
        raw_data_longitudinal = get_data_excel(
            self.filepath,
            self.sheet,
            self.rows,
            DATA_LONGITUDINAL,
        )
        for index, data_longitudinal in raw_data_longitudinal.items():
            data = self.get_default_longitudinal()
            data.update(self.transform_data_longitudinal(**data_longitudinal))
            peserta_didik = peserta_didik_baru[index]
            peserta_didik_baru[index] = self.longitudinal_peserta_didik(
                data, peserta_didik
            )
        return peserta_didik_baru

    def tambah_peserta_didik(self, data: dict) -> PesertaDidik:
        pdb = CreatePesertaDidik(
            kode_wilayah_str=data["kode_wilayah"],
            **data,
        )
        return pdb.save(self.dapodik)

    def longitudinal_peserta_didik(
        self, data: dict, peserta_didik: PesertaDidik
    ) -> PesertaDidik:
        longitudinal = PesertaDidikLongitudinal.Create(**data)
        peserta_didik.create_longitudinal(longitudinal)
        return peserta_didik

    def registrasi_peserta_didik(
        self, data: dict, peserta_didik: PesertaDidik
    ) -> PesertaDidik:
        reg_pd = RegistrasiPesertaDidik(
            peserta_didik_id=peserta_didik.peserta_didik_id,
            sekolah_id=peserta_didik.sekolah_id,
            **data,
        )
        reg_pd.sekolah_id = self.sekolah.sekolah_id
        # peserta_didik._dapodik = self.dapodik
        peserta_didik.register(reg_pd)
        return peserta_didik

    def transform_data_individu(
        self,
        nisn: str,
        nama: str,
        jenis_kelamin: str,
        agama_id: str,
        kode_wilayah: str,
        tempat_lahir: str,
        reg_akta_lahir: str,
        nomor_telepon_seluler: str,
        email: str,
        **kwargs: Any,
    ) -> dict:
        kwargs["nisn"] = nisn if nisn else ""
        kwargs["nama"] = nama.upper()
        jenis_kelamin = jenis_kelamin.upper()
        assert jenis_kelamin in ("L", "P")
        kwargs["jenis_kelamin"] = jenis_kelamin
        kwargs["agama_id"] = self.parse_agama(agama_id)
        kwargs["tempat_lahir"] = tempat_lahir.upper()
        kwargs["kode_wilayah"] = self.find_kode_wilayah(kode_wilayah)
        kwargs["reg_akta_lahir"] = reg_akta_lahir if reg_akta_lahir else ""
        kwargs["nomor_telepon_seluler"] = (
            nomor_telepon_seluler if nomor_telepon_seluler else ""
        )
        kwargs["email"] = email if email else ""
        return kwargs

    def transform_data_registrasi(
        self,
        jenis_pendaftaran_id: str,
        sekolah_asal: str,
        nipd: str,
        id_hobby: str,
        id_cita: str,
        a_pernah_paud: str,
        a_pernah_tk: str,
        **kwargs: Any,
    ) -> dict:
        kwargs["jenis_pendaftaran_id"] = self.parse_pendaftaran(jenis_pendaftaran_id)
        kwargs["id_hobby"] = self.parse_hobby(id_hobby)
        kwargs["id_cita"] = self.parse_cita(id_cita)
        kwargs["sekolah_asal"] = sekolah_asal if sekolah_asal else ""
        kwargs["nipd"] = nipd if nipd else ""
        kwargs["a_pernah_paud"] = 1 if a_pernah_paud == "YA" else 0
        kwargs["a_pernah_tk"] = 1 if a_pernah_tk == "YA" else 0
        return kwargs

    def transform_data_longitudinal(
        self,
        jarak_rumah_ke_sekolah: int,
        menit_tempuh_ke_sekolah: int,
        **kwargs: Any,
    ) -> dict:
        if jarak_rumah_ke_sekolah <= 1:
            kwargs["jarak_rumah_ke_sekolah"] = 1
            kwargs["jarak_rumah_ke_sekolah_km"] = 0
        else:
            kwargs["jarak_rumah_ke_sekolah"] = 2
            kwargs["jarak_rumah_ke_sekolah_km"] = jarak_rumah_ke_sekolah
        if not isinstance(menit_tempuh_ke_sekolah, int):
            menit_tempuh_ke_sekolah = jarak_rumah_ke_sekolah * self.JARAK_KE_MENIT
        kwargs["waktu_tempuh_ke_sekolah"] = menit_tempuh_ke_sekolah // 60
        kwargs["menit_tempuh_ke_sekolah"] = menit_tempuh_ke_sekolah % 60
        return kwargs

    def transform_data_ayah(
        self,
        tahun_lahir_ayah: str,
        jenjang_pendidikan_ayah: str,
        pekerjaan_id_ayah: str,
        penghasilan_id_ayah: str,
        **kwargs: Any,
    ) -> dict:
        if isinstance(tahun_lahir_ayah, int):
            kwargs["tahun_lahir_ayah"] = str(tahun_lahir_ayah)
        elif isinstance(tahun_lahir_ayah, str) and tahun_lahir_ayah.isdigit():
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
        if isinstance(tahun_lahir_ibu, int):
            kwargs["tahun_lahir_ibu"] = str(tahun_lahir_ibu)
        elif isinstance(tahun_lahir_ibu, str) and tahun_lahir_ibu.isdigit():
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

    @cachedmethod(attrgetter("cita_cache"))
    def parse_cita(self, val: str) -> int:
        for cita in self.CITA:
            if val in cita.nm_cita:
                return cita.id_cita
        return 8

    @cachedmethod(attrgetter("hobby_cache"))
    def parse_hobby(self, val: str) -> int:
        for hobby in self.HOBBY:
            if val in hobby.nm_hobby:
                return hobby.id_hobby
        return 6

    @cachedmethod(attrgetter("pendaftaran_cache"))
    def parse_pendaftaran(self, val: str) -> int:
        for pendaftaran in self.PENDAFTARAN:
            if val in pendaftaran.nama:
                return pendaftaran.jenis_pendaftaran_id
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

    def get_default_registrasi(self) -> Dict[str, Any]:
        return {
            "registrasi_id": "Admin.model.RegistrasiPesertaDidik-3",
            # "peserta_didik_id":"",
            "jurusan_sp_id": "",
            # "sekolah_id":"",
            # "jenis_pendaftaran_id":1,
            # "tanggal_masuk_sekolah": "2021-07-05",
            "jenis_keluar_id": "",
            "tanggal_keluar": None,
            "keterangan": "",
            "no_skhun": "",
            # "nipd": "",
            # "id_hobby":6,
            # "id_cita":8,
            "no_seri_ijazah": "",
            "no_peserta_ujian": "",
            # "sekolah_asal": "",
            "a_pernah_paud": 0,
            "a_pernah_tk": 0,
            "jurusan_sp_id_str": "",
            "peserta_didik_id_str": "",
            "sekolah_id_str": "",
            "jenis_pendaftaran_id_str": "",
            "id_hobby_str": "",
            "id_cita_str": "",
            "jenis_keluar_id_str": "",
        }

    def get_default_longitudinal(self) -> Dict[str, Any]:
        return {
            "peserta_didik_longitudinal_id": "Admin.model.PesertaDidikLongitudinal-40",
            "semester_id": __semester__,
            # "peserta_didik_id": "",
            # "tinggi_badan": 75,
            # "berat_badan": 11,
            "jarak_rumah_ke_sekolah_km": 0,
            "jarak_rumah_ke_sekolah": 1,
            "waktu_tempuh_ke_sekolah": 0,
            # "menit_tempuh_ke_sekolah": 5,
            # "jumlah_saudara_kandung": 4,
            "vld_count": 0,
            "peserta_didik_longitudinal_id_str": "",
            "peserta_didik_id_str": "",
            "semester_id_str": "",
            # "lingkar_kepala": 20,
        }
