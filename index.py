from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType('library.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.db = MySQLdb.connect(host='localhost', user='markomiseljic', password='markomiseljic', db='library')
        self.cur = self.db.cursor()
        self.setupUi(self)
        self.handle_ui_changes()
        self.handle_buttons()

        self.show_categories()
        self.show_authors()
        self.show_publishers()

        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()

    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.show_themes)
        self.pushButton_21.clicked.connect(self.hiding_themes)

        self.pushButton.clicked.connect(self.open_day_to_day_tab)
        self.pushButton_2.clicked.connect(self.open_book_tab)
        self.pushButton_26.clicked.connect(self.open_client_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)

        self.pushButton_7.clicked.connect(self.add_new_book)

        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_15.clicked.connect(self.add_author)
        self.pushButton_16.clicked.connect(self.add_publisher)

        self.pushButton_9.clicked.connect(self.search_books)
        self.pushButton_8.clicked.connect(self.edit_books)
        self.pushButton_10.clicked.connect(self.delete_books)

        self.pushButton_11.clicked.connect(self.add_user)
        self.pushButton_12.clicked.connect(self.login)
        self.pushButton_13.clicked.connect(self.edit_user)

        self.pushButton_17.clicked.connect(self.dark_orange_theme)
        self.pushButton_18.clicked.connect(self.dark_blue_theme)
        self.pushButton_20.clicked.connect(self.dark_grey_theme)
        self.pushButton_19.clicked.connect(self.qdark_theme)

        self.pushButton_22.clicked.connect(self.add_new_client)
        self.pushButton_24.clicked.connect(self.search_client)
        self.pushButton_23.clicked.connect(self.edit_client)
        self.pushButton_25.clicked.connect(self.delete_client)

    def handle_ui_changes(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)

    def show_themes(self):
        self.groupBox_3.show()

    def hiding_themes(self):
        self.groupBox_3.hide()

    ##########################################
    ######### oppening tabs ##################

    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(4)

    ##########################################
    ################# Books ##################
    def add_new_book(self):
        book_title = self.lineEdit_3.text()
        book_code = self.lineEdit_2.text()
        book_category = self.comboBox_3.currentIndex()
        book_author = self.comboBox_4.currentIndex()
        book_publisher = self.comboBox_5.currentIndex()
        book_price = self.lineEdit_4.text()
        book_description = self.textEdit.toPlainText()

        self.cur.execute('''
            INSERT INTO book(book_name,book_description,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))
        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_3.setText('')
        self.lineEdit_2.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.textEdit.setPlainText('')

    def search_books(self):
        book_title = self.lineEdit_8.text()
        self.cur.execute('''
            SELECT * FROM book WHERE book_name = %s
        ''', (book_title,))

        data = self.cur.fetchone()
        print(data)
        self.statusBar().showMessage("BOOK IS FOUND")

        self.lineEdit_7.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_5.setText(data[3])
        self.comboBox_7.setCurrentIndex(data[4])
        self.comboBox_6.setCurrentIndex(data[5])
        self.comboBox_8.setCurrentIndex(data[6])
        self.lineEdit_6.setText(str(data[7]))

    def edit_books(self):
        book_title = self.lineEdit_7.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_5.text()
        book_category = self.comboBox_7.currentIndex()
        book_author = self.comboBox_6.currentIndex()
        book_publisher = self.comboBox_8.currentIndex()
        book_price = float(self.lineEdit_6.text())

        search_book_title = self.lineEdit_8.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name=%s
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price,
              search_book_title))
        self.db.commit()
        self.statusBar().showMessage("Book updated")

    def delete_books(self):
        search_book_title = self.lineEdit_8.text()

        warning = QMessageBox.warning(self, 'Delete book', 'Are you sure you want to delete this book', QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            self.cur.execute('''
                DELETE FROM book WHERE book_name=%s
            ''', (search_book_title,))
            self.db.commit()
            self.statusBar().showMessage("Book deleted")

    ##########################################
    ################# Clients ##################
    def add_new_client(self):
        client_name = self.lineEdit_22.text()
        client_email = self.lineEdit_23.text()
        client_national_id = self.lineEdit_24.text()

        self.cur.execute('''
            INSERT INTO clients(client_name, client_email, client_national_id) 
            VALUES (%s, %s, %s)
        ''', (client_name, client_email, client_national_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')

    def show_all_clients(self):
        pass

    def search_client(self):
        client_national_id = self.lineEdit_28.text()

        sql = '''SELECT * FROM clients WHERE client_national_id = %s'''
        self.cur.execute(sql, (client_national_id,))
        data = self.cur.fetchone()
        print(data)

        self.statusBar().showMessage('Client Found')

        self.lineEdit_27.setText(data[1])
        self.lineEdit_25.setText(data[2])
        self.lineEdit_26.setText(data[3])

    def edit_client(self):
        client_original_national_id = self.lineEdit_26.text()

        client_name = self.lineEdit_27.text()
        client_email = self.lineEdit_25.text()
        client_national_id = self.lineEdit_26.text()

        self.cur.execute('''
            UPDATE clients SET client_name=%s, client_email=%s, client_national_id=%s WHERE client_national_id=%s
        ''', (client_name, client_email, client_national_id, client_original_national_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client Updated')

    def delete_client(self):
        client_original_national_id = self.lineEdit_26.text()

        warning = QMessageBox.warning(self, "Delete Client", "are you sure you want to delete this client", QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            self.cur.execute('''
                DELETE FROM clients WHERE client_national_id=%s
            ''', (client_original_national_id,))
            self.db.commit()
            self.close()
            self.statusBar().showMessage('Client Deleted')

    ##########################################
    ################# Users ##################
    def add_user(self):
        username = self.lineEdit_9.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password2 = self.lineEdit_12.text()

        if password == password2:
            self.cur.execute('''
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (%s, %s, %s)
            ''', (username, email, password))
            self.db.commit()
            self.statusBar().showMessage('New User Added')
        else:
            self.label_30.setText('Please add a valid password twice')

    def edit_user(self):
        username = self.lineEdit_18.text()
        email = self.lineEdit_15.text()
        password = self.lineEdit_17.text()
        password2 = self.lineEdit_16.text()

        original_name = self.lineEdit_14.text()

        if password == password2:
            self.cur.execute('''
                UPDATE users SET user_name=%s, user_email=%s, user_password=%s WHERE user_name=%s 
            ''', (username, email, password, original_name))
            self.db.commit()
            self.statusBar().showMessage('User Data Updated Successfully')
        else:
            print("Make sure you entered password correctly")

    def login(self):
        username = self.lineEdit_14.text()
        password = self.lineEdit_13.text()

        sql = '''
            SELECT * FROM users
        '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            print(row)
            if username == row[1] and password == row[3]:
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_18.setText(row[1])
                self.lineEdit_15.setText(row[2])
                self.lineEdit_17.setText(row[3])
                self.lineEdit_16.setText('')

    ##########################################
    ################# Settings ###############
    def add_category(self):
        new_category = self.lineEdit_19.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''', (new_category,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added ')
        self.lineEdit_19.setText('')
        self.show_categories()
        self.show_category_combobox()

    def show_categories(self):
        self.cur.execute('''
            SELECT category_name From category
        ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def add_author(self):
        author_name = self.lineEdit_20.text()

        self.cur.execute('''
                    INSERT INTO authors (author_name) VALUES (%s)
                ''', (author_name,))

        self.db.commit()
        self.statusBar().showMessage('New Author Added ')
        self.lineEdit_20.setText('')
        self.show_authors()
        self.show_author_combobox()

    def show_authors(self):
        self.cur.execute('''
                    SELECT author_name From authors
                ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def add_publisher(self):
        publisher_name = self.lineEdit_21.text()

        self.cur.execute('''
                    INSERT INTO publisher (publisher_name) VALUES (%s)
                ''', (publisher_name,))

        self.db.commit()
        self.statusBar().showMessage('New Publisher Added ')
        self.lineEdit_21.setText('')
        self.show_publishers()
        self.show_publisher_combobox()

    def show_publishers(self):
        self.cur.execute('''
                            SELECT publisher_name From publisher
                        ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    #############################################################
    ################# show settings data in UI ##################
    def show_category_combobox(self):
        self.cur.execute('''
                    SELECT category_name From category
                ''')
        data = self.cur.fetchall()
        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_7.addItem(category[0])

    def show_publisher_combobox(self):
        self.cur.execute('''
                    SELECT publisher_name From publisher
                ''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_8.addItem(publisher[0])

    def show_author_combobox(self):
        self.cur.execute('''
                    SELECT author_name From authors
                ''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_6.addItem(author[0])

    ###########################################
    ################# UI Themes ###############

    def dark_blue_theme(self):
        style = open('themes/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_grey_theme(self):
        style = open('themes/darkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qdark_theme(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
