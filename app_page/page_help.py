from main import App
from PyQt5.QtWidgets import QTableView, QDialog,QLabel
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from database import Database
from PyQt5 import QtWidgets
from desigin_page.personel_ekle import Ui_frm_personelEkle
from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime
from sesion import session_manager

class page_help_class(QtWidgets.QMainWindow):
    def __init__(self, ui, name):
        super(page_help_class, self).__init__()
        print(name, 'Sayfasına geçildi...')
        self.ui = ui
        self.database = Database()
        self.add_label_to_widget()
        self.ui.widget_11.hide()
        
    def pepInsert(self):
        try:
            help_title= self.ui.tb_helpTitle.text()
            help_description = self.ui.tb_helpDescription.text()
            kullaniciID_=session_manager.kullaniciID()
            if len(help_title)>0 and len(help_description)>0:
                self.database.ekle('help_all', aciklama=help_description, title=help_title,kullaniciID=kullaniciID_)
                print('Yardım merkeze ulaştı size bir dönüş yapacağız')

            else:
                print('Lütfen title ve descripton alanlarını 10 karakter uzunluğundan fazla giriniz')
        except Exception as e:print('Bir hata meydana geldi',e)


#Kod ile label oluşturmak için bu yöntemi kullanmamız gerekli.
    def add_label_to_widget(self):
        for a in self.database.table('select * from help_all'):
            #Veritabanından aldığım verileri label içerisine yazdırmak için bunu kullanmamız gerekli
            aciklama=str(a[1])
            title=str(a[2])
            value=f'{aciklama}\n{title}'
            label = QLabel(value)
            label.setStyleSheet('background-color: white; border: 1px solid black; padding: 10px;')
            
            # Label içerisindeki yazıları ortalamayı sağlar.
            label.setAlignment(QtCore.Qt.AlignCenter)
            
            # Widget ve düzen erişimi
            widget_11 = self.ui.widget_11
            
            if widget_11.layout() is None:
                # Eğer düzen mevcut değilse yeni bir düzen oluşturur ve widget'a atar
                layout = QVBoxLayout(widget_11)
                widget_11.setLayout(layout)
            else:
                # Mevcut düzeni kullanır
                layout = widget_11.layout()
            
            # Etiketler arasındaki boşluğu azaltır
            layout.setSpacing(5)  
            
            # Düzenin etrafındaki kenar boşluklarını ayarlar
            layout.setContentsMargins(1, 1, 1, 1)  # Kenar boşluklalrını ayarlar
            
            # Etiketi düzenin içine ekler
            layout.addWidget(label)






    
