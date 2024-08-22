from main import App
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from database import Database
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class yakitGiderleri(QtWidgets.QMainWindow):#Home page sınıfını çağırırken üst sınıfı olan Qtwidgets sınıfının __init__ değerini çağırmamaız gerekiyor, o değeri çalıştırmadan diğer derğerli çalıştırmaya kalsakrsak kodda hata alırız
    def __init__(self, ui,name):
        super(yakitGiderleri, self).__init__() 
        self.ui = ui
        self.database = Database()
        self.date=date.today()
        print(name,'Sayfasına geçildi...')
        self.ui.tabWidget_3.currentChanged.connect(self.tabWidgetSelect)
        
    def tabWidgetSelect(self,index):
        if index==2:
            self.yakitGiderEkle()
        elif index==1:
            self.WidgetTableVi()
    
    def yakitGiderEkle(self):
        self.combobax('arac_plaka',self.ui.cb_aracPlaka)
        self.combobax('kullanicilar',self.ui.cb_yakitKullanici)

    def combobax(self,tablo,cb):
        cb.clear()#combobaxın sürekli değer eklemesini engelliyor
        for a in self.database.table(f'SELECT * FROM {tablo}'):
            cb.addItem(str(a[1]),str(a[0]))

    def pepInsert(self):
            kullaniciID = self.ui.cb_yakitKullanici.currentIndex() + 1
            kullaniciName = self.ui.cb_yakitKullanici.currentText()
            yakit = self.ui.tb_yakitTutar.toPlainText()
            plaka = self.ui.cb_aracPlaka.currentIndex()+1
            self.database.ekle('yakit',kullaniciID=kullaniciID, aracID=plaka,tutar=yakit,tarih=self.date)
            print(f'{kullaniciName} kullanıcısı eklendi')
            self.ui.lb_bilgi.setText(f'{kullaniciName} personeline {self.ui.cb_aracPlaka.currentText()} yakıt bilgisi girildi...')
            print('İçerisinde harf var veya isim çok uzun')
            self.WidgetTableVi()


    def WidgetTableVi(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['', 'İsim', 'Soyisim', 'Bölüm', 'Tarih','Araç Plaka','Tutar'])
        table = self.database.kullanicilarTable('SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim, Bolum.bolum_name,yakit.tarih,arac_plaka.aracPlaka, yakit.tutar FROM kullanicilar INNER JOIN yakit ON kullanicilar.ID=yakit.kullaniciID INNER JOIN Bolum ON kullanicilar.bolumID=Bolum.ID INNER JOIN arac_plaka ON yakit.aracID=arac_plaka.ID')
        self.model.setRowCount(len(table))
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))

        self.ui.tw_yakitTukatim.setModel(self.model)

   