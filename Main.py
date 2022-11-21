import ITR_Admin
import sys
from tqdm import tqdm

failed_test_list = []
full_test = [
    # Sign
    ITR_Admin.Sign.Sign_InOut(), # ITR-1
    ITR_Admin.Sign.Rememeber_Me(), # ITR-2
    # Topbar
    ITR_Admin.Topbar.Search_Schedule_List(), # ITR-3
    # Refer
    ITR_Admin.Refer.Hospital_List(), # ITR-7
    ITR_Admin.Refer.Reporter_List(), # ITR-8
    # Search filter
    ITR_Admin.Search_filter.Priority(), # ITR-9
    ITR_Admin.Search_filter.Job_Status(), # ITR-10
    ITR_Admin.Search_filter.Date(), # ITR-11
    ITR_Admin.Search_filter.Patient_Location(), # ITR-12
    ITR_Admin.Search_filter.Patient_ID(), # ITR-13
    ITR_Admin.Search_filter.Patient_Name(), # ITR-14
    ITR_Admin.Search_filter.Age(), # ITR-15
    ITR_Admin.Search_filter.Study_Description(), # ITR-16
    ITR_Admin.Search_filter.Modality(), # ITR-17
    ITR_Admin.Search_filter.Bodypart(), # ITR-18
    ITR_Admin.Search_filter.Department(), # ITR-19
    ITR_Admin.Search_filter.Request_Name(), # ITR-20
    ITR_Admin.Search_filter.Search_All(), # ITR-21
    ITR_Admin.Search_filter.RealTime(), # ITR-22
    ITR_Admin.Search_filter.ShortCut(), # ITR-23
    # Worklist
    ITR_Admin.Worklist.All_Assigned_List(), # ITR-24
    ITR_Admin.Worklist.Not_Assigned_List(), # ITR-25
    ITR_Admin.Worklist.All_List(), # ITR-26
    ITR_Admin.Worklist.Schedule(), # ITR-27
    ITR_Admin.Worklist.Priority(), # ITR-28
    ITR_Admin.Worklist.Canceled(), # ITR-29
    ITR_Admin.Worklist.Refer(), # ITR-30
    ITR_Admin.Worklist.Refer_Cancel(), # ITR-31
    ITR_Admin.Worklist.Refer_Cancel_And_Refer(), # ITR-32
    ITR_Admin.Worklist.Set_Schedule(), # ITR-34
    ITR_Admin.Worklist.Schedule_Cancel(), # ITR-35
    ITR_Admin.Worklist.Revised(), # ITR-36
    ITR_Admin.Worklist.Discard(), # ITR-37
    ITR_Admin.Worklist.Retry_Request(), # ITR-38
    ITR_Admin.Worklist.Columns(), # ITR-39
    ITR_Admin.Worklist.Show_Entries(), # ITR-40
    ITR_Admin.Worklist.Use_Related_Worklist(), # ITR-224
    ITR_Admin.Worklist.Sort_By(), # ITR-41
    # Statistics
    ITR_Admin.Statistics.SearchFilter_Date(), # ITR-44
    ITR_Admin.Statistics.SearchFilter_Hospital(), # ITR-45
    ITR_Admin.Statistics.SearchFilter_Reporter(), # ITR-46
    ITR_Admin.Statistics.SearchFilter_Modality(), # ITR-47
    ITR_Admin.Statistics.Columns(), # ITR-42
    ITR_Admin.Statistics.Show_Entries() # ITR-43
    ]

# Full Test
try:
    for test in tqdm(full_test, desc='ITR Admin Test Processing'):
        test
except:
    failed_test_list.append(current_func_name = sys._getframe().f_code.co_name)
    pass

print("failed_test_list: ", failed_test_list)

ITR_Admin.driver.quit()




# # Sign
# ITR_Admin.Sign.Sign_InOut() # ITR-1
# ITR_Admin.Sign.Rememeber_Me() # ITR-2
# # Topbar
# ITR_Admin.Topbar.Search_Schedule_List() # ITR-3
# # Refer
# ITR_Admin.Refer.Hospital_List() # ITR-7
# ITR_Admin.Refer.Reporter_List() # ITR-8
# # Search filter
# ITR_Admin.Search_filter.Priority() # ITR-9
# ITR_Admin.Search_filter.Job_Status() # ITR-10
# ITR_Admin.Search_filter.Date() # ITR-11
# ITR_Admin.Search_filter.Patient_Location() # ITR-12
# ITR_Admin.Search_filter.Patient_ID() # ITR-13
# ITR_Admin.Search_filter.Patient_Name() # ITR-14
# ITR_Admin.Search_filter.Age() # ITR-15
# ITR_Admin.Search_filter.Study_Description() # ITR-16
# ITR_Admin.Search_filter.Modality() # ITR-17
# ITR_Admin.Search_filter.Bodypart() # ITR-18
# ITR_Admin.Search_filter.Department() # ITR-19
# ITR_Admin.Search_filter.Request_Name() # ITR-20
# ITR_Admin.Search_filter.Search_All() # ITR-21
# ITR_Admin.Search_filter.RealTime() # ITR-22
# ITR_Admin.Search_filter.ShortCut() # ITR-23
# # Worklist
# ITR_Admin.Worklist.All_Assigned_List() # ITR-24
# ITR_Admin.Worklist.Not_Assigned_List() # ITR-25
# ITR_Admin.Worklist.All_List() # ITR-26
# ITR_Admin.Worklist.Schedule() # ITR-27
# ITR_Admin.Worklist.Priority() # ITR-28
# ITR_Admin.Worklist.Canceled() # ITR-29
# ITR_Admin.Worklist.Refer() # ITR-30
# ITR_Admin.Worklist.Refer_Cancel() # ITR-31
# ITR_Admin.Worklist.Refer_Cancel_And_Refer() # ITR-32
# ITR_Admin.Worklist.Set_Schedule() # ITR-34
# ITR_Admin.Worklist.Schedule_Cancel() # ITR-35
# ITR_Admin.Worklist.Revised() # ITR-36
# ITR_Admin.Worklist.Discard() # ITR-37
# ITR_Admin.Worklist.Retry_Request() # ITR-38
# ITR_Admin.Worklist.Columns() # ITR-39
# ITR_Admin.Worklist.Show_Entries() # ITR-40
# ITR_Admin.Worklist.Use_Related_Worklist() # ITR-224
# ITR_Admin.Worklist.Sort_By() # ITR-41
# # Statistics
# ITR_Admin.Statistics.SearchFilter_Date() # ITR-44
# ITR_Admin.Statistics.SearchFilter_Hospital() # ITR-45
# ITR_Admin.Statistics.SearchFilter_Reporter() # ITR-46
# ITR_Admin.Statistics.SearchFilter_Modality() # ITR-47
# ITR_Admin.Statistics.Columns() # ITR-42
# ITR_Admin.Statistics.Show_Entries() # ITR-43
