import os
import sys
import pandas as pd
import pypyodbc
from dotenv import load_dotenv
class Database:
    def __init__(self) -> None:
        load_dotenv(dotenv_path='.env')
        self.db = pypyodbc.connect(
            f"Driver={os.environ['db_driver']};"
            f"Server={os.environ['db_server']};"
            f"Database={os.environ['db_database']};",
            timeout=30
        )
        

    def ekle(self, tablo, **kwargs):
        imlec = self.db.cursor()
        kolonlar = ', '.join(kwargs.keys())#Gelen verilerin araına ',' işareti koymak için kullanılır
        degerler = tuple(kwargs.values())#Gelen değerleri alır sadece, Ad:Erkut ksımın sadece ad kısmını alır
        placeholders = ', '.join('?' * len(kwargs))#Oluşturduğum bu sorguda tablolar sürekli değiştiği için bu fonkisyonu kullnadık gelen paramaetre sayısı kadar soru işareti oluştururur.
        imlec.execute(f"INSERT INTO {tablo} ({kolonlar}) VALUES ({placeholders})", (degerler))
        self.db.commit()
        imlec.close()

    
    def delete(self,value,query='DELETE FROM kullanicilar WHERE ID=?)'):
        imlec=self.db.cursor()
        imlec.execute(query,(value,))
        imlec.commit()

    def table(self,sorgu):
        cursor = self.db.cursor()
        cursor.execute(sorgu)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def kullanicilarTable(self,value):
        cursor=self.db.cursor()
        cursor.execute(value)
        rows=cursor.fetchall()
        cursor.close()
        return rows

    def guncelleme(self,query,**kwargs):
        try:
            cursor = self.db.cursor()
            values = tuple(kwargs.values())#Gelen değerleri almasını sağlar,()Parentez içerisinde alır
            cursor.execute(f'UPDATE {query}', (values))
            self.db.commit()
            cursor.close()
            print('Başarılı bir şekilde güncellem işlemi yapıldı')
        except Exception as e:
            print('Güncelleme sırasında bir hata meydana geldi...',e)


    def excellWrite(self,name:str,sorgu:str,title:str):
            #Dosyayı masaüstüne kaydetmek için bu kod satırını yazmamız gerekli
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            query = self.table(sorgu)

            #Sql tablosundan gelen sorgu sonucunu datafareme çevirmemiz gerekli, bir for döngüsü kullanmamıza gerek yok.
            df = pd.DataFrame(query, columns=title)

            #dosyanın excell dosyasına çevirelmesi için bu kod satırı kullanılmalı. os.path.join dosya yolunu tam olarak birleştiriyor.
            file_path = os.path.join(desktop_path, f'{name}.xlsx')
            df.to_excel(file_path, index=False)#Excell dosyasını kayderken satır sayılarını yazmamasını istiyoruz bu yüzden index=false değerini yazmamız gerekli. 

            print(f"Excel dosyası {file_path} konumuna kaydedildi.")

