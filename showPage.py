import os
import re
from PyQt5 import uic, QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QDate

class printPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(printPage, self).__init__()
        uic.loadUi('ui/print.ui', self)

        self.FIO = self.findChild(QtWidgets.QLabel, 'FIO')
        self.years_old = self.findChild(QtWidgets.QLabel, 'years_old')
        self.birthDate = self.findChild(QtWidgets.QLabel, 'birthDate')
        self.inf = self.findChild(QtWidgets.QLabel, 'inf')
        self.photo = self.findChild(QtWidgets.QLabel, 'photo')
        self.TodayDate = self.findChild(QtWidgets.QLabel, 'TodayDate')
        
        self.place = self.findChild(QtWidgets.QLabel, 'place')
        self.doctor = self.findChild(QtWidgets.QLabel, 'doctor')
        self.healingList = self.findChild(QtWidgets.QListWidget, 'healingList')
        
        self.galeryStart = self.findChild(QtWidgets.QListWidget, 'galeryStart')
        self.galeryEnd = self.findChild(QtWidgets.QListWidget, 'galeryEnd')
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')

    def print_ui(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            printer.setPageSize(QPrinter.Letter)

            painter = QPainter(printer)
            
            scale_factor = printer.pageRect().width() / self.width()
            painter.scale(scale_factor, scale_factor)
            self.render(painter)

            painter.end()
            
    def print_preview_page(self, printer):
        painter = QPainter(printer)
        scale_factor = printer.pageRect().width() / self.width()
        painter.scale(scale_factor, scale_factor)
        self.render(painter)
        painter.end()

class show_page(QtWidgets.QMainWindow):
    def __init__(self):
        super(show_page, self).__init__()
        uic.loadUi('ui/show-page.ui', self)

        self.printClass = printPage()

        self.goBack_btn = self.findChild(QtWidgets.QPushButton, 'goBack_btn')
        self.goBack_btn2 = self.findChild(QtWidgets.QPushButton, 'goBack_btn_2')
        self.goBack_btn3 = self.findChild(QtWidgets.QPushButton, 'goBack_btn_3')
        self.goBack_btn4 = self.findChild(QtWidgets.QPushButton, 'goBack_btn_4')
        
        self.FIO = self.findChild(QtWidgets.QLabel, 'FIO')
        self.years_old = self.findChild(QtWidgets.QLabel, 'years_old')

        self.birthDate = self.findChild(QtWidgets.QLabel, 'birthDate')
        self.inf = self.findChild(QtWidgets.QLabel, 'inf')
        self.listCount = self.findChild(QtWidgets.QLabel, 'listCount')
        self.Addictional = self.findChild(QtWidgets.QStackedWidget, 'Addictional')
        self.doc_list = self.findChild(QtWidgets.QListWidget, 'doc_list')
        self.photo = self.findChild(QtWidgets.QLabel, 'photo')
        self.previous = self.findChild(QtWidgets.QPushButton, 'previous')
        self.next = self.findChild(QtWidgets.QPushButton, 'next')
        self.print = self.findChild(QtWidgets.QPushButton, 'print')
        self.preview = self.findChild(QtWidgets.QPushButton, 'preview')

        self.place = self.findChild(QtWidgets.QLabel, 'place')
        self.doctor_name = self.findChild(QtWidgets.QLabel, 'doctor_name')
        self.listWidget = self.findChild(QtWidgets.QListWidget, 'listWidget')
        self.imageWidget = self.findChild(QtWidgets.QListWidget, 'imageWidget')
        self.listWidget_3 = self.findChild(QtWidgets.QListWidget, 'listWidget_3')
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        self.nextPage = self.findChild(QtWidgets.QPushButton, 'nextPage')
        self.nextPage2 = self.findChild(QtWidgets.QPushButton, 'nextPage2')
        self.previousPage2 = self.findChild(QtWidgets.QPushButton, 'previousPage2')
        self.nextPage3 = self.findChild(QtWidgets.QPushButton, 'nextPage3')
        self.previousPage3 = self.findChild(QtWidgets.QPushButton, 'previousPage3')
        self.previousPage4 = self.findChild(QtWidgets.QPushButton, 'previousPage4')

        self.previous.clicked.connect(lambda: self.listPage(-1))
        self.next.clicked.connect(lambda: self.listPage(1))

        self.print.clicked.connect(self.print_ui)
        self.preview.clicked.connect(self.print_preview)

        self.doc_list.itemDoubleClicked.connect(self.open_file)
        self.photo.mouseDoubleClickEvent = lambda event: self.open_photo(self.photo)

        self.nextPage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))
        self.nextPage2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))
        self.previousPage2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1))
        self.nextPage3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))
        self.previousPage3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1))
        self.previousPage4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1))

    def open_file(self,  item):
        value = "AppData\\Roaming\\DataBaseManage\\files\\" + item.text()
        if os.path.exists(value):
            os.startfile(value)
    def open_photo(self, item):
        style = item.styleSheet()
        url = re.search(r"url\((.*?)\)", style)
        if url != None:
             os.startfile(url.group(1))

    def listPage(self, value): #previous and next page function
        current = self.Addictional.currentIndex()
        self.Addictional.setCurrentIndex(current + value)
        self.listCount.setText(f"№{self.Addictional.currentIndex()}")


    def updatePrintData(self):
        self.printClass.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex())
        self.printClass.photo.setStyleSheet(self.photo.styleSheet())
        self.printClass.FIO.setText(self.FIO.text())
        self.printClass.years_old.setText(self.years_old.text())
        self.printClass.birthDate.setText(self.birthDate.text())
        self.printClass.inf.setText(self.inf.text())

        self.printClass.place.setText(self.place.text())
        self.printClass.doctor.setText(self.doctor_name.text())

        self.printClass.healingList.clear()
        count = 1
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            text = item.text()
            self.printClass.healingList.addItem(f'{count}. {text}')
            count+=1
        
        self.printClass.galeryStart.clear()
        for i in range(self.imageWidget.count()):
            itemObj = self.imageWidget.item(i)

            text = itemObj.text()
            icon = itemObj.icon()
            item = QListWidgetItem(text)
            item.setIcon(icon)
            self.printClass.galeryStart.addItem(item)

        self.printClass.galeryEnd.clear()
        for i in range(self.listWidget_3.count()):
            itemObj = self.listWidget_3.item(i)

            text = itemObj.text()
            icon = itemObj.icon()
            item = QListWidgetItem(text)
            item.setIcon(icon)
            self.printClass.galeryEnd.addItem(item)



        today = QDate.currentDate()
        today_str = today.toString("yyyy-MM-dd")
        self.printClass.TodayDate.setText(today_str)

    def print_ui(self):
        self.updatePrintData()
        self.printClass.print_ui()

    def print_preview(self):
        printer = QPrinter()
        preview_dialog = QPrintPreviewDialog(printer, self)
        self.printClass.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex())

        self.updatePrintData()
        preview_dialog.paintRequested.connect(self.printClass.print_preview_page)

        # Show the preview dialog
        preview_dialog.exec_()
