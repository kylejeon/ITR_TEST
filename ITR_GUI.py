# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
#form_class = uic.loadUiType("untitled.ui")[0]
form_class = uic.loadUiType("Test_GUI.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # > Click
        self.pushButton_11.clicked.connect(self.One_Right)


    def add_child_all(parent, item, child_Count):
        for n in range(0, child_Count):
            new_item = QTreeWidgetItem(parent)
            new_item.setText(0, item.child(n).text(0))

            new_child_Count = item.child(n).childCount()
            if new_child_Count != 0:
                WindowClass.add_child_all(new_item, item.child(n), new_child_Count)

    def One_Right(self):
        # Right
        Widget = self.treeWidget_4

        select_item = self.treeWidget_3.currentItem()

        # select_item top check
        if select_item.parent() == None:
            # select_item already exist check in Right
            check = False
            for n in range(0, Widget.topLevelItemCount()):
                if Widget.topLevelItem(n).text(0) == select_item.text(0):
                    check = True
                    ##### except in Right / + new_item
                  
            # select_item not in Right
            if check == False:
                new_item = QTreeWidgetItem(self.treeWidget_4)
                new_item.setText(0, select_item.text(0))

                child_Count = select_item.childCount()
                if child_Count != 0:
                    WindowClass.add_child_all(new_item, select_item, child_Count)

        else:
            # 추가할 대상을 찾아 경로 list화
            add_item_list = []
            add_item = select_item
            
            # select_item이 child 유무 확인
            extra_item = QTreeWidgetItem()
            if select_item.childCount() != 0:
                extra_item = select_item

            while(1):
                add_item_list.append(add_item.text(0))
                add_item = add_item.parent()
                if add_item == None:
                    break

            # 조상이 Right에 존재하는지 확인
            current_pos = QTreeWidgetItem() #current_item.text(0) == ""
            for n in range(0, Widget.topLevelItemCount()):
                if Widget.topLevelItem(n).text(0) == add_item_list[len(add_item_list)-1]:
                    current_pos = Widget.topLevelItem(n)
                    break
            
            # 존재 X 경우
            if current_pos.text(0) == "":
                new_item = QTreeWidgetItem(self.treeWidget_4)
                new_item.setText(0, add_item_list.pop())
                while(1):
                    new_item = QTreeWidgetItem(new_item)
                    new_item.setText(0, add_item_list.pop())
                    if len(add_item_list) == 0:
                        # selected item이 child를 가진 경우
                        if extra_item.text(0) != "":
                            new_child_Count = extra_item.childCount()
                            WindowClass.add_child_all(new_item,extra_item,new_child_Count)
                        break
            # 존재 O 경우
            else:
                pass



            #while(1):
            #    check_item = add_item_list.pop()

            #    WindowClass.list_check_add(current_pos, check_item)

            #    if len(add_item_list) == 0:
            #        break




            ## parent already exist check in Right
            #check = False
            #for n in range(0, Widget.topLevelItemCount()):
            #    if Widget.topLevelItem(n).text(0) == parent.text(0):
            #        check = True
            #        ##### except in Right / + new_item


            ## parent not in Right
            #if check == False:
            #    new_item = QTreeWidgetItem(self.treeWidget_4)
            #    new_item.setText(0, parent.text(0))

            #    sub_item = QTreeWidgetItem(new_item)
            #    sub_item.setText(0, select_item.text(0))


        ## Expand Add List (Right) 수정필요
        #for n in range(0, Widget.topLevelItemCount()):
        #    if Widget.topLevelItem(n).text(0) == select_item.text(0):
        #        Widget.expandItem(Widget.topLevelItem(n))
        #        break

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
