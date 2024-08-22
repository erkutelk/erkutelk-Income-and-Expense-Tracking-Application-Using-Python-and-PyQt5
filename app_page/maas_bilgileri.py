from main import App
from PyQt5.QtWidgets import QTableView, QDialog
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

class salary_information_class(QtWidgets.QMainWindow):
    def __init__(self, ui, name):
        super(salary_information_class, self).__init__()
        self.ui = ui
        self.database = Database()
        print(name, 'Sayfasına geçildi...')
        self.cb_kullaniciSecme()
        self.radioButtonSecilen()
        self.ui.cb_staff.currentIndexChanged.connect(self.textTutarGosterme)  
        # Sürekli çalışacağı için kod satırının burada olması gerekli
        self.ui.btn_maasBilgileriSearch.clicked.connect(self.yukle)


    def yukle(self):
        deger = self.ui.lineEdit_2.text().strip()
        if deger == '*':
            self.WidgetTableVik()
        elif deger:
            self.WidgetTableVik(f"""
                SELECT maasBilgileri.ID, kullanicilar.isim, kullanicilar.soyisim, Bolum.bolum_name, 
                kullanicilar.tarih, kullanicilar.telefon, maasBilgileri.maas 
                FROM maasBilgileri 
                INNER JOIN kullanicilar on kullanicilar.ID=maasBilgileri.kullaniciID 
                INNER JOIN Bolum on kullanicilar.bolumID=Bolum.ID 
                WHERE kullanicilar.isim LIKE '{deger}%'""")



    def radioButtonSecilen(self):
            self.ui.radioButton_6.clicked.connect(self.radioButtonChanged)
            self.ui.radioButton_7.clicked.connect(self.radioButtonChanged)
            self.ui.radioButton_8.clicked.connect(self.radioButtonChanged)
    
    def radioButtonChanged(self):
        radioButton = self.radiobutonZam()
        if radioButton == 1:
            #Fonksiyonu burada tanımladığımız için bir daha çağırmaya gerek yok
            self.apply_salary_increase(15,self.ui.radioButton_6.isChecked())
        elif radioButton == 2:
            self.apply_salary_increase(25,self.ui.radioButton_7.isChecked())
        elif radioButton == 3:
            self.apply_salary_increase(35,self.ui.radioButton_8.isChecked())

    def apply_salary_increase(self, yüzdelikdeger,radioButonSelect):
        if radioButonSelect:
            try:
                tutar = self.ui.cb_salery.text().strip()
                if tutar:
                    value = (float(tutar) * yüzdelikdeger)/100+float(tutar)
                    self.ui.cb_salery.setText(str(value))
                    print('Yüzdelik dilim eklendi...')
            except Exception as e:
                print('Radio buttonlarda bir hata meydana geldi: ', e)

    def cb_kullaniciSecme(self):
        self.ui.cb_staff.clear()
        for a in self.database.table('SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim FROM kullanicilar'):
            isim = str(a[1])
            soyisim = str(a[2])
            value = f"{isim} {soyisim}".upper()
            self.ui.cb_staff.addItem(value, str(a[0]))
        
        self.textTutarGosterme()

    def pepInsert(self):
        kullanici = self.ui.cb_staff.currentIndex() + 1
        tutar = self.ui.cb_salery.text().strip()
        self.database.ekle('maasBilgileri', kullaniciID=kullanici, maas=tutar)
        print(f'{kullanici} kullanıcısı eklendi')
        self.WidgetTableVik()

    def textTutarGosterme(self):
        kullanici = self.ui.cb_staff.currentData()
        if kullanici:  # cb içerisindeki veriyi alıp sql veritabanından var mı kontrol etmak için kullanılır. 
            result = self.database.table(f'SELECT * FROM maasBilgileri WHERE maasBilgileri.kullaniciID={kullanici}')
            if result:
                self.ui.cb_salery.setText(str(result[0][2]).strip())
            else:
                self.ui.cb_salery.clear()

    def kontrol(self):
        kullanici = self.ui.cb_staff.currentData()
        existing_record = self.database.table(f'SELECT * FROM maasBilgileri WHERE kullaniciID={kullanici}')
        if existing_record:
            print('Kullanıcı mevcut, güncelleme işlemi yapılıyor...')
            self.Guncelle()
        else:
            print('Kullanıcı mevcut değil, ekleme işlemi yapılıyor...')
            self.pepInsert()  



    def Guncelle(self):
        tutar = self.ui.cb_salery.text().strip()
        kullanici = self.ui.cb_staff.currentData()
        self.database.guncelleme(query='MaasBilgileri SET maas = ? WHERE kullaniciID = ?',tutar=tutar, kullaniciID=kullanici)
        print('Güncelleme işlemi yapıldı...')
        self.WidgetTableVik()

    def radiobutonZam(self):
        if self.ui.radioButton_6.isChecked():
            return 1
        elif self.ui.radioButton_7.isChecked():
            return 2
        elif self.ui.radioButton_8.isChecked():
            return 3

    def WidgetTableVik(self,value="""
                       SELECT maasBilgileri.ID, kullanicilar.isim, kullanicilar.soyisim, Bolum.bolum_name, kullanicilar.tarih, kullanicilar.telefon, maasBilgileri.maas 
                       FROM maasBilgileri 
                       INNER JOIN kullanicilar on kullanicilar.ID=maasBilgileri.kullaniciID 
                       INNER JOIN Bolum on kullanicilar.bolumID=Bolum.ID"""):
        
        header = ['ID', 'İsim', 'Soyisim', 'bolum_name', 'tarih', 'telefon', 'Maaş']
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(header)
        table = self.database.kullanicilarTable(value)
        self.model.setRowCount(len(table))
        
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))
        
        self.ui.tableView_3.setModel(self.model)
