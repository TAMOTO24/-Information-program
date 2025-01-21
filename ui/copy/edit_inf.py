import os
from PyQt5.QtWidgets import QLabel, QFileDialog, QVBoxLayout, QWidget, QSizePolicy, QListWidgetItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import shutil

class edit_page(QtWidgets.QMainWindow): #NEW CLASS FOR EDITING INF
    def __init__(self):
        super(edit_page, self).__init__()
        uic.loadUi('ui/addUser.ui', self)

        self.data = {
            'img': 'none',
            'FIO': 'No Informaion',
            'years_old': 'No Informaion', 
            'date_of_birth': 'No Informaion',
            'other_images': [],
            'inf': 'No Informaion',
            'doc_files': ''
        }
        self.main_photo_path = ""
        self.current_style_photo = "QLabel {\nborder: 2px dashed black;\nfont-size: 30px;\npadding: 80px;\n}"

        self.addChild()

    def addChild(self):
        self.fio_line = self.findChild(QtWidgets.QLineEdit, 'FIOLine')
        self.textEdit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.year_oldLine = self.findChild(QtWidgets.QLineEdit, 'year_oldLine')
        self.dateLine = self.findChild(QtWidgets.QLineEdit, 'dateLine')
        self.add_form_btn = self.findChild(QtWidgets.QPushButton, 'saveChanges')
        self.photoScreen = self.findChild(QtWidgets.QLabel, 'photoScreen')
        self.photo_screen_add = self.findChild(QtWidgets.QPushButton, 'faceIMGAdd')
        self.photo_screen_delete = self.findChild(QtWidgets.QPushButton, 'faceIMGDelete')
        self.btn_menu = self.findChild(QtWidgets.QPushButton, 'btn_menu')
        self.cancel_page = self.findChild(QtWidgets.QPushButton, 'cancel_page')

        self.listCount = self.findChild(QtWidgets.QLabel, 'label_9')
        self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")

        self.page = self.findChild(QtWidgets.QWidget, 'page')

        self.otherPhotosList = self.findChild(QtWidgets.QStackedWidget, 'otherPhotosList')
        self.imgAdd = self.findChild(QtWidgets.QPushButton, 'imgAdd')
        self.imgDelete = self.findChild(QtWidgets.QPushButton, 'imgDelete')
        self.previousPage = self.findChild(QtWidgets.QPushButton, 'previousPage')
        self.nextPage = self.findChild(QtWidgets.QPushButton, 'nextPage')
        self.imgDelete = self.findChild(QtWidgets.QPushButton, 'imgDelete')
        self.btn_deleteFile = self.findChild(QtWidgets.QPushButton, 'btn_deleteFile')
        self.btn_addFile = self.findChild(QtWidgets.QPushButton, 'btn_addFile')
        self.docFileList = self.findChild(QtWidgets.QListWidget, 'docFileList')

        self.imgDelete.clicked.connect(self.removePage)
        self.previousPage.clicked.connect(lambda: self.listPage(-1))
        self.nextPage.clicked.connect(lambda: self.listPage(1))
        self.imgAdd.clicked.connect(self.addPhotoToList) #add photo to QStackedWidget
        self.photo_screen_add.clicked.connect(self.addMainPhoto) #add main photo
        self.photo_screen_delete.clicked.connect(self.deleteMainPhoto)

        self.add_form_btn.clicked.connect(self.updateData)

        self.btn_addFile.clicked.connect(self.addDocFile)
        self.btn_deleteFile.clicked.connect(self.remove_file)

    def removePage(self):# remove and 
        widget = self.otherPhotosList.widget(self.otherPhotosList.currentIndex())
        self.otherPhotosList.removeWidget(widget)
        widget.deleteLater()

    def listPage(self, value): #previous and next page function
        current = self.otherPhotosList.currentIndex()
        self.otherPhotosList.setCurrentIndex(current + value)
        self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")

    def addPhotoToList(self):
        options = QFileDialog.Options()
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)

        if photo_path:

            self.data['other_images'].append(photo_path) #add new img path
            layout = QVBoxLayout() #create Layout

            image = QLabel()#create label for img
            image.setStyleSheet(f"border-image: url({photo_path}); ")
            image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
            layout.addWidget(image)

            text = QLabel(photo_path) #set text with photo_path varible
            text.setStyleSheet(f"font-size: 10px;")
            layout.addWidget(text)

            widget = QWidget() #set widget for adding img and text to it
            widget.setLayout(layout)

            self.otherPhotosList.addWidget(widget) # add widget
            self.otherPhotosList.setCurrentWidget(widget)
            self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")
        
    def deleteMainPhoto(self):
        if hasattr(self, 'current_style_photo'):
            self.photoScreen.setStyleSheet(self.current_style_photo)
            self.photoScreen.setText('+')
            self.data["img"] = "delete"

    def addMainPhoto(self):
        options = QFileDialog.Options()
        main_photo_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)
        
        if main_photo_path:
            # print(main_photo_path, _)
            self.data["img"] = main_photo_path
            # print("Nothing ", self.data['img'])
            # self.current_style_photo = self.photoScreen.styleSheet()
            self.photoScreen.setStyleSheet(self.current_style_photo[:-1] + f'border-image: url({main_photo_path}) 0 0 0 0;\n'  \
            + "padding-left: 130px;" + 'background: #464646;' + "}")
            self.photoScreen.setText('')

    def is_item_in_list_widget(self, list_widget, target_text):
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            if item.text() == target_text:
                return True
        return False
    
    def addDocFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Виберите файл', "", "File (*.docx *.doc)")

        if file_path:
            _, file_name = os.path.split(file_path)

            if self.is_item_in_list_widget(self.docFileList, file_name): #If doc file exist then exit
                print("doc-File exist")
                return

            item = QListWidgetItem(file_name, self.docFileList)
            icon = QIcon('img\\word_icon.png')
            item.setIcon(icon)

            self.docFileList.addItem(item)
            shutil.copy(file_path, "AppData\\Roaming\\DataBaseManage\\files")

            self.data['doc_files'] = file_name #add new file path

    def remove_file(self):#Need repair
        selected_item = self.docFileList.currentItem()

        if selected_item != None:
            self.docFileList.takeItem(self.docFileList.row(selected_item))

    def updateData(self):
        if self.fio_line.text() != '':
            self.data['FIO'] = self.fio_line.text()
        if self.year_oldLine.text() != '':
            self.data['years_old'] = self.year_oldLine.text()
        if self.dateLine.text() != '':
            self.data['date_of_birth'] = self.dateLine.text()
        if self.textEdit.toPlainText() != '':
            self.data['inf'] = self.textEdit.toPlainText()
