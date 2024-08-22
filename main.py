from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from desigin_page.personel_ekle import Ui_frm_personelEkle
from database import Database 
from PyQt5.QtWidgets import QTableView, QDialog,QLabel

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_frm_personelEkle()
        self.ui.setupUi(self)
        self.ui.widget_10.hide()
        self.ui.widget_2_is_visible = True
        self.ui.stackedWidget.setCurrentIndex(10)
        self.setWindowTitle(" ")
        self.Database = Database()
        self.ui.widget_2.hide()
        self.SayfaGeçişleri()
        self.loginPage()
    def SayfaGeçişleri(self):
        self.ui.btn_home.clicked.connect(self.home)
        self.ui.btn_permissiInformation.clicked.connect(self.page_information)
        self.ui.btn_personelBilgileri.clicked.connect(self.personel_bilgileri)
        self.ui.pushButton_8.clicked.connect(self.yakitGiderleri_)
        self.ui.pushButton_6.clicked.connect(self.pages_Expenses)
        self.ui.pushButton_9.clicked.connect(self.salary_Information)
        self.ui.pushButton_10.clicked.connect(self.page_help)
        self.ui.pushButton_12.clicked.connect(self.limit_belirleme)
        self.ui.pushButton_13.clicked.connect(self.exitFuncation)
        self.ui.btn_yoneticiEkle.clicked.connect(self.page_kayit)
        self.ui.pushButton_7.clicked.connect(self.gelirler)
        self.ui.btn_home_2.clicked.connect(self.navbarhide)
        self.ui.btn_home_4.clicked.connect(self.navbarhide2)

    
    def navbarhide(self):
        self.ui.widget_2.hide()
        self.ui.widget_10.show()
        self.ui.stackedWidget.setGeometry(70, 0, 1078, 900)
    
    def navbarhide2(self):
        self.ui.widget_2.show()
        self.ui.widget_10.hide()
        self.ui.stackedWidget.setGeometry(230, 0, 100, 900)

    def home(self):
        from app_page.home import HomePage
        self.ui.stackedWidget.setCurrentIndex(0)
        self.home=HomePage(self.ui,'Anasayfa')
        self.ui.widget_2.show()

    def home(self):
        from app_page.home import HomePage
        self.ui.stackedWidget.setCurrentIndex(0)
        self.home=HomePage(self.ui,'Anasayfa')
        self.ui.widget_2.show()
        
    def page_information(self):
        from app_page.permission_information import pageInformation
        self.ui.stackedWidget.setCurrentIndex(1)
        self.page_information_instance = pageInformation(self.ui,'İzin Bilgileri')
        self.ui.izinKaydet.clicked.connect(self.page_information_instance.pepInsert)
        self.ui.pushButton_5.clicked.connect(self.page_information_instance.label_Callender_goster)
        self.ui.pushButton_2.clicked.connect(self.page_information_instance.excelWrite)

    def page_kayit(self):
        from app_page.kayit_page import kayitClass
        self.pageHelparticel=kayitClass(self.ui,'Kullanıcı Ekleme')
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.btn_prsonel_admin.clicked.connect(self.pageHelparticel.pepInsert)

    def yakitGiderleri_(self):
        from app_page.yakit_giderleri import yakitGiderleri
        self.ui.stackedWidget.setCurrentIndex(3)
        self.yakitGiderleri_ = yakitGiderleri(self.ui,'Yakıt giderleri')
        self.ui.btn_yakitKaydet.clicked.connect(self.yakitGiderleri_.pepInsert)

    def personel_bilgileri(self):
        from app_page.personel_bilgileri import personel_bilgileri
        self.ui.stackedWidget.setCurrentIndex(4)
        self.personel_bilgileri_ = personel_bilgileri(self.ui,'Personel Bilgileri')
        self.ui.btn_ekle.clicked.connect(self.personel_bilgileri_.pepInsert)
        self.ui.pushButton_3.clicked.connect(self.personel_bilgileri_.excelWrite)


    def pages_Expenses(self):
        from app_page.giderler import page_expenses_class
        self.ui.stackedWidget.setCurrentIndex(5)
        self.page_expenses_class_intherince=page_expenses_class(self.ui,'Gider İşlemelri')
        self.ui.btn_yakitKaydet_2.clicked.connect(self.page_expenses_class_intherince.pepInsert)

    def salary_Information(self):
        from app_page.maas_bilgileri import salary_information_class
        self.ui.stackedWidget.setCurrentIndex(6)
        self.salary_Information_article=salary_information_class(self.ui,'Maaş Bilgileri')
        self.ui.bt_sallery_save.clicked.connect(self.salary_Information_article.kontrol)

    def limit_belirleme(self):
        from app_page.setLimit import limit_class
        self.limit_class_attrs=limit_class(self.ui,'Limit Oluştur')
        self.ui.stackedWidget.setCurrentIndex(7)
        self.ui.bt_limitKaydet.clicked.connect(self.limit_class_attrs.pepInsert)
        
    def gelirler(self):
        from app_page import gelirler
        self.gelirlerAttrs=gelirler.gelirlerClass(self.ui,'Gelirler')
        self.ui.stackedWidget.setCurrentIndex(8)
        self.ui.bt_limitKaydet_3.clicked.connect(self.gelirlerAttrs.kaydet)

    def page_help(self):
        from app_page.page_help import page_help_class
        self.pageHelparticel=page_help_class(self.ui,'Yardım Oluştur')
        self.ui.stackedWidget.setCurrentIndex(9)
        self.ui.bt_limitKaydet_2.clicked.connect(self.pageHelparticel.pepInsert)

    def loginPage(self):
        from app_page.loginPage import loginPage
        self.loginPagee = loginPage(self.ui,'Login Page')
        self.ui.login_giris.clicked.connect(self.loginPagee.Giris)

    def exitFuncation(self):
        self.ui.widget_2.hide()
        self.ui.stackedWidget.setCurrentIndex(10)
        self.ui.label_35.setText('Çıkış yapıldı')
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
