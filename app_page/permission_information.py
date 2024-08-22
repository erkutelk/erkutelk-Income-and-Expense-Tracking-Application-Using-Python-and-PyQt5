from main import App
from PyQt5.QtWidgets import QTableView, QDialog
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime
import pandas as pd
from PyQt5.QtSql import QSqlQuery
import pandas as pd
from PyQt5.QtSql import QSqlQuery
import os

class pageInformation(QtWidgets.QMainWindow):
    def __init__(self,ui,name):
        super(pageInformation,self).__init__()
        self.ui = ui
        self.name=name
        self.today = date.today()
        self.gunSayisi=0
        self.database = Database()
        print(name,' Sayfasına geçildi...')
        self.ui.baslangcTarih.clicked.connect(self.show_date)
        self.tarihAraligi=[]
        self.ui.baslangcTarih.hide()
        self.ui.label_36.hide()
        self.ui.tabWidget.currentChanged.connect(self.tabwidget)
        
        self.enFazlaizinKullanan()
        self.izinliolanKisiler()
        self.izinleri_devam_edenler()

        


    def tabwidget(self,index):
        if index == 1:
            self.tablo()
        elif index==2:
            self.izinBilgilsiEkle()
        elif index==0:
            print('Anasayfa değeri seçildi...')


    def izinBilgilsiEkle(self):
        self.label_Callender_goster()
        self.cb_kullaniciSecme()
        self.radioButton()
        self.show_date()


    def tablo(self):
        self.WidgetTableVik('SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim,izin.aciklama,izin.baslangicTarihi,izin.bitisTarihi,izin.gun_sayisi FROM izin INNER JOIN izin_kategori ON izin_kategori.ID = izin.borcKategori INNER JOIN kullanicilar ON kullanicilar.ID = izin.KullaniciID INNER JOIN Bolum ON Bolum.ID = kullanicilar.bolumID ',['ID','İsim', 'Soyisim','Açıklama','Başlangıç Tarihi','Bitiş Tarihi','Gün Sayısı'])

    def label_Callender_goster(self):
        if self.ui.baslangcTarih.isVisible() and self.ui.label_36.isVisible():
            self.ui.baslangcTarih.hide()
            self.ui.label_36.hide()
        else:
            self.ui.baslangcTarih.show()
            self.ui.label_36.show()

    def cb_kullaniciSecme(self):
            self.ui.cb_kullanici.clear()
            for a in self.database.table('SELECT * FROM kullanicilar'):
                isim = str(a[1])
                soyisim = str(a[2])
                value = f"{isim} {soyisim}".upper()  
                self.ui.cb_kullanici.addItem(value,str(a[0])) 


    def enFazlaizinKullanan(self):
        for a in self.database.table('SELECT TOP 1 kullanicilar.isim,kullanicilar.soyisim, Bolum.bolum_name,SUM(izin.gun_sayisi),izin_kategori.Kategori FROM izin  INNER JOIN kullanicilar ON izin.KullaniciID=kullanicilar.ID INNER JOIN izin_kategori ON izin_kategori.ID=izin.borcKategori INNER JOIN Bolum ON Bolum.ID=kullanicilar.bolumID GROUP BY kullanicilar.isim,kullanicilar.soyisim, Bolum.bolum_name,izin_kategori.Kategori ORDER BY MAX(izin.gun_sayisi) DESC'):
            isim=str(a[0])
            soyisim=str(a[1])
            izin=str(a[2])
            self.ui.label_26.setText(f'{isim} {soyisim}'.title())

    def bugünİzinAlan(self):
        liste = []
        for a in self.database.table(f"SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim FROM izin INNER JOIN kullanicilar ON izin.KullaniciID = kullanicilar.ID WHERE izin.baslangicTarihi = '{self.today}' GROUP BY kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim"):
            isim = f"{a[1]} {a[2]}"
            liste.append(isim)
        names_str = '\n'.join(liste)#Bir litede bulunan elemnları tek bir çıktı vermesini sağlamak için kullanılır, liste elemnlarını birleştiriyor,sonra aralarına bir satır ekliyor.
        if len(liste)==0:
            self.ui.label_32.setText('Yok')
        else:
            self.ui.label_32.setText(names_str.title())

    def izinliolanKisiler(self):
        for isim in self.database.table(f"SELECT COUNT(*) AS isim FROM (SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim FROM izin INNER JOIN kullanicilar ON izin.KullaniciID = kullanicilar.ID WHERE izin.baslangicTarihi = '{self.today}'GROUP BY kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim) AS subquery"):
            self.ui.label_28.setText(str(isim[0]))

    def izinliolanKisiler(self):
        for isim in self.database.table(f"SELECT COUNT(*) AS isim FROM (SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim FROM izin INNER JOIN kullanicilar ON izin.KullaniciID = kullanicilar.ID WHERE izin.baslangicTarihi = '{self.today}'GROUP BY kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim) AS subquery"):
            self.ui.label_28.setText(str(isim[0]))

    def izinleri_devam_edenler(self):
        liste=[]
        for isim in self.database.table(f"SELECT k.isim, k.soyisim, i.baslangicTarihi, i.bitisTarihi FROM izin i INNER JOIN kullanicilar k ON k.ID = i.KullaniciID INNER JOIN (SELECT KullaniciID, MAX(baslangicTarihi) AS sonBaslangicTarihi FROM izin GROUP BY KullaniciID) AS sonIzin ON i.KullaniciID = sonIzin.KullaniciID AND i.baslangicTarihi = sonIzin.sonBaslangicTarihi;"):
            bitis_tarihi = isim[3].date()#Veritabanından gelen veriyi python ile pythonun anlayabileceği biçime getirmemiz gerekli
            if bitis_tarihi >= self.today:
                kullanici=f'{str(isim[0])} {str(isim[1])}'
                liste.append(kullanici)
            else:
                self.ui.label_63.setText('İzini devam eden kişi yok')
        names_str = '\n'.join(liste)
        self.ui.label_63.setText(names_str)
    def WidgetTableVik(self,value,header):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(header)
        
        table = self.database.kullanicilarTable(value)
        self.model.setRowCount(len(table))
        
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))
        
        self.ui.tableView_2.setModel(self.model)

    def pepInsert(self):
            deger=self.radioButton()
            kullaniciID = self.ui.cb_kullanici.currentIndex() + 1
            kullaniciName = self.ui.cb_kullanici.currentText()
            aciklamaText=self.ui.plainTextEdit_3.toPlainText()
            self.database.ekle('izin', KullaniciID=kullaniciID,izinKullandi=True, baslangicTarihi=self.tarihAraligi[-2],bitisTarihi=self.tarihAraligi[-1],borcKategori=deger,gun_sayisi=self.gunSayisi,aciklama=aciklamaText)
            print(f'{kullaniciName} kullanıcısına izin bilgisi eklendi')
            self.WidgetTableVik('SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim,izin.aciklama,izin.baslangicTarihi,izin.bitisTarihi,izin.gun_sayisi FROM izin INNER JOIN izin_kategori ON izin_kategori.ID = izin.borcKategori INNER JOIN kullanicilar ON kullanicilar.ID = izin.KullaniciID INNER JOIN Bolum ON Bolum.ID = kullanicilar.bolumID ',['ID','İsim', 'Soyisim','Açıklama','Başlangıç Tarihi','Bitiş Tarihi','Gün Sayısı'])
            self.tablo()
            self.bugünİzinAlan()
            
    def radioButton(self):
        if self.ui.radioButton.isChecked():
            return 1
        elif self.ui.radioButton_2.isChecked():
            return 2
        elif self.ui.radioButton_3.isChecked():
            return 3
        else:
            print('lütfen bir izin kategorisi seçiniz')


    def show_date(self):
        selected_date = self.ui.baslangcTarih.selectedDate() #seçilen tarih
        formatted_date = selected_date.toPyDate()            #tarih değerini pythona uygun biçimde dönüştür

        self.tarihAraligi.append(formatted_date)
        if len(self.tarihAraligi) > 1:
            deger = self.tarihAraligi[-2]
            deger2 = self.tarihAraligi[-1]
            value = abs((deger2 - deger).days)
            print(value)
            self.gunSayisi=value

    def excelWrite(self):
            self.database.excellWrite(
                'izinler',
                'SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim, izin.aciklama, izin.baslangicTarihi, izin.bitisTarihi, izin.gun_sayisi FROM izin INNER JOIN izin_kategori ON izin_kategori.ID = izin.borcKategori INNER JOIN kullanicilar ON kullanicilar.ID = izin.KullaniciID INNER JOIN Bolum ON Bolum.ID = kullanicilar.bolumID',
                ["ID", "İsim", "Soyisim", "Açıklama", "Başlangıç Tarihi", "Bitiş Tarihi", "Gün Sayısı"]
            )
