# import os
import os.path
import win32com.client

if os.path.exists("excelsheet.xlsm"):
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Workbooks.Open(os.path.abspath("excelsheet.xlsm"), ReadOnly=1)
    xl.Application.Run("excelsheet.xlsm!modulename.macroname")
    """
    xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
    """
    xl.Application.Quit()  # Comment this out if your excel script closes

    del xl


# Import the following library to make use of the DispatchEx to run the macro
import win32com.client as wincl
import os.path

def runMacro():

    if os.path.exists("C:\\Users\\Dev\\Desktop\\Development\\completed_apps\\My_Macr_Generates_Data.xlsm"):

        # DispatchEx is required in the newest versions of Python.
        excel_macro = wincl.DispatchEx("Excel.application")
        excel_path = os.path.expanduser(
            "C:\\Users\\Dev\\Desktop\\Development\\completed_apps\\My_Macr_Generates_Data.xlsm")
        workbook = excel_macro.Workbooks.Open(Filename=excel_path, ReadOnly=1)
        excel_macro.Application.Run("ThisWorkbook.Template2G")
        # Save the results in case you have generated data
        workbook.Save()
        excel_macro.Application.Quit()
        del excel_macro
