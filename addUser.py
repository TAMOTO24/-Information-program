import os
from PyQt5.QtWidgets import QLabel, QFileDialog, QVBoxLayout, QWidget, QSizePolicy, QListWidgetItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import shutil
from PyQt5.QtCore import Qt
class AddUserWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddUserWindow, self).__init__()
        uic.loadUi('ui/addUser.ui', self)

        try:
            os.makedirs(os.path.join("AppData\\Roaming\\DataBaseManage\\files"))
            os.makedirs("AppData\\Roaming\\ListIMG")
            print("Successful, creation of mainfolder!")
        except OSError as e:
            print("Folder wasn't created: ", e)

        self.data = {
            'img': 'none',
            'FIO': 'No Information',
            'years_old': 'No Information', 
            'date_of_birth': 'No Information',
            'other_images': [],
            'inf': 'No Information',
            'doc_files': '',
            'doctor_name': 'No Information',
            'place': 'No Information',
            'healingList': [],
            'start_healingPhotos': {},
            'end_healingPhotos': {}
        }
        print('awd')
        self.main_photo_path = ""

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

        self.cancel_page = self.findChild(QtWidgets.QPushButton, 'cancel_page')
        self.cancel_page_2 = self.findChild(QtWidgets.QPushButton, 'cancel_page_2')
        self.cancel_page_3 = self.findChild(QtWidgets.QPushButton, 'cancel_page_3')
        self.cancel_page_4 = self.findChild(QtWidgets.QPushButton, 'cancel_page_4')

        self.nextSettingsPage = self.findChild(QtWidgets.QPushButton, 'nextSettingsPage')
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        self.listWidget = self.findChild(QtWidgets.QListWidget, 'listWidget')
        self.addNewText = self.findChild(QtWidgets.QPushButton, 'addNewText')
        self.deleteCurrent = self.findChild(QtWidgets.QPushButton, 'deleteCurrent')
        self.nextSettingsPage2 = self.findChild(QtWidgets.QPushButton, 'nextSettingsPage2')
        self.addImg = self.findChild(QtWidgets.QPushButton, 'addImg')
        self.imageWidget = self.findChild(QtWidgets.QListWidget, 'imageWidget')
        self.pushBtnDeleteIMG = self.findChild(QtWidgets.QPushButton, 'pushBtnDeleteIMG')
        self.nextPage3 = self.findChild(QtWidgets.QPushButton, 'nextPage3')

        self.place = self.findChild(QtWidgets.QLineEdit, 'place')
        self.doctor_name = self.findChild(QtWidgets.QLineEdit, 'doctor_name')

        self.listCount = self.findChild(QtWidgets.QLabel, 'label_9')
        self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")

        self.page = self.findChild(QtWidgets.QWidget, 'page')

        self.otherPhotosList = self.findChild(QtWidgets.QStackedWidget, 'otherPhotosList')
        while self.otherPhotosList.count() > 0: #CLEAN ALL PAGES ON QStackedWidget
            widget = self.otherPhotosList.widget(0)
            self.otherPhotosList.removeWidget(widget)
            widget.deleteLater()

        self.imgAdd = self.findChild(QtWidgets.QPushButton, 'imgAdd')
        self.imgDelete = self.findChild(QtWidgets.QPushButton, 'imgDelete')
        self.previousPage = self.findChild(QtWidgets.QPushButton, 'previousPage')
        self.nextPage = self.findChild(QtWidgets.QPushButton, 'nextPage')
        self.imgDelete = self.findChild(QtWidgets.QPushButton, 'imgDelete')
        self.btn_deleteFile = self.findChild(QtWidgets.QPushButton, 'btn_deleteFile')
        self.btn_addFile = self.findChild(QtWidgets.QPushButton, 'btn_addFile')
        self.docFileList = self.findChild(QtWidgets.QListWidget, 'docFileList')
        self.listWidget_end = self.findChild(QtWidgets.QListWidget, 'listWidget_end')
        self.addIMG2 = self.findChild(QtWidgets.QPushButton, 'addIMG2')
        self.deleteIMG2 = self.findChild(QtWidgets.QPushButton, 'deleteIMG2')


        self.imgDelete.clicked.connect(self.removePage)
        self.previousPage.clicked.connect(lambda: self.listPage(-1))
        self.nextPage.clicked.connect(lambda: self.listPage(1))
        self.imgAdd.clicked.connect(self.addPhotoToList) #add photo to QStackedWidget
        self.photo_screen_add.clicked.connect(self.addMainPhoto) #add main photo
        self.photo_screen_delete.clicked.connect(self.deleteMainPhoto)
        

        self.add_form_btn.clicked.connect(self.updateData)

        self.btn_addFile.clicked.connect(self.addDocFile)
        self.btn_deleteFile.clicked.connect(self.remove_file)
        self.photo_screen_delete.clicked.connect(self.deleteMainPhoto)

        self.addNewText.clicked.connect(self.addValueToList)
        self.deleteCurrent.clicked.connect(lambda: self.deleteCurrentElement(self.listWidget))
        self.deleteIMG2.clicked.connect(lambda: self.deleteCurrentElement(self.listWidget_end))

        self.pushBtnDeleteIMG.clicked.connect(lambda: self.deleteCurrentElement(self.imageWidget))
        self.addImg.clicked.connect(lambda: self.addPhoto(self.imageWidget, 1))
        self.addIMG2.clicked.connect(lambda: self.addPhoto(self.listWidget_end, 0))

        self.nextSettingsPage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))
        self.nextSettingsPage2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))
        self.nextPage3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1))

    def addValueToList(self):
        item = QListWidgetItem("Новий елемент.")
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.listWidget.addItem(item)
        

    def deleteCurrentElement(self, element):
        current_item = element.currentItem()
        if current_item is not None:
            sender_object_name = self.sender().objectName()
            row = element.row(current_item)
            element.takeItem(row)

            if element is self.imageWidget:
                keys = list(self.data['start_healingPhotos'].keys())
                del self.data['start_healingPhotos'][keys[row]]
            elif element is self.listWidget_end:
                keys = list(self.data['end_healingPhotos'].keys())
                del self.data['end_healingPhotos'][keys[row]]


    def deleteMainPhoto(self):
        if hasattr(self, 'current_style_photo'):
            self.photoScreen.setStyleSheet(self.current_style_photo)
            self.photoScreen.setText('+')
            self.data["img"] = "delete"

    def addPhoto(self, element, value):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Виберите файл', "", "Images (*.png *.jpg *.bmp *.gif)")
        
        if file_path:
            filename = os.path.basename(file_path)
            shutil.copy(file_path, "AppData\\Roaming\\ListIMG")

            icon = QIcon("AppData\\Roaming\\ListIMG\\" + filename)
            item = QListWidgetItem("Текст")
            item.setIcon(icon)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            element.addItem(item)
            if value == 1:
                self.data['start_healingPhotos'][filename] = ''
            else:
                self.data['end_healingPhotos'][filename] = ''


    def removePage(self):# remove
        if self.otherPhotosList.count() != 0:
            widget = self.otherPhotosList.widget(self.otherPhotosList.currentIndex())
            self.otherPhotosList.removeWidget(widget)
            widget.deleteLater()
            if self.data["other_images"]:
                self.data["other_images"].pop(self.otherPhotosList.currentIndex())

            self.otherPhotosList.setCurrentIndex(self.otherPhotosList.currentIndex())
            if self.otherPhotosList.count() == 0:
                self.listCount.setText(f'№None')

    def listPage(self, value): #previous and next page function
        current = self.otherPhotosList.currentIndex()
        self.otherPhotosList.setCurrentIndex(current + value)
        self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")

    def addPhotoToList(self):
        options = QFileDialog.Options()
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)

        if photo_path:

            self.data['other_images'].append(photo_path) #add new img path
            print("added", self.data['other_images'])
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
            widget.setGeometry(0, 0, 0, 0)

            self.otherPhotosList.addWidget(widget) # add widget
            self.otherPhotosList.setCurrentWidget(widget)
            self.listCount.setText(f"№{self.otherPhotosList.currentIndex()}")
        
    def deleteMainPhoto(self):
        if hasattr(self, 'current_style_photo'):
            self.photoScreen.setStyleSheet(self.current_style_photo)
            self.photoScreen.setText('+')

    def addMainPhoto(self):
        options = QFileDialog.Options()
        main_photo_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)
        
        if main_photo_path:
            print(main_photo_path, _)
            self.data["img"] = main_photo_path
            print("Nothing ", self.data['img'])
            self.current_style_photo = self.photoScreen.styleSheet()
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
            icon = QIcon('Program\\ui\\word_icon.png')
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

        if self.place.text() != '':
            self.data['doctor_name'] = self.doctor_name.text()

        if self.doctor_name.text() != '':
            self.data['place'] = self.place.text()

        if self.data['healingList'] == []:
            List = []
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                text = item.text()
                List.append(text)

            self.data['healingList'] = List

        count = 0
        for i in self.data['start_healingPhotos']:
            item = self.imageWidget.item(count)
            self.data['start_healingPhotos'][i] = item.text()
            count += 1

        count = 0
        for i in self.data['end_healingPhotos']:
            item = self.listWidget_end.item(count)
            self.data['end_healingPhotos'][i] = item.text()
            count += 1

        print("DATA: ", self.data)
