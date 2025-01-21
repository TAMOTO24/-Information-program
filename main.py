from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy, QListWidgetItem
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from startPage import Ui_MainWindow
from addUser import AddUserWindow
from showPage import show_page
import re
import sys
import json

class MainWindowWidgets():
    def __init__(self):
        self.frameBorder = 0
        self.label_Photo = 0
        self.label_Inf = 0
        self.label_FIO = 0
        self.date = 0
        self.number = 0

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.show_page = show_page()
        self.edit_inf = AddUserWindow()
        self.add_user_window = AddUserWindow()
        

        self.list_count = 0
        self.mainData = {} #Main users data
        self.widgetsList = [] #widget varibles

        self.show_main_window()

    def show_main_window(self):
        self.ui.setupUi(self)
        self.ui.add_new_member_btn.clicked.connect(self.show_add_user_screen)
        self.ui.lineEdit.textChanged.connect(self.searchFucn)

        with open('my_dict.json', 'r') as file:
            value = json.load(file)
        # value = settings.value('user_data', '')
        if value != {}:
            for key, text in value.items():
                self.mainData[int(key)] = text
            # self.mainData = value
            for i in value:
                self.update_data_on_main_window(value[i], True)
            
        
        self.close()
    def search_by_sequence(self, names_dict, sequence):
        matching_names = []

        for key, name in names_dict.items():
            if sequence.lower() in name.lower():
                matching_names.append(key)

        return matching_names

    
    def searchFucn(self):
        data = {}

        for i in self.widgetsList:
            i.frameBorder.setVisible(False)

        for i in self.widgetsList:
            data[i.number] = f"{i.label_FIO.text()}"


        search_result = self.search_by_sequence(data, self.ui.lineEdit.text())

        for i in self.widgetsList:
            if i.number in search_result:
                i.frameBorder.setVisible(True)
            else:
                i.frameBorder.setVisible(False)


    def changeData(self, value):
        newData = self.edit_inf.data

        start = {}
        end = {}


        for i in newData['start_healingPhotos']:
            start[i] = newData['start_healingPhotos'][i]
        for i in newData['end_healingPhotos']:
            end[i] = newData['end_healingPhotos'][i]


        if newData['img'] == 'none':
            newData['img'] = self.mainData[value]['img']
        # if len(newData['other_images']) != 0:
        #     newData['other_images'] = newData['other_images']
            
        if newData['doc_files'] == "":
            newData['doc_files'] = self.mainData[value]['doc_files']

        if len(start) != 0:
            newData['start_healingPhotos'] = start
        if len(end) != 0:
            newData['end_healingPhotos'] = end
            

        self.edit_inf.data = {} #Clear previous note
        self.mainData[value] = newData
        
        self.widgetsList[value].label_FIO.setText(newData['FIO'])
        self.widgetsList[value].label_Inf.setText(newData['inf'])
        self.widgetsList[value].date.setText(newData['date_of_birth'])
        self.widgetsList[value].number = value


        current_style_photo = self.widgetsList[value].label_Photo.styleSheet()
        pattern = r"border-image: url\((.*?)\);"
        css_string_updated = re.sub(pattern, f"border-image: url({newData['img']});", current_style_photo)
        self.widgetsList[value].label_Photo.setStyleSheet(css_string_updated)

        self.back_to_main_window()

    def edit_users_information(self, ev, value):############################################################################
        num = value - 1
        self.edit_inf = AddUserWindow()

        self.edit_inf.show()

        self.edit_inf.add_form_btn.clicked.connect(lambda: self.changeData(num))
        self.edit_inf.cancel_page.clicked.connect(self.cancel_data_btn)
        self.edit_inf.cancel_page_2.clicked.connect(self.cancel_data_btn)
        self.edit_inf.cancel_page_3.clicked.connect(self.cancel_data_btn)
        self.edit_inf.cancel_page_4.clicked.connect(self.cancel_data_btn)

        self.edit_inf.fio_line.setText(self.mainData[num]['FIO'])
        self.edit_inf.year_oldLine.setText(self.mainData[num]['years_old'])
        self.edit_inf.dateLine.setText(self.mainData[num]['date_of_birth'])
        self.edit_inf.textEdit.setText(self.mainData[num]['inf'])
        self.edit_inf.place.setText(self.mainData[num]['place'])
        self.edit_inf.doctor_name.setText(self.mainData[num]['doctor_name'])

        if self.mainData[num]['img'] != 'none':
            current_style_photo = self.edit_inf.photoScreen.styleSheet()
            self.edit_inf.photoScreen.setText("")
            self.edit_inf.photoScreen.setStyleSheet(current_style_photo[:-1] + f'border-image: url({self.mainData[num]['img']}) 0 0 0 0;\n'  \
                + "padding-left: 130px;" + 'background: #464646;' + "}")
        if self.mainData[num]['img'] == 'delete':
            print("DELETER")
            self.edit_inf.photoScreen.setStyleSheet(self.edit_inf.current_style_photo)
            self.edit_inf.photoScreen.setText("+")
            
        if self.mainData[num]['doc_files'] != '':
            self.edit_inf.docFileList.clear()
            item = QListWidgetItem(self.mainData[num]['doc_files'], self.edit_inf.docFileList)
            icon = QIcon('img\\word_icon.png')
            item.setIcon(icon)
            
            self.edit_inf.docFileList.addItem(item)

        if len(self.mainData[num]['other_images']) > 0:
            for i in range(self.edit_inf.otherPhotosList.count()):
                widget = self.edit_inf.otherPhotosList.widget(i)
                if widget is not None:
                    self.edit_inf.otherPhotosList.removeWidget(widget)
                    widget.deleteLater()
        
            self.edit_inf.otherPhotosList.setCurrentIndex(0)
            for i in self.mainData[num]['other_images']:
                layout = QVBoxLayout() #create Layout

                image = QLabel()#create label for img
                image.setStyleSheet(f"border-image: url({i});\n")
                image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
                layout.addWidget(image)

                text = QLabel(i) #set text with photo_path varible
                self.edit_inf.data['other_images'].append(i)
                text.setStyleSheet(f"font-size: 10px;")
                layout.addWidget(text)

                widget = QWidget() #set widget for adding img and text to it
                widget.setLayout(layout)
                widget.setGeometry(0, 0, 0, 0)

                self.edit_inf.otherPhotosList.addWidget(widget) # add widget
                self.edit_inf.otherPhotosList.setCurrentWidget(widget)
                self.edit_inf.listCount.setText(f"№{self.edit_inf.otherPhotosList.currentIndex()}")


        if len(self.mainData[num]['healingList']) > 0: ########################## new
            for i in self.mainData[num]['healingList']:################################
                item = QListWidgetItem(i)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.edit_inf.listWidget.addItem(item)

        if self.mainData[num]['start_healingPhotos'] != {}:
            for key in self.mainData[num]['start_healingPhotos']:
                item = QListWidgetItem(self.mainData[num]['start_healingPhotos'][key])
                icon = QIcon("AppData\\Roaming\\ListIMG\\" + key)
                item.setIcon(icon)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.edit_inf.imageWidget.addItem(item)
                self.edit_inf.data['start_healingPhotos'][key] = ""
            
        if self.mainData[num]['end_healingPhotos'] != {}:
            for key in self.mainData[num]['end_healingPhotos']:
                print(key)
                item = QListWidgetItem(self.mainData[num]['end_healingPhotos'][key])
                icon = QIcon("AppData\\Roaming\\ListIMG\\" + key)
                item.setIcon(icon)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.edit_inf.listWidget_end.addItem(item)
                self.edit_inf.data['end_healingPhotos'][key] = ""

        self.close()
    #######################################################################################################

    def show_current_user_inf(self, event, value):
        self.show_page = show_page()
        self.show_page.show()
        self.show_page.goBack_btn.clicked.connect(self.back_to_main_window)
        self.show_page.goBack_btn2.clicked.connect(self.back_to_main_window)
        self.show_page.goBack_btn3.clicked.connect(self.back_to_main_window)
        self.show_page.goBack_btn4.clicked.connect(self.back_to_main_window)

        num = value - 1
        
        self.show_page.FIO.setText(self.mainData[num]['FIO'])
        self.show_page.years_old.setText(self.mainData[num]['years_old'])
        self.show_page.birthDate.setText(self.mainData[num]['date_of_birth'])
        self.show_page.inf.setText(self.mainData[num]['inf'])
        self.show_page.place.setText(self.mainData[num]['place'])
        self.show_page.doctor_name.setText(self.mainData[num]['doctor_name'])
        
        if self.mainData[num]['img'] != 'none':
            current_style_photo = self.show_page.photo.styleSheet()
            self.show_page.photo.setStyleSheet(current_style_photo[:-1] + f'border-image: url({self.mainData[num]['img']}) 0 0 0 0;\n'  \
                + "padding-left: 130px;" + 'background: #464646;' + "}")
        if self.mainData[num]['img'] == 'delete':
            print("DELETER")
            self.show_page.photo.setStyleSheet(self.edit_inf.current_style_photo)
            self.show_page.photo.setText("+")
            
        if self.mainData[num]['doc_files'] != '':
            self.show_page.doc_list.clear()
            item = QListWidgetItem(self.mainData[num]['doc_files'], self.show_page.doc_list)
            icon = QIcon('img\\word_icon.png')
            item.setIcon(icon)

            self.show_page.doc_list.addItem(item)
        if len(self.mainData[num]['other_images']) > 0:
            for i in range(self.show_page.Addictional.count()):
                widget = self.show_page.Addictional.widget(i)
                if widget is not None:
                    self.show_page.Addictional.removeWidget(widget)
                    widget.deleteLater()
        
            self.show_page.Addictional.setCurrentIndex(-1)
            for i in self.mainData[num]['other_images']:
                layout = QVBoxLayout() #create Layout

                image = QLabel()#create label for img
                image.setStyleSheet(f"border-image: url({i});\n margin-left: 100%;\n margin-right: 100%;")
                image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
                layout.addWidget(image)

                text = QLabel(i) #set text with photo_path varible
                text.setStyleSheet(f"font-size: 10px;")
                layout.addWidget(text)

                widget = QWidget() #set widget for adding img and text to it
                widget.setLayout(layout)

                self.show_page.Addictional.addWidget(widget) # add widget
                self.show_page.Addictional.setCurrentWidget(widget)
                self.show_page.listCount.setText(f"№{self.show_page.Addictional.currentIndex()}")
                # print(self.show_page.Addictional.currentIndex())
        
        if len(self.mainData[num]['healingList']) > 0: ########################## new
            for i in self.mainData[num]['healingList']:################################
                item = QListWidgetItem(i)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.show_page.listWidget.addItem(item)

        if self.mainData[num]['start_healingPhotos'] != {}:
            for key in self.mainData[num]['start_healingPhotos']:
                print(key)
                item = QListWidgetItem(self.mainData[num]['start_healingPhotos'][key])
                icon = QIcon("AppData\\Roaming\\ListIMG\\" + key)
                item.setIcon(icon)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.show_page.imageWidget.addItem(item)

        if self.mainData[num]['end_healingPhotos'] != {}:
            for key in self.mainData[num]['end_healingPhotos']:
                print(key)
                item = QListWidgetItem(self.mainData[num]['end_healingPhotos'][key])
                icon = QIcon("AppData\\Roaming\\ListIMG\\" + key)
                item.setIcon(icon)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.show_page.listWidget_3.addItem(item)
                


        self.close()
    
    def show_add_user_screen(self):
        self.add_user_window = AddUserWindow()
        self.add_user_window.show()
        self.add_user_window.add_form_btn.clicked.connect(self.update_data_on_main_window)
        self.add_user_window.cancel_page.clicked.connect(self.cancel_data_btn)
        self.add_user_window.cancel_page_2.clicked.connect(self.cancel_data_btn)
        self.add_user_window.cancel_page_3.clicked.connect(self.cancel_data_btn)
        self.add_user_window.cancel_page_4.clicked.connect(self.cancel_data_btn)
        
        self.close()
    def cancel_data_btn(self):
        print('CANCELLED')
        self.back_to_main_window()

    def back_to_main_window(self):
        self.add_user_window.close()
        self.show_page.close()
        self.edit_inf.close()
        self.show()

    def update_data_on_main_window(self, otherData="", value=False):
        if not value:
            self.data = self.add_user_window.data
            self.mainData[self.list_count] = self.data
        else:
            self.data = otherData

        data_widget = MainWindowWidgets()

        self.list_count += 1

        data_widget.frameBorder = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        data_widget.frameBorder.setStyleSheet(
        "#frameBorder{\n"
        "padding: 0px;\n"
        "background-color: rgb(101, 199, 198);\n"
        "border-radius: 20px;\n"
        "margin-bottom: 10px;\n"
        "}\n"
        "\n"
        "\n"
        "")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(data_widget.frameBorder.sizePolicy().hasHeightForWidth())

        data_widget.frameBorder.setSizePolicy(sizePolicy)
        data_widget.frameBorder.setMinimumSize(QtCore.QSize(0, 184))
        data_widget.frameBorder.setFrameShape(QtWidgets.QFrame.StyledPanel)
        data_widget.frameBorder.setFrameShadow(QtWidgets.QFrame.Raised)
        data_widget.frameBorder.setObjectName("frameBorder")

        verticalLayout_2 = QtWidgets.QVBoxLayout(data_widget.frameBorder)
        verticalLayout_2.setContentsMargins(0, 15, 0, 0)
        verticalLayout_2.setObjectName("verticalLayout_2")

        personInf = QtWidgets.QFrame(data_widget.frameBorder)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(personInf.sizePolicy().hasHeightForWidth())

        personInf.setSizePolicy(sizePolicy)
        personInf.setStyleSheet(
        "QFrame {\n"
        "padding: 0px;\n"
        "    border: 2px solid  rgb(101, 199, 198);\n"
        "    border-radius: 20px;\n"
        "    background:white;\n"
        "}\n"
        "QLabel{\n"
        "border: none;\n"
        "}")
        personInf.setObjectName("personInf_2")
        
        personGrid = QtWidgets.QGridLayout(personInf)
        personGrid.setObjectName("personGrid_3")

        label_AddBtn = QtWidgets.QLabel(personInf)
        label_AddBtn.setStyleSheet(
        "QLabel{\n"
        "font-size: 40px;\n"
        "background-image: url(img/magnifying-glass.png);\n"
        "background-repeat: no-repeat;\n"
        "background-position: center;\n"
        "}\n"
        "QLabel{\n"
        "font-size: 40px;\n"
        "}\n"
        "QLabel:hover{\n"
        "border: 2px dashed  rgb(101, 199, 198);\n"
        "color: rgb(101, 199, 198);\n"
        "}")
        label_AddBtn.setAlignment(QtCore.Qt.AlignCenter)
        label_AddBtn.setObjectName("label_AddBtn")

        label_AddBtn.mousePressEvent = lambda event, num=self.list_count: self.show_current_user_inf(event, num)


        personGrid.addWidget(label_AddBtn, 0, 3, 3, 1)

        data_widget.label_Photo = QtWidgets.QLabel(personInf)
        data_widget.label_Photo.setMaximumSize(QtCore.QSize(120, 16777215))
        data_widget.label_Photo.setStyleSheet(
        "padding: 40px;\n"
        "padding-left: 65px;\n"
        "padding-right: 65px;\n"
        "border: 1px solid black;\n"
        "border-radius: 48px;\n"
        f"border-image: url({self.data['img']});\n"
        "")
        data_widget.label_Photo.setText("")
        data_widget.label_Photo.setObjectName("label_Photo_2")
        data_widget.label_Photo.setMinimumWidth(120)
        data_widget.label_Photo.setMaximumWidth(120)

        data_widget.label_Photo.setMinimumHeight(100)
        data_widget.label_Photo.setMaximumHeight(100)

        personGrid.addWidget(data_widget.label_Photo, 1, 1, 1, 1)

        data_widget.label_Inf = QtWidgets.QLabel(personInf)
        data_widget.label_Inf.setMaximumWidth(284)
        data_widget.label_Inf.setMinimumHeight(0)

        data_widget.label_Inf.setMaximumHeight(102)
        data_widget.label_Inf.setMinimumWidth(0)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(data_widget.label_Inf.sizePolicy().hasHeightForWidth())

        data_widget.label_Inf.setSizePolicy(sizePolicy)
        data_widget.label_Inf.setTextFormat(QtCore.Qt.AutoText)
        data_widget.label_Inf.setScaledContents(False)
        data_widget.label_Inf.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        data_widget.label_Inf.setWordWrap(True)
        data_widget.label_Inf.setObjectName("label_Inf_2")

        personGrid.addWidget(data_widget.label_Inf, 0, 2, 2, 1)
        data_widget.label_FIO = QtWidgets.QLabel(personInf)
        data_widget.label_FIO.setStyleSheet("font-size: 15px;")
        data_widget.label_FIO.setObjectName("label_FIO_2")

        personGrid.addWidget(data_widget.label_FIO, 2, 1, 1, 2)

        data_widget.date = QtWidgets.QLabel(personInf)
        data_widget.date.setStyleSheet("font-size: 20px;")
        data_widget.date.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        data_widget.date.setObjectName("label_Date_2")

        personGrid.addWidget(data_widget.date, 3, 1, 1, 2)

        changeInf = QtWidgets.QPushButton(personInf)
        changeInf.mousePressEvent = lambda event, num=self.list_count: self.edit_users_information(event, num)
        changeInf.setStyleSheet(
        "QPushButton{\n"
        "border: 2px solid rgb(101, 199, 198);\n"
        "background: rgb(101, 199, 198);\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "color: rgb(240, 249, 248);\n"
        "}\n"
        "QPushButton:hover{\n"
        "border: 2px dashed  rgb(101, 199, 198);\n"
        "color: rgb(101, 199, 198);\n"
        "background: rgb(240, 249, 248);\n"
        "}")
        changeInf.setObjectName("changeInf_2")
        personGrid.addWidget(changeInf, 3, 3, 1, 1)

        Number = QtWidgets.QLabel(personInf)
        Number.setMaximumSize(QtCore.QSize(20, 16777215))
        Number.setSizeIncrement(QtCore.QSize(20, 0))
        Number.setStyleSheet('font-size: 10px;')
        Number.setObjectName("Number_2")

        personGrid.addWidget(Number, 1, 0, 3, 1)

        verticalLayout_2.addWidget(personInf)
        self.ui.verticalLayout.addWidget(data_widget.frameBorder)

        data_widget.label_Inf.setText(self.data['inf'])
        data_widget.label_FIO.setText(self.data['FIO'])
        data_widget.date.setText(self.data['date_of_birth'])
        changeInf.setText("Редагувати")
        Number.setText(f"#{self.list_count}")
        
        data_widget.number = self.list_count
        self.widgetsList.append(data_widget)

        self.back_to_main_window()
    def program_quit(self):
        # settings = QSettings('Colos', 'DataBaseApp')
        # settings.setValue('user_data', self.mainData)
        # print(self.mainData)
        # settings.sync()
        with open('my_dict.json', 'w') as file:
            json.dump(self.mainData, file)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    app.aboutToQuit.connect(main_window.program_quit)
    main_window.show()
    sys.exit(app.exec_())