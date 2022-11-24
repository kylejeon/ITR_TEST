import ITR_Admin
import time

sign_list = [
    # Sign
    ITR_Admin.Sign.Sign_InOut, # ITR-1
    ITR_Admin.Sign.Rememeber_Me # ITR-2
    ]

topbar_list = [
    # Topbar
    ITR_Admin.Topbar.Search_Schedule_List # ITR-3
    ]

refer_list = [
    # Refer
    ITR_Admin.Refer.Hospital_List, # ITR-7
    ITR_Admin.Refer.Reporter_List # ITR-8
    ]

search_filter_list = [
    # Search filter
    ITR_Admin.Search_filter.Priority, # ITR-9
    ITR_Admin.Search_filter.Job_Status, # ITR-10
    ITR_Admin.Search_filter.Date, # ITR-11
    ITR_Admin.Search_filter.Patient_Location, # ITR-12
    ITR_Admin.Search_filter.Patient_ID, # ITR-13
    ITR_Admin.Search_filter.Patient_Name, # ITR-14
    ITR_Admin.Search_filter.Age, # ITR-15
    ITR_Admin.Search_filter.Study_Description, # ITR-16
    ITR_Admin.Search_filter.Modality, # ITR-17
    ITR_Admin.Search_filter.Bodypart, # ITR-18
    ITR_Admin.Search_filter.Department, # ITR-19
    ITR_Admin.Search_filter.Request_Name, # ITR-20
    ITR_Admin.Search_filter.Search_All, # ITR-21
    ITR_Admin.Search_filter.RealTime, # ITR-22
    ITR_Admin.Search_filter.ShortCut # ITR-23
    ]

worklist_list = [
    # Worklist
    ITR_Admin.Worklist.All_Assigned_List, # ITR-24
    ITR_Admin.Worklist.Not_Assigned_List, # ITR-25
    ITR_Admin.Worklist.All_List, # ITR-26
    ITR_Admin.Worklist.Schedule, # ITR-27
    ITR_Admin.Worklist.Priority, # ITR-28
    ITR_Admin.Worklist.Canceled, # ITR-29
    ITR_Admin.Worklist.Refer, # ITR-30
    ITR_Admin.Worklist.Refer_Cancel, # ITR-31
    ITR_Admin.Worklist.Refer_Cancel_And_Refer, # ITR-32
    ITR_Admin.Worklist.Set_Schedule, # ITR-34
    ITR_Admin.Worklist.Schedule_Cancel, # ITR-35
    ITR_Admin.Worklist.Revised, # ITR-36
    ITR_Admin.Worklist.Discard, # ITR-37
    ITR_Admin.Worklist.Retry_Request, # ITR-38
    ITR_Admin.Worklist.Columns, # ITR-39
    ITR_Admin.Worklist.Show_Entries, # ITR-40
    ITR_Admin.Worklist.Use_Related_Worklist, # ITR-224
    ITR_Admin.Worklist.Sort_By # ITR-41
    ]
statistics_list = [
    # Statistics
    ITR_Admin.Statistics.SearchFilter_Date, # ITR-44
    ITR_Admin.Statistics.SearchFilter_Hospital, # ITR-45
    ITR_Admin.Statistics.SearchFilter_Reporter, # ITR-46
    ITR_Admin.Statistics.SearchFilter_Modality, # ITR-47
    ITR_Admin.Statistics.Columns, # ITR-42
    ITR_Admin.Statistics.Show_Entries # ITR-43
    ]

UserManagement_SearchFilter_List = [
    ITR_Admin.UserManagement.SearchFilter_Class,
    ITR_Admin.UserManagement.SearchFilter_Institution,
    ITR_Admin.UserManagement.SearchFilter_UserID,
    ITR_Admin.UserManagement.SearchFilter_UserName,
    ITR_Admin.UserManagement.SearchFilter_ShowWithMappingID
    ]

UserManagement_UserRegistartion_List = [
    ITR_Admin.UserManagement.UserRegistartion_Add,
    ITR_Admin.UserManagement.UserRegistartion_Delete,
    ITR_Admin.UserManagement.UserRegistartion_Modify
    ]

Specialty_SpecialtyList_List = [
    ITR_Admin.Specialty.SpecialtyList_Search,
    ITR_Admin.Specialty.SpecialtyList_Add,
    ITR_Admin.Specialty.SpecialtyList_Delete,
    ITR_Admin.Specialty.SpecialtyList_Modify
    ]

Specialty_InstitutionList = [
    ITR_Admin.Specialty.InstitutionList_Search, 
    ITR_Admin.Specialty.InstitutionList_Add,
    ITR_Admin.Specialty.InstitutionList_Delete,
    ITR_Admin.Specialty.InstitutionList_Modify,
    ITR_Admin.Specialty.InstitutionList_Modify_Search
    ]

DownloadControl_User_List = [
    ITR_Admin.DownloadControl.User_SearchFilter_Class,
    ITR_Admin.DownloadControl.User_SearchFilter_Institution,
    ITR_Admin.DownloadControl.User_SearchFilter_UserID,
    ITR_Admin.DownloadControl.User_SearchFilter_UserName,
    ITR_Admin.DownloadControl.User_Add,
    ITR_Admin.DownloadControl.User_Delete,
    ITR_Admin.DownloadControl.User_Modify
    ]

DownloadControl_Institution_List = [
    ITR_Admin.DownloadControl.Institution_SearchFilter_Class,
    ITR_Admin.DownloadControl.Institution_SearchFilter_Institution,
    ITR_Admin.DownloadControl.Institution_SearchFilter_UserID,
    ITR_Admin.DownloadControl.Institution_SearchFilter_UserName,
    ITR_Admin.DownloadControl.Institution_Add,
    ITR_Admin.DownloadControl.Institution_Delete,
    ITR_Admin.DownloadControl.Institution_Modify
    ]

Institution_List = [
    ITR_Admin.Institution.SearchFilter,
    ITR_Admin.Institution.Add,
    ITR_Admin.Institution.Delete,
    ITR_Admin.Institution.Modify
    ]

StandardReport_List = [
    # Add > GroupAdd > GroupModify > Modify > Delete
    ITR_Admin.StandardReport.All
    ]

MultiReadingCenterRule_List = [
    ITR_Admin.MultiReadingCenterRule.SearchFilter,
    # MultiReadingCenterRule.Add() > MultiReadingCenterRule.Modify() > MultiReadingCenterRule.Delete()
    ITR_Admin.MultiReadingCenterRule.All
    ]

Auditlog_List = [
    ITR_Admin.Auditlog.Auditlog_Search,
    ITR_Admin.Auditlog.Auditlog_Export,
    ITR_Admin.Auditlog.Auditlog_Showentries,
    ITR_Admin.Auditlog.Auditlog_Sorting,
    ITR_Admin.Auditlog.Auditlog_Data
    ]

Notice_List = [
    ITR_Admin.Notice.NoticeList_NoticeEditBoard,
    ITR_Admin.Notice.NoticeList_Edit,
    ITR_Admin.Notice.NoticeList_Delete,
    ITR_Admin.Notice.NoticeList_NoticeDisplay
    ]

DirectMessageBox_List = [
    ITR_Admin.DirectMessage.DirectMessageBox_Search, 
    ITR_Admin.DirectMessage.DirectMessageBox_ShowEntries,
    ITR_Admin.DirectMessage.DirectMessageBox_Sorting,
    ITR_Admin.DirectMessage.DirectMessageBox_Badge,
    ITR_Admin.DirectMessage.DirectMessageBox_Message
    ]

NewDirectMessage_Institution_List = [
    ITR_Admin.DirectMessage.NewDirectMessage_Institution_Search,
    ITR_Admin.DirectMessage.NewDirectMessage_Institution_Message,
    ITR_Admin.DirectMessage.NewDirectMessage_Center_Search,
    ITR_Admin.DirectMessage.NewDirectMessage_Center_Message,
    ITR_Admin.DirectMessage.NewDirectMessage_Reporter_Search,
    ITR_Admin.DirectMessage.NewDirectMessage_Reporter_Message
    ]

DirectMessageSetting_List = [
    ITR_Admin.DirectMessage.DirectMessageSetting_Search,
    ITR_Admin.DirectMessage.DirectMessageSetting_Authorize,
    ITR_Admin.DirectMessage.DirectMessageSetting_Selection
    ]

# Full Test
def full_test():
    start = time.time()
    failed_test_list = []

    for test in full_test:
        time.sleep(0.5)
        try:
            print("(",str(full_test.index(test)+1) + " / " + str(len(full_test)),")", round(((full_test.index(test)+1)*100/int(len(full_test))),1),"%")
            run_time = time.time()
            test()
        except Exception as e:
            for i in range(0,2):
                try:
                    print(e, "retry ("+str(i+1)+"/3)")
                    test()
                    break
                except:
                    pass
        finally:
            print("run time:", round((int(time.time() - run_time)/60),2),"min\n")
            pass

    print("Totla Run Time:", round((int(time.time() - start)/60),2),"min")
    print("failed_test_list: ", failed_test_list)

    ITR_Admin.driver.quit()

    ITR_Admin.signInOut.subadmin_sign_in()
    subadmin_list = [
        DirectMessageBox_List,
        NewDirectMessage_Institution_List,
        DirectMessageSetting_List
        ]

    for a in subadmin_list:
        for b in a:
            try:
                b()
            except:
                print("Exception on " + str(b))
                ITR_Admin.driver.get(ITR_Admin.baseUrl)
                for i in range(0,2):
                    try:
                        b()
                        break
                    except:
                        print("Retry Exception on " + str(b))
                        ITR_Admin.driver.get(ITR_Admin.baseUrl)
                        pass



    # logout
    ITR_Admin.driver.find_element(By.CSS_SELECTOR, "body > nav > div > ul:nth-child(3) > li > a > span").click()
    ITR_Admin.driver.implicitly_wait(5)

    ITR_Admin.admin_login()
    admin_list = [
        Notice_List,
        Auditlog_List,
        MultiReadingCenterRule_List,
        StandardReport_List,
        Institution_List,
        DownloadControl_User_List,
        DownloadControl_Institution_List,
        Specialty_SpecialtyList_List,
        Specialty_InstitutionList,
        UserManagement_SearchFilter_List,
        UserManagement_UserRegistartion_List
        ]

    for a in admin_list:
        for b in a:
            try:
                b()
            except:
                print("Exception on " + str(b))
                ITR_Admin.driver.get(ITR_Admin.baseUrl)
                for i in range(0,2):
                    try:
                        b()
                        break
                    except:
                        print("Retry Exception on " + str(b))
                        ITR_Admin.driver.get(ITR_Admin.baseUrl)
                        pass
                break

    end = time.time()
    print(f"{end - start:.5f} sec")

