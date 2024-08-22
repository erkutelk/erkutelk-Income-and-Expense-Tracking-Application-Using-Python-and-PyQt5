from main import App
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from app_page.home import HomePage
from sesion import session_manager
from datetime import datetime
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class gelirlerClass(QtWidgets.QMainWindow):
    def __init__(self,ui,name):
        super(gelirlerClass,self).__init__()
        self.ui = ui
        self.name=name
        self.database=Database()
        self.tarih=datetime.today()
        self.WidgetTableVi()
        print(self.name,'Sayfasına geçildi')
       
    def kaydet(self):
            self.tb_baslik=self.ui.tb_baslik.text()
            self.tb_soyisim=self.ui.tb_soyisim.text()
            self.tb_tutar=self.ui.tb_tutar.text()
            self.tb_aciklama=self.ui.tb_aciklama.text()
            self.database.ekle('gelirler', name=self.tb_baslik, surnama=self.tb_soyisim, tutar=self.tb_tutar,tarih=self.tarih,aciklama=self.tb_aciklama)
            print(f'{self.tb_baslik} kullanıcısı eklendi')
            print('Ekleme İşlemi yapıldı...')

    def WidgetTableVi(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ID', 'İsim', 'Soyisim', 'Tutar', 'Tarih','Açıklama'])
        table = self.database.kullanicilarTable('SELECT * FROM gelirler')
        self.model.setRowCount(len(table))
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))

        self.ui.tableView_4.setModel(self.model)