import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
import sip

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Test_GUI_2.ui")[0]

class Form(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # self.init_ui()
        self.setupUi(self)
        
        self.btn_move_to_right:QPushButton
        self.btn_move_to_left:QPushButton
        self.select_list:QTreeWidget
        self.selected_list:QTreeWidget

        self.select_list.setSortingEnabled(True)
        self.select_list.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.selected_list.setSortingEnabled(True)
        self.selected_list.sortByColumn(0, QtCore.Qt.AscendingOrder)
        
        # 시그널 설정
        self.btn_move_to_right.clicked.connect(self.move_item)
        self.btn_move_to_left.clicked.connect(self.move_item)

    def add_child_all(parent, item, child_Count):
        for n in range(0, child_Count):
            new_item = QTreeWidgetItem(parent)
            new_item.setText(0, item.child(n).text(0))

            new_child_Count = item.child(n).childCount()
            if new_child_Count != 0:
                Form.add_child_all(new_item, item.child(n), new_child_Count)

    # 아이템 이동
    def move_item(self):
        sender = self.sender()
        if self.btn_move_to_right == sender:
            source_tw = self.select_list
            target_tw = self.selected_list
        else:
            source_tw = self.selected_list
            target_tw = self.select_list
        
        # 현재 선택된 아이템을 꺼내어 반대편 쪽으로 전달
        item = source_tw.currentItem()
        parent_item = item.parent()
        
        # Parent를 선택 이동하는 경우
        if item.parent() == None:
            # Parent를 선택 이동하는데, parent가 존재하지 않는 경우
            if target_tw.topLevelItemCount() == 0:
                source = QTreeWidget.invisibleRootItem(source_tw)
                source.removeChild(item)
                root = QTreeWidget.invisibleRootItem(target_tw)
                root.addChild(item)
            # Parent를 선택 이동하는데, parnet가 존재하는 경우
            else:
                # Parent를 선택 이동하는데, 동일한 parent가 있는 경우
                for n in range(0, target_tw.topLevelItemCount()):
                    if target_tw.topLevelItem(n).text(0) == item.text(0):
                        current_pos = target_tw.topLevelItem(n)
                        for i in range(0, item.childCount()):
                            new_item = QTreeWidgetItem(current_pos)
                            new_item.setText(0, item.child(i).text(0))
                            new_item.setText(1, item.child(i).text(1))
                        source = QTreeWidget.invisibleRootItem(source_tw)
                        source.removeChild(item)
                        break
                    # Parent를 선택 이동하는데, 동일한 parent가 없는 경우
                    else:
                        source = QTreeWidget.invisibleRootItem(source_tw)
                        source.removeChild(item)
                        root = QTreeWidget.invisibleRootItem(target_tw)
                        root.addChild(item)

        
        # Sub Child가 없는 child를 선택 이동하는 경우
        elif item.childCount() == 0:
            add_item_list = []
            add_item = item

            # 선택한 item을 저장
            children = []
            for child in range(item.parent().childCount()):
                if item.parent().child(child) == item:
                    children.append(item.parent().child(child))

            # select_item이 child 유무 확인
            extra_item = QTreeWidgetItem()
            if item.childCount() != 0:
                extra_item = item

            while(1):
                add_item_list.append(add_item.text(0))
                add_item_list.append(add_item.text(1))

                add_item = add_item.parent()
                if add_item == None:
                    break
            
            # 조상이 Right에 존재하는지 확인
            current_pos = QTreeWidgetItem() #current_item.text(0) == ""
            for n in range(0, target_tw.topLevelItemCount()):
                if target_tw.topLevelItem(n).text(1) == add_item_list[len(add_item_list)-1]:
                    current_pos = target_tw.topLevelItem(n)
                    break
            
            # First parent가 존재하지 않는 경우
            if current_pos.text(0) == "":
                new_item = QTreeWidgetItem(target_tw)
                item_cnt = len(add_item_list)
                new_item.setText(0, add_item_list.pop(item_cnt - 2))
                new_item.setText(1, add_item_list.pop(item_cnt - 2))
                item_cnt -= 2

                # Selected list에 추가하고 선택한 item을 select list에서 삭제
                for child in children:
                    item.parent().removeChild(child)

                    # Parent에 child가 존재하지 않는 경우, parenet 삭제
                    if parent_item.childCount() == 0:
                        sip.delete(parent_item)

                while(1):
                    # child 추가
                    new_item = QTreeWidgetItem(new_item)
                    new_item.setText(0, add_item_list.pop(item_cnt - 2))
                    new_item.setText(1, add_item_list.pop(item_cnt - 2))
                    item_cnt -= 2

                    if len(add_item_list) == 0:
                        # selected item(child)이 child를 가진 경우
                        if extra_item.text(0) != "":
                            new_child_Count = extra_item.childCount()
                            Form.add_child_all(new_item,extra_item,new_child_Count)
                        break
            # First parent가 존재하는 경우
            else:
                first_parent = parent_item.parent()
                for n in range(0, target_tw.topLevelItemCount()):
                    # Selected list에서 선택한 chlid의 parent 찾기
                    if target_tw.topLevelItem(n).text(0) == current_pos.text(0):
                        item_cnt = len(add_item_list)
                        add_item_list.pop(item_cnt - 2)
                        add_item_list.pop(item_cnt - 2)
                        item_cnt -= 2

                # Second parnet가 존재하는지 확인    
                if len(item.text(0).split('.')) > 2:
                    # Selected list에서 선택한 child의 second parent 찾기
                    for n in range(0, current_pos.childCount()):
                        # Second parent가 있으면 add_item_list에서 삭제
                        if len(add_item_list) > 0:
                            if current_pos.child(n).text(1) == add_item_list[item_cnt-1]:
                                new_item = QTreeWidgetItem(current_pos.child(n))
                                add_item_list.pop(item_cnt - 2)
                                add_item_list.pop(item_cnt - 2)
                                item_cnt -= 2

                                # child 추가
                                new_item.setText(0, add_item_list.pop(item_cnt - 2))
                                new_item.setText(1, add_item_list.pop(item_cnt - 2))

                    # Second parent가 없으면 추가
                    if item_cnt > 3:
                        new_item = QTreeWidgetItem(current_pos)
                        new_item.setText(0, add_item_list.pop(item_cnt - 2))
                        new_item.setText(1, add_item_list.pop(item_cnt - 2))
                        item_cnt -= 2

                        # child 추가
                        sub_item = QTreeWidgetItem()
                        sub_item.setText(0, add_item_list.pop(item_cnt - 2))
                        sub_item.setText(1, add_item_list.pop(item_cnt - 2))
                        new_item.addChild(sub_item)
                else:
                # child 추가
                    new_item = QTreeWidgetItem(current_pos)
                    new_item.setText(0, add_item_list.pop(item_cnt - 2))
                    new_item.setText(1, add_item_list.pop(item_cnt - 2))

                # Selected list에 추가하고 선택한 item을 select list에서 삭제
                for child in children:
                    item.parent().removeChild(child)

                    # Parent에 child가 존재하지 않는 경우, parenet 삭제
                    if parent_item.childCount() == 0:
                        sip.delete(parent_item)
                        # First parent에 second parent가 존재하지 않을 경우, first parent 삭제
                        try:
                            if first_parent.childCount() == 0:
                                sip.delete(first_parent)                                                    
                        except:
                            pass
                
                # if len(add_item_list) == 0:
                #     # selected item이 child를 가진 경우
                #     if extra_item.text(0) != "":
                #         new_child_Count = extra_item.childCount()
                #         Form.add_child_all(new_item,extra_item,new_child_Count)
                #     break
        # Sub Child가 있는 child를 선택 이동하는 경우
        else:
            add_item_list = []
            add_item = item

            # 선택한 item을 저장
            children = []
            for child in range(item.parent().childCount()):
                if item.parent().child(child) == item:
                    children.append(item.parent().child(child))
            
            # 선택한 child의 Sub child list 저장
            new_child_Count = add_item.childCount()
            for n in range(0, new_child_Count):
                add_item_list.append(add_item.child(n).text(0))
                add_item_list.append(add_item.child(n).text(1))
            
            add_item_list.append(add_item.text(0))
            add_item_list.append(add_item.text(1))

            # Parent 저장
            while(1):
                add_item = add_item.parent()
                if add_item != None:
                    add_item_list.append(add_item.text(0))
                    add_item_list.append(add_item.text(1))
                else:
                    break

            # Selected list에 선택한 item의 parent가 존재하는지 확인
            current_pos = QTreeWidgetItem() 
            for n in range(0, target_tw.topLevelItemCount()):
                if target_tw.topLevelItem(n).text(1) == add_item_list[len(add_item_list)-1]:
                    current_pos = target_tw.topLevelItem(n)
                    break

            # Selected list에 선택한 item의 parent가 존재하지 않는 경우
            # First parent 추가
            cnt = len(add_item_list)
            if current_pos.text(0) == "":
                new_item = QTreeWidgetItem(target_tw)
                new_item.setText(0, add_item_list.pop(cnt-2))
                new_item.setText(1, add_item_list.pop(cnt-2))
                cnt -= 2

                # Second parent 추가
                if cnt > new_child_Count*2:
                    new_item = QTreeWidgetItem(new_item)
                    new_item.setText(0, add_item_list.pop(cnt-2))
                    new_item.setText(1, add_item_list.pop(cnt-2))

                # Selected list에 추가하고 선택한 item을 select list에서 삭제
                for child in children:
                    item.parent().removeChild(child)

                    # Parent에 child가 존재하지 않는 경우, parenet 삭제
                    if parent_item.childCount() == 0:
                        sip.delete(parent_item)

                # Child 추가            
                if len(add_item_list) > 0:
                    while len(add_item_list) > 0:
                        sub_item = QTreeWidgetItem()
                        sub_item.setText(0, add_item_list.pop(0))
                        sub_item.setText(1, add_item_list.pop(0))
                        new_item.addChild(sub_item)
            # Selected list에 선택한 item의 parent가 존재하는 경우
            else:
                if target_tw.topLevelItem(n).text(0) == current_pos.text(0):
                    new_item = QTreeWidgetItem(current_pos)
                    add_item_list.pop(cnt-2)
                    add_item_list.pop(cnt-2)
                    cnt -= 2

                # Second parent 추가
                new_item.setText(0, add_item_list.pop(cnt-2))
                new_item.setText(1, add_item_list.pop(cnt-2))

                # Child 추가            
                if len(add_item_list) > 0:
                    while len(add_item_list) > 0:
                        sub_item = QTreeWidgetItem()
                        sub_item.setText(0, add_item_list.pop(0))
                        sub_item.setText(1, add_item_list.pop(0))
                        new_item.addChild(sub_item)
                
                # Selected list에 추가하고 선택한 item을 select list에서 삭제
                for child in children:
                    item.parent().removeChild(child)

                    # Parent에 child가 존재하지 않는 경우, parenet 삭제
                    if parent_item.childCount() == 0:
                        sip.delete(parent_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())