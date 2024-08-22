from main import App
from PyQt5.QtWidgets import QTableView, QDialog
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime
from database import Database
class kayitClass(QtWidgets.QMainWindow):
    def __init__(self,ui,name):
        super(kayitClass,self).__init__()
        self.ui = ui
        self.name=name
        self.database=Database()
        print(name,' Sayfasına geçildi...')
        self.ui.cb_kullanici_kayit.currentIndexChanged.connect(self.textTutarGosterme)
        self.cb_kullaniciSecme()
        

    def cb_kullaniciSecme(self):
            self.ui.cb_kullanici.clear()
            for a in self.database.table('SELECT * FROM kullanicilar'):
                isim = str(a[1])
                soyisim = str(a[2])
                value = f"{isim} {soyisim}".upper()  
                self.ui.cb_kullanici_kayit.addItem(value,str(a[0])) 
                self.textTutarGosterme()

    def textTutarGosterme(self):
        kullanici = self.ui.cb_kullanici_kayit.currentData()
        if kullanici:  # Eğer Değer Var ise 
            result = self.database.table(f'SELECT * FROM pers_login WHERE pers_login.kullaniciID={kullanici}')
            if result:
                self.ui.lineEdit_3.setText(str(result[0][2]).strip())
            else:
                self.ui.lineEdit_3.clear()
    

    def pepInsert(self):
        kullaniciID = self.ui.cb_kullanici_kayit.currentData()
        sifre = self.ui.lineEdit_3.text()
        kullaniciAdi = self.ui.lineEdit_4.text()
        # self.database.ekle('pers_login',kullaniciID=kullaniciID,mail=kullaniciAdi, sifre=sifre)
        self.database.guncelleme(query='pers_login SET mail = ?, sifre=? WHERE kullaniciID = ?',mail=kullaniciAdi,sifre=sifre,kullaniciID=kullaniciID)
        print('Güncelleme işlemi yapıldı...')
