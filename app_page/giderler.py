from main import App
from PyQt5.QtWidgets import QTableView, QDialog,QListView,QInputDialog,QMessageBox,QLineEdit
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

class page_expenses_class(QtWidgets.QMainWindow):
    def __init__(self,ui,name):
        super(page_expenses_class,self).__init__()
        self.today = date.today()
        self.ui = ui
        self.name=name
        self.database = Database()
        print(name,' Sayfasına geçildi...')
        self.local_pageler()


    def local_pageler(self):
        self.ui.widget_9.hide()
        self.cb_funcation(query='SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim FROM kullanicilar',
                        combobox=self.ui.kullaniciSEc_cb,
                        id_col=0, first_name_col=1, last_name_col=2)
        
        self.cb_funcation(query='SELECT borc_kategorisi.ID,borc_kategorisi.kategori FROM borc_kategorisi',
                        combobox=self.ui.cb_giderler,
                        id_col=0, first_name_col=1, last_name_col=None)
        self.WidgetTableVi()
        self.listView_table()
        self.ui.pushButton_4.clicked.connect(self.ekleme)
        self.ui.pushButton_20.clicked.connect(self.guncelleme)
        self.ui.pushButton_21.clicked.connect(self.silme)


    def cb_funcation(self,query,combobox,id_col,first_name_col,last_name_col):
        combobox.clear()
        for a in self.database.table(query):
            isim = str(a[first_name_col])
            soyisim = str(a[last_name_col]) if last_name_col is not None else ''
            value = f"{isim} {soyisim}".strip().upper()  # Use strip() to remove any trailing spaces
            combobox.addItem(value, str(a[id_col]))

  
    def pepInsert(self):
                remindingRadioChecked=self.remindingRadio()
                try:
                    datetime_value = self.ui.dateTimeEdit_hatirlatma.dateTime()
                    datetime_str = datetime_value.toString('yyyy-MM-dd HH:mm:ss')
                    borcKategorisi=self.ui.cb_giderler.currentIndex()+1
                    kullaniciID = self.ui.kullaniciSEc_cb.currentIndex() + 1
                    aciklamaText=self.ui.tb_aciklamaGiderler.text()
                    tutar=self.ui.tb_giderlerTutar.text()
                    self.database.ekle('borclartablosu',
                                        kullaniciID=kullaniciID,
                                        borc=tutar,
                                        borc_kategorisiID=borcKategorisi ,
                                        aciklama=aciklamaText,
                                        borc_alinan_tarih=self.today,
                                        hatirlatma=remindingRadioChecked,
                                        hatirlatilacakTarih=datetime_str)
                    print('Kullanıcısı eklendi')
                    self.WidgetTableVi()
                except Exception as e:
                      print('Kullanıcısı eklenirken bir hata meydana geldi',e)

    def remindingRadio(self):
        if self.ui.radioButton_4.isChecked():
            print('Evet Hatırlat')
            return 1
        
        if self.ui.radioButton_5.isChecked():
            print('Hatırlatma')
            return 0
        
    def WidgetTableVi(self,value=
                      "SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim,borclar.aciklama,borclar.borc, hatirlatma.hatirlatilack_tarih, borclar.borc_alinan_tarih  FROM borclartablosu AS borclar  INNER JOIN kullanicilar ON kullanicilar.ID = borclar.kullaniciID  INNER JOIN hatirlatma ON hatirlatma.borcdefteriID = borclar.ID"):
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ID', 'İsim', 'Soyisim','Açıklama','Borç', 'Hatıratılacak Tarih','Borç Alınan Tarih'])
        table = self.database.kullanicilarTable(value)
        self.model.setRowCount(len(table))
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))

        self.ui.tableView_5.setModel(self.model)

    def listView_table(self):
        model = QStandardItemModel()
        categories = self.database.table('SELECT borc_kategorisi.kategori FROM borc_kategorisi')        
        for category in categories:
            list_item = QStandardItem(category[0])
            model.appendRow(list_item)
        self.ui.listView.setModel(model)

    def ekleme(self):
        text,ok=QInputDialog.getText(self,'Yeni öğrenci ekleniyor','lütfen yeni kategori ismini giriniz...')
        if ok and text:#Açılan pencere
             self.database.ekle(tablo='borc_kategorisi',kategori=text)
        self.listView_table()

    def guncelleme(self):
        index = self.ui.listView.currentIndex()#öğe seçmemiz gerekli.
        if not index.isValid():
            print("No item selected")
            return        
        current_category = index.data()#Mevcut kategori adını almamızı sağlıyor
        print(current_category)
        text, ok = QInputDialog.getText(self, 'Kategori Güncelleme', f'Lütfen yeni kategori değerini giriniz (Eski Değer: {current_category})')
        if ok and text:
            category_id_query = f"SELECT ID FROM borc_kategorisi WHERE kategori='{current_category}'"# eğerkategori isimleri ile seçtiğim kategori ismi aynıysa Id değerini alır.
            #? [[1]] sql sorgusundan gelen değer bu biçimde gelir. bu yüzden[0][0] şekilini kullanırız.
            
            category_id = self.database.table(category_id_query)[0][0]
            self.database.guncelleme(query='borc_kategorisi SET kategori=? WHERE ID=?', kategori=text, ID=category_id)
            print("Kategori güncellendi")
            self.listView_table()
    
    def silme(self):
            index = self.ui.listView.currentIndex()  # seçilen değer
            if not index.isValid():
                print("No item selected")#Değer seçilmezse
                return
            current_category = index.data()
            category_id_query = f"SELECT ID FROM borc_kategorisi WHERE kategori='{current_category}'"#Kategoriinin ID değerini sql sorgusu ile alıyoruz
            self.category_id = self.database.table(category_id_query)[0][0]
            self.database.delete(query='DELETE FROM borc_kategorisi WHERE ID=?',value=self.category_id)     # silme sql kodu 
            print("Kategori silindi")
            self.listView_table()
