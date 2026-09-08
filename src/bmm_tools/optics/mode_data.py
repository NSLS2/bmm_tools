'''Import the photon delivery system lookup table from a version
controlled Excel spreadsheet.

'''


import os
from openpyxl import load_workbook

MODEDATA = None
def read_mode_data():
     '''Read the lookup table Modes.xlsx and return position and encoder
     readings as a dict.
     '''
     wb = load_workbook(os.path.join(os.path.dirname(__file__), 'Modes.xlsx'), read_only=True);
     ws = wb['Modes A-F']
     bl = dict()
     header = 1
     for row in ws.rows:
         axis = dict()
         if str(row[0].value) == 'Instrument':
             header = 0
             continue
         if header == 1: continue
         alias           = row[2].value
         if 'fe_slits' in alias: continue
         axis['PV']      = row[1].value
         axis['desc']    = row[3].value
         axis['A']       = row[4].value
         axis['A_REP']   = row[5].value
         axis['B']       = row[6].value
         axis['B_REP']   = row[7].value
         axis['C']       = row[8].value
         axis['C_REP']   = row[9].value
         axis['D']       = row[10].value
         axis['D_REP']   = row[11].value
         axis['E']       = row[12].value
         axis['E_REP']   = row[13].value
         axis['F']       = row[14].value
         axis['F_REP']   = row[15].value
         axis['XRD']     = row[19].value
         axis['XRD_REP'] = row[20].value
         bl[alias] = axis
     del bl['xafs_ydo']         # clean up unneeded entry (Summer 2026, xafs_ydi and xafs_ydo are coupled)
     return bl

MODEDATA = read_mode_data();
