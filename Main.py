import ITR_Admin_Common
import ITR_Admin_Login
import ITR_Admin_Refer
import ITR_Admin_Worklist
import ITR_Admin_Statistics
import ITR_Admin_Configuration
import ITR_Admin_Auditlog
import ITR_Admin_Notice
import ITR_Admin_DirectMessage
import time
# from ITR_Execute_GUI import Form
import Common_Var
import importlib
import sys

full_test_case = [
    # Sign
    ITR_Admin_Login.Sign.Sign_InOut, # ITR-1
    ITR_Admin_Login.Sign.Rememeber_Me, # ITR-2
    # Topbar
    ITR_Admin_Login.Topbar.Search_Schedule_List, # ITR-3
    # Refer
    # ITR_Admin_Login.signInOut.admin_sign_out, # Admin logout
    # ITR_Admin_Login.signInOut.subadmin_sign_in, # SubAdmin login
    ITR_Admin_Refer.Refer.Hospital_List, # ITR-7
    ITR_Admin_Refer.Refer.Reporter_List, # ITR-8
    # Search filter
    ITR_Admin_Refer.Search_filter.Priority, # ITR-9
    ITR_Admin_Refer.Search_filter.Job_Status, # ITR-10
    ITR_Admin_Refer.Search_filter.Date, # ITR-11
    ITR_Admin_Refer.Search_filter.Patient_Location, # ITR-12
    ITR_Admin_Refer.Search_filter.Patient_ID, # ITR-13
    ITR_Admin_Refer.Search_filter.Patient_Name, # ITR-14
    ITR_Admin_Refer.Search_filter.Age, # ITR-15
    ITR_Admin_Refer.Search_filter.Study_Description, # ITR-16
    ITR_Admin_Refer.Search_filter.Modality, # ITR-17
    ITR_Admin_Refer.Search_filter.Bodypart, # ITR-18
    ITR_Admin_Refer.Search_filter.Department, # ITR-19
    ITR_Admin_Refer.Search_filter.Request_Name, # ITR-20
    ITR_Admin_Refer.Search_filter.Search_All, # ITR-21
    ITR_Admin_Refer.Search_filter.RealTime, # ITR-22
    ITR_Admin_Refer.Search_filter.ShortCut, # ITR-23
    # Worklist
    ITR_Admin_Worklist.Worklist.All_Assigned_List, # ITR-24
    ITR_Admin_Worklist.Worklist.Not_Assigned_List, # ITR-25
    ITR_Admin_Worklist.Worklist.All_List, # ITR-26
    ITR_Admin_Worklist.Worklist.Schedule, # ITR-27
    ITR_Admin_Worklist.Worklist.Priority, # ITR-28
    ITR_Admin_Worklist.Worklist.Canceled, # ITR-29
    ITR_Admin_Worklist.Worklist.Refer, # ITR-30
    ITR_Admin_Worklist.Worklist.Refer_Cancel, # ITR-31
    ITR_Admin_Worklist.Worklist.Refer_Cancel_And_Refer, # ITR-32
    ITR_Admin_Worklist.Worklist.Set_Schedule, # ITR-34
    ITR_Admin_Worklist.Worklist.Schedule_Cancel, # ITR-35
    ITR_Admin_Worklist.Worklist.Revised, # ITR-36
    ITR_Admin_Worklist.Worklist.Discard, # ITR-37
    ITR_Admin_Worklist.Worklist.Retry_Request, # ITR-38
    ITR_Admin_Worklist.Worklist.Columns, # ITR-39
    ITR_Admin_Worklist.Worklist.Show_Entries, # ITR-40
    ITR_Admin_Worklist.Worklist.Use_Related_Worklist, # ITR-224
    ITR_Admin_Worklist.Worklist.Sort_By, # ITR-41
    # Statistics
    # ITR_Admin_Login.signInOut.subadmin_sign_out, # SubAdmin logout
    # ITR_Admin_Login.signInOut.admin_sign_in, # Admin login
    ITR_Admin_Statistics.Statistics.SearchFilter_Date, # ITR-44
    ITR_Admin_Statistics.Statistics.SearchFilter_Hospital, # ITR-45
    ITR_Admin_Statistics.Statistics.SearchFilter_Reporter, # ITR-46
    ITR_Admin_Statistics.Statistics.SearchFilter_Modality, # ITR-47
    ITR_Admin_Statistics.Statistics.Columns, # ITR-42
    ITR_Admin_Statistics.Statistics.Show_Entries, # ITR-43
    # Confiuration - User Management
    ITR_Admin_Configuration.UserManagement.SearchFilter_Class, # ITR-49
    ITR_Admin_Configuration.UserManagement.SearchFilter_Institution, # ITR-50
    ITR_Admin_Configuration.UserManagement.SearchFilter_UserID, # ITR-51
    ITR_Admin_Configuration.UserManagement.SearchFilter_UserName, # ITR-52
    ITR_Admin_Configuration.UserManagement.SearchFilter_ShowWithMappingID, # ITR-53
    ITR_Admin_Configuration.UserManagement.UserRegistartion_Add, # ITR-54
    ITR_Admin_Configuration.UserManagement.UserRegistartion_Delete, # ITR-218
    ITR_Admin_Configuration.UserManagement.UserRegistartion_Modify, # ITR-56
    # Confiuration - Specialty
    ITR_Admin_Configuration.Specialty.SpecialtyList_Search, # ITR-56
    ITR_Admin_Configuration.Specialty.SpecialtyList_Add, # ITR-57
    ITR_Admin_Configuration.Specialty.SpecialtyList_Delete, # ITR-58
    ITR_Admin_Configuration.Specialty.SpecialtyList_Modify, # ITR-59
    ITR_Admin_Configuration.Specialty.InstitutionList_Search, # ITR-60
    ITR_Admin_Configuration.Specialty.InstitutionList_Add, # ITR-61
    ITR_Admin_Configuration.Specialty.InstitutionList_Delete, # ITR-64
    ITR_Admin_Configuration.Specialty.InstitutionList_Modify, # ITR-65
    ITR_Admin_Configuration.Specialty.InstitutionList_Modify_Search, # ITR-68
    # Confiuration - Download Control
    ITR_Admin_Configuration.DownloadControl.User_SearchFilter_Class, # ITR-69
    ITR_Admin_Configuration.DownloadControl.User_SearchFilter_Institution, # ITR-70
    ITR_Admin_Configuration.DownloadControl.User_SearchFilter_UserID, # ITR-71
    ITR_Admin_Configuration.DownloadControl.User_SearchFilter_UserName, # ITR-72
    ITR_Admin_Configuration.DownloadControl.User_Add, # ITR-73
    ITR_Admin_Configuration.DownloadControl.User_Delete, # ITR-74
    ITR_Admin_Configuration.DownloadControl.User_Modify, # ITR-75
    ITR_Admin_Configuration.DownloadControl.Institution_SearchFilter_Class, # ITR-76
    ITR_Admin_Configuration.DownloadControl.Institution_SearchFilter_Institution, # ITR-77
    ITR_Admin_Configuration.DownloadControl.Institution_SearchFilter_UserID, # ITR-78
    ITR_Admin_Configuration.DownloadControl.Institution_SearchFilter_UserName, # ITR-79
    ITR_Admin_Configuration.DownloadControl.Institution_Add, # ITR-80
    ITR_Admin_Configuration.DownloadControl.Institution_Delete, # ITR-81
    ITR_Admin_Configuration.DownloadControl.Institution_Modify, # ITR-82
    # Confiuration - Institutions
    ITR_Admin_Configuration.Institution.SearchFilter_Institution_Code, # ITR-83
    ITR_Admin_Configuration.Institution.SearchFilter_Institution_Name, # ITR-84
    ITR_Admin_Configuration.Institution.Add, # ITR-85
    ITR_Admin_Configuration.Institution.Delete, # ITR-86
    ITR_Admin_Configuration.Institution.Modify, # ITR-87
    # Add > GroupAdd > GroupModify > Modify > Delete
    # Confiuration - Standard Report
    ITR_Admin_Configuration.StandardReport.All, # ITR-88~93
    # Confiuration - Multi Reading Center Rule
    ITR_Admin_Configuration.MultiReadingCenterRule.SearchFilter, # ITR-94
    # MultiReadingCenterRule.Add() > MultiReadingCenterRule.Modify() > MultiReadingCenterRule.Delete()
    ITR_Admin_Configuration.MultiReadingCenterRule.All, # ITR-95~97
    # Audit Log
    ITR_Admin_Auditlog.Auditlog.Auditlog_Search, # ITR-98
    ITR_Admin_Auditlog.Auditlog.Auditlog_Export, # ITR-99
    ITR_Admin_Auditlog.Auditlog.Auditlog_Showentries, # ITR-100
    ITR_Admin_Auditlog.Auditlog.Auditlog_Sorting, # ITR-101
    ITR_Admin_Auditlog.Auditlog.Auditlog_Data, # ITR-102
    # Notice
    ITR_Admin_Notice.Notice.NoticeList_NoticeEditBoard, # ITR-103
    ITR_Admin_Notice.Notice.NoticeList_Edit, # ITR-104
    ITR_Admin_Notice.Notice.NoticeList_Delete, # ITR-105
    ITR_Admin_Notice.Notice.NoticeList_NoticeDisplay, # ITR-106
    # Direct Message
    ITR_Admin_Login.signInOut.admin_sign_out, # SubAdmin login
    ITR_Admin_Login.signInOut.subadmin_sign_in, # SubAdmin login
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageBox_Search, # ITR-107
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageBox_ShowEntries, # ITR-108
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageBox_Sorting, # ITR-109
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageBox_Badge, # ITR-110
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageBox_Message, # ITR-111
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Institution_Search, # ITR-112
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Institution_Message, # ITR-113
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Center_Search, # ITR-114
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Center_Message, # ITR-115
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Reporter_Search, # ITR-116
    ITR_Admin_DirectMessage.DirectMessage.NewDirectMessage_Reporter_Message, # ITR-117
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageSetting_Search, # ITR-118
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageSetting_Authorize, # ITR-119
    ITR_Admin_DirectMessage.DirectMessage.DirectMessageSetting_Selection # ITR-120
    ]

test_index_list = [
    ["Sign In/Out",5],
    ["Remember Me",1],
    ["Search Schedule List",2],
    ["Hospital List",8],
    ["Reporter List",3],
    ["Search Priority",3],
    ["Job Status",13],
    ["Search Date",4],
    ["Patient Location",5],
    ["Patient ID",2],
    ["Patient Name",2],
    ["Age",4],
    ["Study Description",1],
    ["Search Modality",1],
    ["Bodypart",1],
    ["Department",1],
    ["Request Name",1],
    ["Search All",1],
    ["Real Time",2],
    ["Short cut",14],
    ["All Assigned List",1],
    ["Not Assigned List",1],
    ["All List",5],
    ["Schedule",2],
    ["Worklist Priority",2],
    ["Canceled",3],
    ["Refer",9],
    ["Refer Cancel",6],
    ["Refer Cancel and Refer",7],
    ["Set Schedule",4],
    ["Schedule Cancel",4],
    ["Revised",1],
    ["Discard",2],
    ["Retry Request",2],
    ["Worklist Columns",6],
    ["Show entries",4],
    ["Sort by",1],
    ["User Related Wokrlist",1],
    ["Statistics Date",5],
    ["Hospital",1],
    ["Reporter",1],
    ["Statistics Modality",1],
    ["Statistics Columns",4],
    ["Statistics Show entries",4],
    ["Class",1],
    ["Insitution",1],
    ["User ID",1],
    ["User Name",1],
    ["Show with Mapping ID",1],
    ["User Registration Add",24],
    ["User Registration Modify",22],
    ["User Registration Delete",4],
    ["Specialty Search",2],
    ["Specialty Add",3],
    ["Specialty Delete",4],
    ["Specialty Modify",10],
    ["Institution List Search",1],
    ["Specialty Institution Add",5],
    ["Specialty Institution Delete",4],
    ["Specialty Institution Modify",3],
    ["Specialty Institution Modify - Search",7],
    ["User Search Filter - Class",1],
    ["User Search Filter - Institution",1],
    ["User Search Filter - User ID",1],
    ["User Search Filter - User Name",1],
    ["User Add",13],
    ["User Delete",4],
    ["User Modify",14],
    ["Institution Search Filter - Class", 1],
    ["Institution Search Filter - Institution",1],
    ["Institution Search Filter - User ID",1],
    ["Institution Search Filter - User Name",1],
    ["D.C. Institution Add",13],
    ["D.C. Institution Delete",4],
    ["D.C. Institution Modify",14],
    ["Institution Code",1],
    ["Institution Name",1],
    ["Institution Add",14],
    ["Institution Delete",4],
    ["Institution Modify",13],
    ["Group Add",3],
    ["Standard Report Add",10],
    ["Standard Report Delete",4],
    ["Group Modify",4],
    ["Standard Report Modify",10],
    ["Multi Reading Search Filter",12],
    ["Multi Reading Add",12],
    ["Multi Reading Delete",1],
    ["Multi Reading Modify",9],
    ["Audit Log Search",1],
    ["Audit Log Export",1],
    ["Audit Log Show entries",3],
    ["Audit Log Sorting",1],
    ["Audit Log Data",1],
    ["Notice Edit Board",23],
    ["Notice Edit",9],
    ["Notice Delete",1],
    ["Notice Display",1],
    ["Direct Message Search",4],
    ["Direct Message Show entries",5],
    ["Direct Message Sorting",3],
    ["Badge",1],
    ["Message",1],
    ["Institution - Search",3],
    ["Institution - Message",3],
    ["Center - Search",3],
    ["Center - Message",3],
    ["Reporter - Search",3],
    ["Reporter - Message",3],
    ["Direct Message Setting Search",4],
    ["Authorize",4],
    ["Selection",6]
]

def get_name(name):
    for i in test_index_list:
        if i[0] == name:
            return test_index_list.index(i)

def get_step(name):
    for i in test_index_list:
        if i[0] == name:
            return test_index_list[test_index_list.index(i)][1]
            
def get_index(name):
    for i in test_index_list:
        if i[0] == name:
            return test_index_list.index(i)

def input_timer(prompt, timeout_sec):
    import subprocess
    import sys
    import threading
    import locale

    class Local:
        # check if timeout occured
        _timeout_occured = False

        def on_timeout(self, process):
            self._timeout_occured = True
            process.kill()
            # clear stdin buffer (for linux)
            # when some keys hit and timeout occured before enter key press,
            # that input text passed to next input().
            # remove stdin buffer.
            try:
                import termios
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except ImportError:
                # windows, just exit
                pass

        def input_timer_main(self, prompt_in, timeout_sec_in):
            # print with no new line
            print(prompt_in, end="")

            # print prompt_in immediately
            sys.stdout.flush()

            # new python input process create.
            # and print it for pass stdout
            cmd = [sys.executable, '-c', 'print(input())']
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                timer_proc = threading.Timer(timeout_sec_in, self.on_timeout, [proc])
                try:
                    # timer set
                    timer_proc.start()
                    stdout, stderr = proc.communicate()

                    # get stdout and trim new line character
                    result = stdout.decode(locale.getpreferredencoding()).strip("\r\n")
                finally:
                    # timeout clear
                    timer_proc.cancel()

            # timeout check
            if self._timeout_occured is True:
                # move the cursor to next line
                print("")
                raise TimeoutError
            return result

    t = Local()
    return t.input_timer_main(prompt, timeout_sec)
class Test:
    # Full Test
    def full_test():
        start = time.time()
        failed_test_list = []
        
        for test in full_test_case:
            time.sleep(0.5)
            try:
                print("(",str(full_test_case.index(test)+1) + " / " + str(len(full_test_case)),")", round(((full_test_case.index(test)+1)*100/int(len(full_test_case))),1),"%")
                run_time = time.time()
                test()
            except:
                # print("Exception on " + str(test))
                print("An exception occurred.")
                for i in range(0,3):
                    try:
                        if test not in failed_test_list:
                            failed_test_list.append(test)
                        print("Retry ("+str(i+1)+"/3)")
                        test()
                        failed_test_list.remove(test)
                        break
                    except:
                        ITR_Admin_Common.driver.refresh()
                        print("An exception occurred.")
                        pass
            finally:
                print("Run Time:", round((int(time.time() - run_time)/60),2),"min\n")
                pass
        #for test in full_test_case:
        #    test()

        print("Total Run Time:", round((int(time.time() - start)/60),2),"min")
        print("failed_test_list: ", failed_test_list)
        
        ITR_Admin_Common.driver.quit()
    def delay():
        time.sleep(0.5)
    def function_test(testcase_list):
        importlib.reload(sys.modules['ITR_Admin_Common'])
        importlib.reload(sys.modules['ITR_Admin_Login'])
        importlib.reload(sys.modules['ITR_Admin_Refer'])
        importlib.reload(sys.modules['ITR_Admin_Worklist'])
        importlib.reload(sys.modules['ITR_Admin_Statistics'])
        importlib.reload(sys.modules['ITR_Admin_Configuration'])
        importlib.reload(sys.modules['ITR_Admin_Notice'])
        importlib.reload(sys.modules['ITR_Admin_Auditlog'])
        importlib.reload(sys.modules['ITR_Admin_DirectMessage'])

        # from ITR_Admin_Common import driver
        ITR_Admin_Common.driver.get(Common_Var.base_admin_url)
        start = time.time()
        failed_test_list = []
        testnum = 0
        for case in testcase_list:
            teststep = get_step(case)
            testidx = get_index(case)            
            time.sleep(0.5)            
            try:
                print("(",str((testnum+1)) + " / " + str(len(testcase_list)),")", round((testnum+1)*100/int(len(testcase_list)),1),"%")
                Common_Var.progress_bar = round((testnum+1)*100/int(len(testcase_list)),1)
                Common_Var.executed = int((testnum+1)*100/int(len(testcase_list)))
                run_time = time.time()
                # TableWidget 값 추가
                Common_Var.tc_name = case
                Common_Var.tc_steps = teststep
                full_test_case[testidx]()
                while Common_Var.btn_play == "Play":
                    try:
                        a = input_timer("Pause the test: ", 1)
                    except:
                        time.sleep(1)
                        pass
                testnum += 1
                Test.delay()
            except Exception as e:
                print(e)
                # print("Exception on " + str(test))
                print("An exception occurred.")
                Common_Var.form.update_exception()
                for i in range(0,3):
                    try:
                        if full_test_case[testidx] not in failed_test_list:
                            failed_test_list.append(full_test_case[testidx])
                        print("Retry ("+str(i+1)+"/3)")
                        full_test_case[testidx]()
                        failed_test_list.remove(full_test_case[testidx])
                        testnum += 1
                        break
                    except:
                        # ITR_Admin_Common.driver.refresh()
                        print("An exception occurred.")
                        Common_Var.form.update_exception()
                        testnum += 1
                        pass
            finally:
                print("Run Time:", round((int(time.time() - run_time)/60),2),"min\n")
                pass
    
        Common_Var.form.update_timer()

        print("Total Run Time:", round((int(time.time() - start)/60),2),"min")
        print("failed_test_list: ", failed_test_list)
        
        ITR_Admin_Common.driver.quit()

    # full test 
    # full_test()