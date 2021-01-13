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

    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.show_themes)
        self.pushButton_21.clicked.connect(self.hiding_themes)

        self.pushButton.clicked.connect(self.open_day_to_day_tab)
        self.pushButton_2.clicked.connect(self.open_book_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)

        self.pushButton_7.clicked.connect(self.add_new_book)

        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_15.clicked.connect(self.add_author)
        self.pushButton_16.clicked.connect(self.add_publisher)

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

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    ##########################################
    ################# Books ##################
    def add_new_book(self):
        book_title = self.lineEdit_3.text()
        book_code = self.lineEdit_2.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()
        book_description = self.textEdit

    def search_books(self):
        pass

    def edit_books(self):
        pass

    def delete_books(self):
        pass

    ##########################################
    ################# Users ##################
    def add_user(self):
        pass

    def edit_user(self):
        pass

    def login(self):
        pass

    ##########################################
    ################# Settings ###############
    def add_category(self):
        new_category = self.lineEdit_19.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''', (new_category,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added ')

    def add_author(self):
        author_name = self.lineEdit_20.text()

        self.cur.execute('''
                    INSERT INTO authors (author_name) VALUES (%s)
                ''', (author_name,))

        self.db.commit()
        self.statusBar().showMessage('New Author Added ')

    def add_publisher(self):
        publisher_name = self.lineEdit_21.text()

        self.cur.execute('''
                    INSERT INTO publisher (publisher_name) VALUES (%s)
                ''', (publisher_name,))

        self.db.commit()
        self.statusBar().showMessage('New Publisher Added ')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
