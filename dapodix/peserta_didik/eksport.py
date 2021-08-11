from openpyxl.worksheet.worksheet import Worksheet
from typing import Any, Dict, List

from dapodik import Dapodik, __semester__
from dapodik.peserta_didik import PesertaDidik

from . import ALL_DATA_INDIVIDU, DATA_LONGITUDINAL
from dapodix.utils import get_workbook, snake_to_title


class EksporPesertaDidikCommand:
    MAPPING_INDIVIDU: Dict[str, str] = ALL_DATA_INDIVIDU
    MAPPING_LONGITUDINAL: Dict[str, str] = DATA_LONGITUDINAL

    def __init__(
        self,
        dapodik: Dapodik,
        filepath: str,
        sheet: str = "Peserta Didik",
        header: bool = True,
    ):
        self.dapodik = dapodik
        self.offset = 2 if header else 1
        self.sekolah = self.dapodik.sekolah()
        self.peserta_didik = self.get_peserta_didik()
        self.WORKBOOK = get_workbook(filepath)
        self.WORKSHEET: Worksheet = self.WORKBOOK.active
        self.WORKSHEET.title = sheet
        if header:
            self.add_header()
        for index, peserta_didik in enumerate(self.peserta_didik):
            self.peserta_didik_to_row(peserta_didik, index + self.offset)
        if not filepath.endswith(".xlsx"):
            filepath += ".xlsx"
        self.WORKBOOK.save(filename=filepath)

    def get_peserta_didik(self) -> List[PesertaDidik]:
        return self.dapodik.peserta_didik(sekolah_id=self.sekolah.sekolah_id)

    def add_header(self, row: int = 1):
        for name, col in self.MAPPING_INDIVIDU.items():
            self.WORKSHEET[f"{col}{row}"] = snake_to_title(name)
        for name, col in self.MAPPING_LONGITUDINAL.items():
            self.WORKSHEET[f"{col}{row}"] = snake_to_title(name)

    def peserta_didik_to_row(self, pd: PesertaDidik, row: int):
        for name, col in self.MAPPING_INDIVIDU.items():
            value = getattr(pd, name)
            if value is None:
                self.WORKSHEET[f"{col}{row}"] = value
        for name, col in self.MAPPING_LONGITUDINAL.items():
            value = getattr(pd, name)
            if value is None:
                self.WORKSHEET[f"{col}{row}"] = value
