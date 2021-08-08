from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Any, Dict, List


def get_data_ws(ws: Worksheet, mapping: Dict[str, str], row: int) -> Dict[str, Any]:
    """get_data_ws get data from worksheet

    Args:
        ws (Worksheet): Openpyxl worksheet
        mapping (Dict[str, str]): Key and collumn combination
        row (int): Row number

    Returns:
        Dict[str, Any]: Data?
    """
    result: Dict[str, Any] = dict()
    for key, col in mapping.items():
        result = ws[f"{col}{row}"].value
    return result


def get_data_excel(
    filepath: str,
    sheet: str,
    rows: List[int],
    mapping: Dict[str, str],
) -> Dict[int, Dict[str, Any]]:
    """get_data_excel get data from excel file

    Args:
        filepath (str): File directory
        sheet (str): Worksheet name
        rows (List[int]): Number of row
        mapping (Dict[str, str]): Key and collumn combination

    Returns:
        Dict[int, Dict[str, Any]]: Data?
    """
    results: Dict[int, Dict[str, Any]] = dict()
    wb = load_workbook(filepath)
    ws = wb[sheet]
    for row in rows:
        results[row] = get_data_ws(ws, mapping, row)
    return results
