from datetime import date
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton, QStyleOptionViewItem, QStyle, QVBoxLayout, QLineEdit, QLabel, QDialog, QComboBox
from PyQt5.QtCore import Qt, QRect, QEvent
from database import Database

class personel_bilgileri(QtWidgets.QMainWindow):
    def __init__(self, ui, name):
        super(personel_bilgileri, self).__init__()
        print(name, 'Sayfasına geçildi...')
        self.ui = ui
        self.database = Database()
        self.comboBax()
        self.today = date.today()
        self.ui.btn_search.clicked.connect(self.yukle)
        self.setupTableView()

    def setupTableView(self):
        delegate = ButtonDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(6, delegate)  # Butonların ekleneceği sütun

    def yukle(self):
        deger = self.ui.lineEdit.text().strip()
        if deger == '*':
            try:
                self.WidgetTableVi()
            except Exception as e:
                print('Çalışırken bir hata meydana geldi:', e)
        elif deger:
            self.WidgetTableVi(
                f"SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim, kullanicilar.telefon, Bolum.bolum_name, kullanicilar.tarih "
                f"FROM kullanicilar "
                f"INNER JOIN Bolum ON kullanicilar.bolumID = Bolum.ID "
                f"WHERE kullanicilar.isim LIKE '{deger}%'"
            )
        else:
            print('Tablo değerleri yüklenirken bir hata meydana geldi çalışmadı')

    def comboBax(self):
        self.ui.cb_bolum.clear()
        for a in self.database.table('SELECT * FROM Bolum'):
            self.ui.cb_bolum.addItem(str(a[1]), str(a[0]))#Veritabanından gelen değeri Id değerini ve kategori ismini almamızı sağlar.

    def WidgetTableVi(self, 
                    value='SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim, kullanicilar.telefon, Bolum.bolum_name, kullanicilar.tarih '
                    'FROM kullanicilar '
                    'INNER JOIN Bolum ON kullanicilar.bolumID = Bolum.ID'):
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ID', 'İsim', 'Soyisim', 'Telefon', 'Bölüm', 'Başlangıç Tarihi', ''])
        table = self.database.kullanicilarTable(value)
        self.model.setRowCount(len(table))
        for row, rowData in enumerate(table):
            for col, item in enumerate(rowData):
                self.model.setItem(row, col, QStandardItem(str(item)))

        self.ui.tableView.setModel(self.model)

    def pepInsert(self):
        try:
            isim = self.ui.textEdit.toPlainText().strip()
            soyisim = self.ui.textEdit_2.toPlainText().strip()
            telefon = self.ui.textEdit_4.toPlainText().strip()
            bolum = self.ui.cb_bolum.currentData()

            if telefon.isdigit():
                self.database.ekle('kullanicilar', 
                    isim=isim, 
                    soyisim=soyisim,
                    telefon=int(telefon), 
                    bolumID=int(bolum), 
                    tarih=self.today)

                print(f'{isim} kullanıcısı eklendi')
                self.WidgetTableVi()
                self.textSıfırla()
            else:
                print('İçerisinde harf var veya telefon numarası geçerli değil')
        except:
            print('Eklerken bir hata meydana geldi')
    def textSıfırla(self):
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_4.clear()
        self.ui.cb_bolum.setCurrentIndex(0)

    def excelWrite(self):
        self.database.excellWrite(
            "personelBilgileri",
            "SELECT kullanicilar.ID, kullanicilar.isim, kullanicilar.soyisim, kullanicilar.telefon, Bolum.bolum_name, kullanicilar.tarih "
            "FROM kullanicilar "
            "INNER JOIN Bolum ON kullanicilar.bolumID = Bolum.ID",
            ["ID", "Isim", "Soyisim", "Telefon", "Bolum", 'Baslangic Tarihi']
        )
#Tabloda bulunan verilerin silinmesini ve güncellemesini sağlayan butonların gözükmesini sağlayan kodlar.
class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ButtonDelegate, self).__init__(parent)
        self.database = Database()

    def paint(self, painter, option, index):
        option = QStyleOptionViewItem(option)
        edit_button_rect = QRect(option.rect.x() + 5, option.rect.y() + 5, (option.rect.width() // 2) - 10, option.rect.height() - 10)
        delete_button_rect = QRect(option.rect.x() + (option.rect.width() // 2) + 5, option.rect.y() + 5, (option.rect.width() // 2) - 10, option.rect.height() - 10)

        painter.save()
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(edit_button_rect, QColor('lightblue'))
        else:
            painter.fillRect(edit_button_rect, QColor('white'))
        painter.drawText(edit_button_rect, Qt.AlignCenter, "Düzenle")

        if option.state & QStyle.State_MouseOver:
            painter.fillRect(delete_button_rect, QColor('red'))
        else:
            painter.fillRect(delete_button_rect, QColor('white'))
        painter.drawText(delete_button_rect, Qt.AlignCenter, "Sil")

        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            click_pos = event.pos()
            edit_button_rect = QRect(option.rect.x() + 5, option.rect.y() + 5, (option.rect.width() // 2) - 10, option.rect.height() - 10)
            delete_button_rect = QRect(option.rect.x() + (option.rect.width() // 2) + 5, option.rect.y() + 5, (option.rect.width() // 2) - 10, option.rect.height() - 10)

            if edit_button_rect.contains(click_pos):
                selected_row = index.row()
                selectedID = model.index(selected_row, 0).data()
                isim = model.index(selected_row, 1).data()
                soyisim = model.index(selected_row, 2).data()
                telefon = model.index(selected_row, 3).data()
                bolum = model.index(selected_row, 4).data()

                dialog = Guncelleme_Penceresi(selectedID, isim, soyisim, telefon, bolum, parent=option.widget)
                dialog.exec_()
                return True

            elif delete_button_rect.contains(click_pos):
                selected_row = index.row()
                selectedID = model.index(selected_row, 0).data()
                self.deleteRecord(selectedID)
                model.removeRow(selected_row)
                return True

        return False

    def deleteRecord(self, record_id):
        try:
            self.database.delete(query='DELETE FROM kullanicilar where ID=?',value=record_id)
        except:
            print('Silme sırasında bir hata meydana geldi...')
        



class Guncelleme_Penceresi(QDialog):
    def __init__(self, selectedID, isim, soyisim, telefon, bolum, parent=None):
        super().__init__(parent)
        self.database = Database()
        self.selectedID = selectedID
        self.setWindowTitle("Güncelleme Sayfası")

        layout = QVBoxLayout(self)

        self.textbox1 = QLineEdit(self)
        layout.addWidget(QLabel("İsim"))
        self.textbox1.setText(isim)
        layout.addWidget(self.textbox1)

        self.textbox2 = QLineEdit(self)
        layout.addWidget(QLabel("Soyisim"))
        self.textbox2.setText(soyisim)
        layout.addWidget(self.textbox2)

        self.textbox3 = QLineEdit(self)
        layout.addWidget(QLabel("Telefon"))
        self.textbox3.setText(telefon)
        layout.addWidget(self.textbox3)

        self.cb_bolum = QComboBox(self)
        for a in self.database.table('SELECT * FROM Bolum'):
            self.cb_bolum.addItem(str(a[1]), str(a[0]))  # Add both text and data
        self.cb_bolum.setCurrentIndex(self.cb_bolum.findData(str(bolum)))  # Set the current index to the selected department
        layout.addWidget(QLabel("Bölüm"))
        layout.addWidget(self.cb_bolum)

        self.button = QPushButton('Güncelle', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        updated_isim = self.textbox1.text().strip()
        updated_soyisim = self.textbox2.text().strip()
        updated_telefon = self.textbox3.text().strip()
        updated_bolum = self.cb_bolum.currentData()

        if not updated_isim or not updated_soyisim or not updated_telefon:
            print("Lütfen tüm alanları doldurunuz.")
            return

        if not updated_telefon.isdigit():
            print("Telefon numarası geçerli değil.")
            return

        self.database.guncelleme(
            query='kullanicilar SET isim=?, soyisim=?, telefon=?, bolumID=? WHERE ID=?',
            isim=updated_isim,soyisim=updated_soyisim,telefon=updated_telefon,bolum=updated_bolum,ID=self.selectedID
        )
        print(f"Güncellendi: {updated_isim}, {updated_soyisim}, {updated_telefon}, {updated_bolum}")
