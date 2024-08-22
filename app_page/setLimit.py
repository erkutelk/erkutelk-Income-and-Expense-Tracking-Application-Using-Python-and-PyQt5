from main import App
from PyQt5.QtWidgets import QTableView, QDialog
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

class limit_class(QtWidgets.QMainWindow):
    def __init__(self, ui, name):
        super(limit_class, self).__init__()
        self.ui = ui
        self.database = Database()
        self.name = name
        self.textYazdir()
        
    def update(self):
        haftalikGider=self.ui.tb_haftalikGider.text()
        aylikGider=self.ui.tb_gunlukGider.text()
        self.database.guncelleme(query='limitPage SET haftalik_gider = ?, aylik_gider=? WHERE ID = 1',haftalikGider=haftalikGider,aylikGider=aylikGider)
        print('Güncelleme işlemi yapıldı...')


    def textYazdir(self):
        try:
            for a in self.database.kullanicilarTable('SELECT * FROM limitPage'):
                hatfalikGiderValue=str(a[1])
                aylikGiderValue=str(a[2])
            self.ui.tb_haftalikGider.setText(hatfalikGiderValue)
            self.ui.tb_gunlukGider.setText(aylikGiderValue)
        except: 
            print('Ekrana yazdırma işlemi tamamlandı...')
        


    
