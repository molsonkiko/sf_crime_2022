from openpyxl.worksheet.table import Table, TableStyleInfo
import openpyxl

def add_table(fname, sheet_name, tbl_name, rng):
    wb = openpyxl.open(fname)
    style = TableStyleInfo(name="TableStyleMedium9", 
                           showFirstColumn=False,
                           showLastColumn=False, 
                           showRowStripes=True, 
                           showColumnStripes=False)
    tbl = Table(displayName = tbl_name, ref = rng)
    tbl.tableStyleInfo = style
    wb[sheet_name].add_table(tbl)
    wb.save(fname)
    wb.close()