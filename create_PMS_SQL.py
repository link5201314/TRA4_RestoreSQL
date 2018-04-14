supplyStart ="2018-09-01"
supplyEnd = "2018-09-30"
trainDate = "201809__"
creator = "ALLPT01"

templateStr_del = """
delete from PMS_SUPPLY_COND where (to_char(sdate,'yyyymm') = '{0}' or to_char(EDATE,'yyyymm') = '{1}');
 -- and CREATOR = '{2};  --Clear Old Data'
""".format(trainDate[:6], trainDate[:6], creator).replace('\n','')

print(templateStr_del)

templateStr_Ins = """
Insert into PMS_SUPPLY_COND (PK_PMS_SUPPLY_COND, TRAIN_NO,SUPPLY_TIME,SDATE,EDATE,FK_RESTAURANT_CODE,SUPPLY_STA_CODE,SUPPLY_LIMIT,ORI_STA_01,ORI_STA_02,DST_STA_01,DST_STA_02,CREATOR,CREATE_DATE,UPDATE_DATE,LAST_MODIFIER,ACTIVE) values (PMS_SUPPLY_COND_sq.nextval, 
'{arg4}','D',to_date('{arg1} 00:00:00','yyyy-mm-dd HH24:MI:SS'),to_date('{arg2} 23:59:59','yyyy-mm-dd HH24:MI:SS'),'A001','1210',999,
(select START_STA_CODE from tms_op_trn where trn_op_no like '{arg3}{arg4}' and rownum<=1),
(select END_STA_CODE from tms_op_trn where trn_op_no like '{arg3}{arg4}' and rownum<=1),
(select START_STA_CODE from tms_op_trn where trn_op_no like '{arg3}{arg4}' and rownum<=1),
(select END_STA_CODE from tms_op_trn where trn_op_no like '{arg3}{arg4}' and rownum<=1),
'{arg5}',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,'PMS_LV006','Y');
"""

fread = open('tmp\PMS_TrainNo.txt', 'r') # r : only read mode
fwrite = open('tmp\PMS_restore.sql', 'w+') # w+: would reset content

fwrite.write(templateStr_del + "\n")

for line in fread.readlines():
    # print(line)
    if line != "":
        args = {'arg1': supplyStart, 'arg2': supplyEnd, 'arg3': trainDate, 'arg4': line, 'arg5': creator}
        fullStr = templateStr_Ins.format(**args).replace('\n','')
        print(line, fullStr)
        fwrite.write(fullStr + "\n")

fread.close()
fwrite.close()

