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

ALL_DATA_INDIVIDU = dict(DATA_INDIVIDU)
ALL_DATA_INDIVIDU.update(DATA_AYAH)
ALL_DATA_INDIVIDU.update(DATA_IBU)
ALL_DATA_INDIVIDU.update(DATA_REGISTRASI)
