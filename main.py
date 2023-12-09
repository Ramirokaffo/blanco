

# from Service.ExcelService import ExportData

from Service.ServerService import ServerService
from UI.App.App import App

# ExportData.import_product(r"C:\Users\HP\Desktop\Liste produit new.xlsx")

# os.startfile()

my_app = App()

if __name__ == '__main__':
    my_app.mainloop()
    ServerService.stop_server()
