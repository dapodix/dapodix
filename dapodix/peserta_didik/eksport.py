from openpyxl.worksheet.worksheet import Worksheet
from typing import Any, Dict, List, Optional

from dapodik import Dapodik, __semester__
from dapodik.peserta_didik import PesertaDidik, PesertaDidikLongitudinal

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
        skip_longitudinal: bool = False,
    ):
        self.dapodik = dapodik
        self.offset = 2 if header else 1
        self.skip_longitudinal = skip_longitudinal
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
            if not hasattr(pd, name):
                continue
            value = getattr(pd, name)
            if value is None:
                continue
            self.WORKSHEET[f"{col}{row}"] = value
        if not self.skip_longitudinal:
            for name, col in self.MAPPING_LONGITUDINAL.items():
                longitudinal: Optional[PesertaDidikLongitudinal] = None
                longitudinals = self.dapodik.peserta_didik_longitudinal(
                    peserta_didik_id=pd.peserta_didik_id,
                )
                for ltd in longitudinals:
                    if ltd.semester_id == __semester__:
                        longitudinal = ltd
                        break
                if not hasattr(longitudinal, name):
                    continue
                value = getattr(longitudinal, name)
                if value is None:
                    continue
                self.WORKSHEET[f"{col}{row}"] = value
