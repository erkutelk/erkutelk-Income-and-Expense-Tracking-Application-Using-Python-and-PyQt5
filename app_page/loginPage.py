from main import App
from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from app_page.home import HomePage
from sesion import session_manager
class loginPage(QtWidgets.QMainWindow):
    def __init__(self,ui,name):
        super(loginPage,self).__init__()
        self.ui = ui
        self.name=name
        self.database=Database()
        print(self.name,'Sayfasına geçildi')
        
    def Giris(self):
        mail = self.ui.mail.text()
        sifre = self.ui.sifre.text()
        found = False
        
        for a in self.database.table('SELECT kullanicilar.ID,kullanicilar.isim,kullanicilar.soyisim,bolum_name,pers_login.mail,pers_login.sifre,kullanicilar.tarih FROM kullanicilar INNER JOIN pers_login on kullanicilar.ID=pers_login.kullaniciID INNER JOIN Bolum on kullanicilar.bolumID=Bolum.ID'):
            if mail == a[4] and sifre == a[5]:
                self.ui.stackedWidget.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2e2e2e, stop:1 #0f0f0f);')
                session_manager.userID(a[0],f'{a[1]}{a[2]}')
                
                self.kullanici(a[1],a[2])
                self.ui.stackedWidget.setCurrentIndex(0)
                found = True
                HomePage(self.ui,'Home')
                print('Giriş bilgileri doğru')
                break

        if found:
            self.ui.widget_2.show()
        else:
            print('Lütfen şifre ve kullanıcı bilgilerinizi kontrol ederek yeniden giriniz')

    def kullanici(self,isim,soyisim):#Giriş yapan kullanıcın bilgilerini home pencersinde gösterme
        user=f'{isim} {soyisim}'
        self.ui.label_8.setText(user)

        