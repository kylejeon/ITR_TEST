import sys, time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool
import sip
import re
import Main
import Common_Var
from ITR_Admin_Common import launch_webdriver

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Test_GUI.ui")[0]
font = QFont()
font.setBold(True)

# Thread 생성
class Thread1(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
    def __del__(self):
        self.wait()
    def run(self):
        Main.Test.function_test(testcase_list)

class Thread2(QThread):
    timer = pyqtSignal(str)
    running = False
    times = 0.0
    def run(self):
        while True:
            if self.running:
                self.times += 0.01
                self.timer.emit(self.convert(self.times))
            time.sleep(0.01)
    def convert(self, times):
        Second = str(times).split('.')[0]
        Hours = str(int((int(Second) / 60) / 60)).zfill(2)
        Minutes = str(int((int(Second) / 60) % 60)).zfill(2)
        Seconds = str(int(int(Second) % 60)).zfill(2)
        return '%s:%s:%s'%(Hours,Minutes,Seconds)

class UpdateTableSignal(QObject):
    signal = pyqtSignal(str, str, str, str, str)

    def run(self):
        self.signal.emit(str(Common_Var.tc_name), str(Common_Var.run_status), str(Common_Var.tc_steps), str(Common_Var.defects), str(Common_Var.runtime))

class UpdatePassSignal(QObject):
    signal = pyqtSignal()

    def run(self):
        self.signal.emit()

class UpdateFailSignal(QObject):
    signal = pyqtSignal()

    def run(self):
        self.signal.emit()

class UpdateExceptionSignal(QObject):
    signal = pyqtSignal()

    def run(self):
        self.signal.emit()

class Form(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread_manager = QThreadPool()

        QApplication.processEvents()
        self.btn_move_to_right:QPushButton
        self.btn_move_to_left:QPushButton
        self.btn_select_all:QPushButton
        self.btn_deselect_all:QPushButton
        self.select_list:QTreeWidget
        self.selected_list:QTreeWidget
        self.text_planid:QLineEdit
        self.text_bn:QLineEdit
        self.btn_run_test:QTreeWidget
        self.btn_close:QTreeWidget
        self.tableWidget:QTableWidget
        self.label_testcase:QLabel
        self.label_passed:QLabel
        self.label_failed:QLabel
        self.label_notexecuted:QLabel
        self.label_exception:QLabel
        self.label_executed:QLabel
        self.progressBar:QProgressBar
        self.label_3:QLabel
        self.label_4:QLabel
        self.label_6:QLabel
        self.noTestlink:QRadioButton
        self.Testlink:QRadioButton
        self.comboBox_browser:QComboBox
        self.label_time:QLabel
        self.label_admin_url:QLineEdit
        self.label_worklist_url:QLineEdit
        self.comboBox_server:QComboBox

        # self.select_list.setSortingEnabled(True)
        # self.select_list.sortByColumn(0, Qt.AscendingOrder)
        # self.selected_list.setSortingEnabled(True)
        # self.selected_list.sortByColumn(0, Qt.AscendingOrder)
        
        # TestPlan ID, BN No., admin_url, worklist_url 레이블 비활성화
        self.text_planid.setDisabled(True)
        self.text_bn.setDisabled(True)
        self.label_admin_url.setDisabled(True)
        self.label_worklist_url.setDisabled(True)
        
        # 시그널 설정
        self.btn_move_to_right.clicked.connect(self.move_item)
        self.btn_move_to_left.clicked.connect(self.move_item)
        self.btn_run_test.clicked.connect(self.run_test)
        self.btn_run_test.clicked.connect(self.start_timer)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)
        self.noTestlink.clicked.connect(self.update_testlink)
        self.Testlink.clicked.connect(self.update_testlink)
        self.comboBox_server.activated[str].connect(self.change_server)     
        self.comboBox_browser.activated[str].connect(self.change_browser)     

        self.thread2 = Thread2()
        self.thread2.timer.connect(self.label_time.setText)
        self.thread2.start()

    def __lt__(self, other):
        column1 = self.select_list.sortColumn()
        column2 = self.selected_list.sortColumn()
        if column1 == 0:
            key1 = self.text(column1)
            key2 = other.text(column1)
            return self.natural_sort_key(key1) < self.natural_sort_key(key2)
        if column2 == 0:
            key3 = self.text(column2)
            key4 = other.text(column2)
            return self.natural_sort_key(key3) < self.natural_sort_key(key4)

    @staticmethod
    def natural_sort_key(key):
        regex = '(\d*\.\d+|\d+)'
        parts = re.split(regex, key)
        return tuple((e if i % 2 == 0 else float(e)) for i, e in enumerate(parts))

    @pyqtSlot(str, str, str, str, str)
    def signal_update_table(self, arg1, arg2, arg3, arg4, arg5):
        Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 0, QTableWidgetItem(str(arg1)))
        if QTableWidgetItem(str(arg2)).text() == "Failed":
            Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 1, QTableWidgetItem(str(arg2)))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setBackground(QtGui.QColor(191,38,0))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setForeground(QtGui.QColor(255,255,255))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setTextAlignment(Qt.AlignCenter)
        else:
            Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 1, QTableWidgetItem(str(arg2)))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setBackground(QtGui.QColor(0,135,90))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setForeground(QtGui.QColor(255,255,255))
            Common_Var.form.tableWidget.item(Common_Var.rowIndex, 1).setTextAlignment(Qt.AlignCenter)
        Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 2, QTableWidgetItem(str(arg3)))
        Common_Var.form.tableWidget.item(Common_Var.rowIndex, 2).setTextAlignment(Qt.AlignCenter)
        Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 3, QTableWidgetItem(str(arg4)))
        Common_Var.form.tableWidget.item(Common_Var.rowIndex, 3).setTextAlignment(Qt.AlignCenter)
        Common_Var.form.tableWidget.setItem(Common_Var.rowIndex, 4, QTableWidgetItem(str(arg5)))
        Common_Var.form.tableWidget.item(Common_Var.rowIndex, 4).setTextAlignment(Qt.AlignCenter)
        QApplication.processEvents()
        Common_Var.form.tableWidget.resizeRowsToContents()
        Common_Var.rowIndex += 1

    pyqtSlot()
    def signal_pass(self):
        Common_Var.test_status_passed += 1
        Common_Var.test_status_notexecuted -= 1
        Common_Var.form.label_passed.setText(str(Common_Var.test_status_passed))
        Common_Var.form.label_notexecuted.setText(str(Common_Var.test_status_notexecuted))
        self.progressBar.setValue(int(Common_Var.progress_bar))
        Common_Var.form.label_executed.setText(str(Common_Var.executed) + "% executed")
    
    pyqtSlot()
    def signal_fail(self):
        Common_Var.test_status_failed += 1
        Common_Var.test_status_notexecuted -= 1
        Common_Var.form.label_passed.setText(str(Common_Var.test_status_failed))
        Common_Var.form.label_notexecuted.setText(str(Common_Var.test_status_notexecuted))
        self.progressBar.setValue(int(Common_Var.progress_bar))
        Common_Var.form.label_executed.setText(str(Common_Var.executed) + "% executed")
    
    pyqtSlot()
    def signal_exception(self):
        Common_Var.test_status_exception -= 1
        Common_Var.form.label_exception.setText(str(Common_Var.test_status_exception))
        self.progressBar.setValue(int(Common_Var.progress_bar))
        Common_Var.form.label_executed.setText(str(Common_Var.executed) + "% executed")

    def update_testlink(self):
        if self.noTestlink.isChecked() == True:
            self.text_planid.setDisabled(True)
            self.text_bn.setDisabled(True)
        else:
            self.text_planid.setEnabled(True)
            self.text_bn.setEnabled(True)

    def set_testlink(self):
        Common_Var.planid = self.text_planid.toPlainText()
        Common_Var.bn = self.text_bn.toPlainText()

    def change_server(self):
        if self.comboBox_server.currentText() == "Staging Server":
            self.label_admin_url.setDisabled(True)
            self.label_worklist_url.setDisabled(True)
            Common_Var.base_admin_url = Common_Var.staging_admin
            Common_Var.base_worklist_url = Common_Var.staging_worklist
        elif self.comboBox_server.currentText() == "Live Server":
            self.label_admin_url.setDisabled(True)
            self.label_worklist_url.setDisabled(True)
            Common_Var.base_admin_url = Common_Var.live_admin
            Common_Var.base_worklist_url = Common_Var.live_worklist
        else:
            self.label_admin_url.setEnabled(True)
            self.label_worklist_url.setEnabled(True)    

    def set_server(self):
        Common_Var.base_admin_url = self.label_admin_url.text()
        Common_Var.base_worklist_url = self.label_worklist_url.text()
    
    def start_timer(self):
        if self.thread2.running:
            self.thread2.running = False
        else:
            self.thread2.running = True

    def change_browser(self):
        if self.comboBox_browser.currentText() == "Edge":
            launch_webdriver()

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
        if self.btn_move_to_right == sender or self.btn_select_all == sender:
            source_tw = self.select_list
            target_tw = self.selected_list
        else:
            source_tw = self.selected_list
            target_tw = self.select_list
        
        # 현재 선택된 아이템을 꺼내어 반대편 쪽으로 전달
        item = source_tw.currentItem()
        try:
            parent_item = item.parent()
        except:
            pass
        
        # Parent를 선택 이동하는 경우
        try:
            if item.parent() == None:
                # Parent를 선택 이동하는데, parent가 존재하지 않는 경우
                if target_tw.topLevelItemCount() == 0:
                    source = QTreeWidget.invisibleRootItem(source_tw)
                    source.removeChild(item)
                    root = QTreeWidget.invisibleRootItem(target_tw)
                    root.addChild(item)
                # Parent를 선택 이동하는데, parnet가 존재하는 경우
                else:
                    add_item = item

                    # 선택한 item을 저장
                    for childs in range(0, item.childCount()):
                        children = []
                        add_child_list = []
                        add_subparent_list = []
                        add_parent_list = []
                        child = 0
                        
                        # Subparent에 child가 존재하는 경우
                        if item.child(child).childCount() > 0:
                            children.append(item.child(child))
                        
                            # 선택한 child의 Sub child list 저장
                            new_child_Count = item.child(child).childCount()
                            for n in range(0, new_child_Count):
                                add_child_list.append(add_item.child(child).child(n).text(0))
                                add_child_list.append(add_item.child(child).child(n).text(1))
                                # Child 저장                    
                                add_subparent_list.append(add_item.child(child).text(0))
                                add_subparent_list.append(add_item.child(child).text(1))
                        # Subparent가 아닌 경우
                        else:
                            children.append(item)
                            new_child_Count = item.childCount()
                            for n in range(0, new_child_Count):
                                add_child_list.append(add_item.child(n).text(0))
                                add_child_list.append(add_item.child(n).text(1))

                        # parent 저장
                        add_parent_list.append(add_item.text(0))
                        add_parent_list.append(add_item.text(1))

                        # Parent를 선택 이동하는데, 동일한 parent가 존재하는 경우
                        for n in range(0, target_tw.topLevelItemCount()):
                            if target_tw.topLevelItem(n).text(0) == item.text(0):
                                parent = target_tw.topLevelItem(n)
                        
                        # subparent 존재하는 경우
                        check = "fail"
                        try:
                            for i in range(0, parent.childCount()):
                                try:
                                    if parent.child(i).text(0) == add_subparent_list[0]:
                                        current_pos = parent.child(i)
                                        check = "subparent"
                                # subparent가 존재하지 않는 경우
                                except:
                                    check = "no subparent"
                                    break
                        except:
                            current_pos = QTreeWidgetItem(target_tw)
                            # current_pos.setData(0, Qt.DisplayRole, int(add_parent_list.pop(0)))
                            # current_pos.setData(1, Qt.DisplayRole, add_parent_list.pop(0))
                            current_pos.setText(0, add_parent_list.pop(0))
                            current_pos.setText(1, add_parent_list.pop(0))
                            parent = current_pos
                        
                        # Second parent가 존재하지 않는 경우, 추가
                        if check == "fail" and len(add_subparent_list) > 0:
                            current_pos = QTreeWidgetItem(parent)
                            cnt = len(add_subparent_list)
                            # current_pos.setData(0, Qt.DisplayRole, float(add_subparent_list.pop(item_cnt - 2)))
                            # current_pos.setData(1, Qt.DisplayRole, add_subparent_list.pop(item_cnt - 2))
                            current_pos.setText(0, add_subparent_list.pop(cnt-2))
                            current_pos.setText(1, add_subparent_list.pop(cnt-2))
                            cnt -= 2
                        elif check == "no subparent":
                            current_pos = parent

                        # Child 추가
                        cnt = len(add_child_list)
                        if len(add_subparent_list) != 0:
                            while len(add_child_list) != 0:
                                new_item = QTreeWidgetItem(current_pos)
                                # new_item.setData(0, Qt.DisplayRole, float(add_child_list.pop(item_cnt - 2)))
                                # new_item.setData(1, Qt.DisplayRole, add_child_list.pop(item_cnt - 2))
                                new_item.setText(0, add_child_list.pop(cnt-2))
                                new_item.setText(1, add_child_list.pop(cnt-2))
                                cnt -= 2
                        else:
                            while len(add_child_list) != 0:
                                new_item = QTreeWidgetItem(current_pos)
                                # new_item.setData(0, Qt.DisplayRole, float(add_child_list.pop(item_cnt - 2)))
                                # new_item.setData(1, Qt.DisplayRole, add_child_list.pop(item_cnt - 2))
                                new_item.setText(0, add_child_list.pop(cnt-2))
                                new_item.setText(1, add_child_list.pop(cnt-2))
                                cnt -= 2

                            # Selected list에 추가하고 선택한 item을 select list에서 삭제
                            for child in children:
                                item.removeChild(child)

                            # Child가 존재하지 않는 경우, parent 삭제
                            if item.childCount() == 0:
                                sip.delete(item)    
                            break

                        # Selected list에 추가하고 선택한 item을 select list에서 삭제
                        for child in children:
                            item.removeChild(child)

                        # Child가 존재하지 않는 경우, parent 삭제
                        if item.childCount() == 0:
                            sip.delete(item)                        

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
                    # new_item.setData(0, Qt.DisplayRole, int(add_item_list.pop(item_cnt - 2)))
                    # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
                    new_item.setText(1, add_item_list.pop(item_cnt - 2))
                    new_item.setText(0, add_item_list.pop(item_cnt - 2))
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
                        try:
                            # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(item_cnt - 2)))
                            # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
                            new_item.setText(0, add_item_list.pop(item_cnt - 2))
                            new_item.setText(1, add_item_list.pop(item_cnt - 2))
                            item_cnt -= 2
                        except Exception as e:
                            print(e)

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
                                if current_pos.child(n).text(0) == add_item_list[item_cnt-2]:
                                    new_item = QTreeWidgetItem(current_pos.child(n))
                                    add_item_list.pop(item_cnt - 2)
                                    add_item_list.pop(item_cnt - 2)
                                    item_cnt -= 2

                                    # # child 추가
                                    # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(item_cnt - 2)))
                                    # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
                                    new_item.setText(0, add_item_list.pop(item_cnt - 2))
                                    new_item.setText(1, add_item_list.pop(item_cnt - 2))
                
                        # Second parent가 없으면 추가
                        if item_cnt > 3:
                            new_item = QTreeWidgetItem(current_pos)
                            # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(item_cnt - 2)))
                            # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
                            new_item.setText(0, add_item_list.pop(item_cnt - 2))
                            new_item.setText(1, add_item_list.pop(item_cnt - 2))
                            item_cnt -= 2

                            # child 추가
                            sub_item = QTreeWidgetItem()
                            # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(item_cnt - 2)))
                            # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
                            sub_item.setText(0, add_item_list.pop(item_cnt - 2))
                            sub_item.setText(1, add_item_list.pop(item_cnt - 2))
                            new_item.addChild(sub_item)
                    else:
                    # child 추가
                        new_item = QTreeWidgetItem(current_pos)
                        # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(item_cnt - 2)))
                        # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(item_cnt - 2))
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
                    # new_item.setData(0, Qt.DisplayRole, int(add_item_list.pop(cnt-2)))
                    # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(cnt-2))
                    new_item.setText(0, add_item_list.pop(cnt-2))
                    new_item.setText(1, add_item_list.pop(cnt-2))
                    cnt -= 2

                    # Second parent 추가
                    if cnt > new_child_Count*2:
                        new_item = QTreeWidgetItem(new_item)
                        new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(cnt-2)))
                        new_item.setData(1, Qt.DisplayRole, add_item_list.pop(cnt-2))
                        # new_item.setText(0, add_item_list.pop(cnt-2))
                        # new_item.setText(1, add_item_list.pop(cnt-2))

                    # Selected list에 추가하고 선택한 item을 select list에서 삭제
                    for child in children:
                        item.parent().removeChild(child)

                        # Parent에 child가 존재하지 않는 경우, parenet 삭제
                        if parent_item.childCount() == 0:
                            sip.delete(parent_item)

                    # Child 추가            
                    if len(add_item_list) > 0:
                        while len(add_item_list) > 0:
                            try:
                                sub_item = QTreeWidgetItem()
                                sub_item.setData(0, Qt.DisplayRole, add_item_list.pop(0))
                                sub_item.setData(1, Qt.DisplayRole, add_item_list.pop(0))
                                # sub_item.setText(0, add_item_list.pop(0))
                                # sub_item.setText(1, add_item_list.pop(0))
                                new_item.addChild(sub_item)
                            except Exception as e:
                                print(e)
                # Selected list에 선택한 item의 parent가 존재하는 경우
                else:
                    if target_tw.topLevelItem(n).text(0) == current_pos.text(0):
                        add_item_list.pop(cnt-2)
                        add_item_list.pop(cnt-2)
                        cnt -= 2

                        # Second parent 존재하는 경우
                        check = False
                        for i in range(0, current_pos.childCount()):
                            if add_item_list[cnt-2] == current_pos.child(i).text(0):
                                new_item = current_pos.child(i)
                                add_item_list.pop(cnt-2)
                                add_item_list.pop(cnt-2)
                                cnt -= 2
                                check = True
                                break

                        if check == False:
                            new_item = QTreeWidgetItem(current_pos)
                            # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(cnt-2)))
                            # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(cnt-2))
                            new_item.setText(0, add_item_list.pop(cnt-2))
                            new_item.setText(1, add_item_list.pop(cnt-2))
                    else:
                        # Second parent 추가
                        # new_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(cnt-2)))
                        # new_item.setData(1, Qt.DisplayRole, add_item_list.pop(cnt-2))
                        new_item.setText(0, add_item_list.pop(cnt-2))
                        new_item.setText(1, add_item_list.pop(cnt-2))

                    # Child 추가            
                    if len(add_item_list) > 0:
                        while len(add_item_list) > 0:
                            sub_item = QTreeWidgetItem()
                            # sub_item.setData(0, Qt.DisplayRole, float(add_item_list.pop(0)))
                            # sub_item.setData(1, Qt.DisplayRole, add_item_list.pop(0))
                            sub_item.setText(0, add_item_list.pop(0))
                            sub_item.setText(1, add_item_list.pop(0))
                            new_item.addChild(sub_item)
                    
                    # Selected list에 추가하고 선택한 item을 select list에서 삭제
                    for child in children:
                        item.parent().removeChild(child)

                        # Parent에 child가 존재하지 않는 경우, parenet 삭제
                        if parent_item.childCount() == 0:
                            sip.delete(parent_item)
        except:
            pass

    def select_all(self):
        source_tw = self.select_list
        target_tw = self.selected_list
        if target_tw.topLevelItemCount() != 0:
            for i in range(0, target_tw.topLevelItemCount()):
                item = target_tw.topLevelItem(0)
                self.move_item()
        
        for i in range(0, source_tw.topLevelItemCount()):
            item = source_tw.topLevelItem(0)
            source = QTreeWidget.invisibleRootItem(source_tw)
            source.removeChild(item)
            root = QTreeWidget.invisibleRootItem(target_tw)
            root.addChild(item)

    def deselect_all(self):
        target_tw = self.select_list
        source_tw = self.selected_list
        if target_tw.topLevelItemCount() != 0:
            for i in range(0, target_tw.topLevelItemCount()):
                item = target_tw.topLevelItem(0)
                self.move_item()
        for i in range(0, source_tw.topLevelItemCount()):
            item = source_tw.topLevelItem(0)
            source = QTreeWidget.invisibleRootItem(source_tw)
            source.removeChild(item)
            root = QTreeWidget.invisibleRootItem(target_tw)
            root.addChild(item)

    def run(self):
        h2 = Thread1(self)
        h2.start()

    def init_status(self):
        self.label_testcase.setText(str(len(testcase_list)))
        self.label_passed.setText(str(Common_Var.test_status_passed))
        self.label_passed.setStyleSheet("Color : green")
        self.label_3.setStyleSheet("Color : green")
        self.label_failed.setText(str(Common_Var.test_status_failed))
        self.label_failed.setStyleSheet("Color : red")
        self.label_4.setStyleSheet("Color : red")
        Common_Var.test_status_notexecuted = int(len(testcase_list))
        self.label_notexecuted.setText(str(int(len(testcase_list))))
        self.label_6.setStyleSheet("Color : orange")
        self.label_exception.setStyleSheet("Color : orange")
        Common_Var.form.label_executed.setText(str(Common_Var.executed) + "% executed")

    def update_passed(self):
        mysignal = UpdatePassSignal()
        mysignal.signal.connect(self.signal_pass)
        mysignal.run()

    def update_failed(self):
        mysignal = UpdateFailSignal()
        mysignal.signal.connect(self.signal_fail)
        mysignal.run()

    def update_exception(self):
        mysignal = UpdateExceptionSignal()
        mysignal.signal.connect(self.signal_exception)
        mysignal.run()
    
    def init_tablewidget(self):
        Common_Var.form.tableWidget.setColumnCount(5)
        Common_Var.row = len(testcase_list)
        Common_Var.form.tableWidget.setRowCount(Common_Var.row)
        Common_Var.form.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        column_headers = ["TestCase Name","Run Status","Test Steps","Defects","Run Time(min)"]
        Common_Var.form.tableWidget.setHorizontalHeaderLabels(column_headers)
        Common_Var.form.tableWidget.setColumnWidth(0,220)
        Common_Var.form.tableWidget.setColumnWidth(1,130)
        Common_Var.form.tableWidget.setColumnWidth(2,90)
        Common_Var.form.tableWidget.setColumnWidth(3,90)
        Common_Var.form.tableWidget.setColumnWidth(4,110)
        Common_Var.form.tableWidget.resizeRowsToContents()
        
    def update_table(self):
        mysignal = UpdateTableSignal()
        mysignal.signal.connect(self.signal_update_table)
        mysignal.run()

    def run_test(self):
        global testcase_list
        testcase_list = []
        
        # Selected list에서 first parent 개수 확인
        for n in range(0, self.selected_list.topLevelItemCount()):
            first_parent = self.selected_list.topLevelItem(n)

            # first parent에 child가 있는지 확인
            for i in range(0, first_parent.childCount()):
                # second parent가 아니면 testcase list에 저장
                if first_parent.child(i).childCount() == 0:
                    testcase_list.append(first_parent.child(i).text(1))
                # second parent 일 경우
                else:
                    for j in range(0, first_parent.child(i).childCount()):
                        testcase_list.append(first_parent.child(i).child(j).text(1))
        self.init_status()
        self.init_tablewidget()
        self.update_testlink()
        if self.comboBox_server.currentText() == "Custom Server":            
            self.set_server()
        else: 
            self.change_server()
        if self.noTestlink.isChecked() != True:
            self.set_testlink()
        if self.comboBox_browser.currentText() == "Edge":
            launch_webdriver()
        self.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Common_Var.form = Form()
    Common_Var.form.setWindowTitle("ITR Automation Test")
    Common_Var.form.show()
    sys.exit(app.exec_())