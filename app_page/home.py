from main import App
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date, timedelta
from sesion import session_manager

class HomePage(QtWidgets.QMainWindow):
    def __init__(self, ui, name):
        super(HomePage, self).__init__()
        self.date = date.today()
        self.ui = ui
        self.database = Database()
        self.name = name
        self.limit()
        self.load_data()
        self.gelirler_toplam()
        self.kullanicinin_izin_sayisi()
        self.WidgetTableVi()

    def load_data(self):
        today = self.date
        last_week = today - timedelta(weeks=1)
        
        queries = [
            (f"SELECT SUM(COALESCE(borclartablosu.borc, 0)) AS DailyTotal "
            f"FROM borclartablosu WHERE CAST(borc_alinan_tarih AS DATE) = '{today}'", self.ui.lb_gunlukGider),

            (f"SELECT SUM(COALESCE(borclartablosu.borc, 0)) AS WeeklyTotal "
            f"FROM borclartablosu WHERE borc_alinan_tarih >= '{last_week}'", self.ui.lb_haftalkGider),

            ('SELECT COUNT(kullanicilar.ID) FROM kullanicilar', self.ui.lb_personelNumber)
        ]
        
        for query, label in queries:
            self.update_label(query, label)


    def limit(self):
        for a in self.database.table('SELECT * FROM limitPage where ID=1'):
            self.ui.label_31.setText(f'| {int(a[1])}')
            self.ui.label_32.setText(f'| {int(a[2])}')

    def gelirler_toplam(self):
        year_month = self.date.strftime('%Y-%m')# Bu tarih formatını istediğimiz biçime çevirmek için kullanılır.
        result = self.database.table(f"SELECT SUM(gelirler.tutar) FROM gelirler WHERE CONVERT(VARCHAR(7), gelirler.tarih, 120) = '{year_month}'")
        
        if result and result[0][0] is not None:
            self.ui.lb_gunlukGider_2.setText(f'{int(result[0][0])}')
        else:
            self.ui.lb_gunlukGider_2.setText('0')


    def kullanicinin_izin_sayisi(self):
        kullaniciID=session_manager.user_id
        result = self.database.table(f"SELECT sum(gun_sayisi) FROM izin where izin.KullaniciID={kullaniciID}")
        self.ui.lb_haftalkGider_2.setText(str(result[0][0]))



    def update_label(self, query, label):
        result = self.database.table(sorgu=query)
        label.setText(str(result[0][0]).split('.')[0])

    def WidgetTableVi(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ID', 'İsim', 'Soyisim','Hatırlatılacak Tarih','Açıklama'])
        table = self.database.kullanicilarTable('SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim,hatirlatma.hatirlatilack_tarih,borclartablosu.aciklama FROM hatirlatma inner join borclartablosu on hatirlatma.ID=borclartablosu.ID inner join kullanicilar on borclartablosu.kullaniciID=kullanicilar.ID')
        self.model.setRowCount(len(table))
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))

        self.ui.tableView_6.setModel(self.model)