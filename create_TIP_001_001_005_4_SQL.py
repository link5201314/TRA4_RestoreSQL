#換票
import datetime
today = datetime.date.today()
# nextDay = today + datetime.timedelta(days=2)
# nextDayStr = nextDay.strftime("%Y/%m/%d")
nextDayStr = "2018/09/10"

templateStr_upd1 = """
update ssp_tkt_orders 
set tkt_order_status_code=1,
start_sta_dep_time=to_date('{arg1} 10:00:00','yyyy/mm/dd hh24:mi:ss'),trn_date=to_date('{arg1} 00:00:00','yyyy/mm/dd hh24:mi:ss') ,
trn_ori_sta_dep_time =to_date('{arg1} 10:00:00','yyyy/mm/dd hh24:mi:ss'),trn_dst_sta_arr_time=to_date('{arg1} 12:03:30','yyyy/mm/dd hh24:mi:ss'), 
ORDER_CANCEL_TIME = null, REC_LIMIT_DATE = to_date('{arg1} 10:00:00','yyyy/mm/dd hh24:mi:ss') 
where tkt_rec_no = '{arg2}' and customer_id = '{arg3}';
"""

templateStr_upd2 = """
update ssp_tkt_seat 
set tkt_status_code=1,
chg_tkt_cnt=null,bef_chg_tkt_no=null,ori_tkt_price=null,
dst_sta_arr_time=to_date('{arg1} 12:03:30','yyyy/mm/dd hh24:mi:ss'),
ori_sta_dep_time = to_date('{arg1} 10:00','yyyy/mm/dd hh24:mi'), 
START_STA_DEP_DATE = to_date('{arg1} 12:03:30','yyyy/mm/dd hh24:mi:ss')
where fk_ssp_tkt_orders=(select pk_ssp_tkt_orders from ssp_tkt_orders where tkt_rec_no = '{arg2}' and customer_id = '{arg3}');
"""

templateStr_upd3 = """
delete from ssp_tkt_seat 
where 
fk_ssp_tkt_orders = (select pk_ssp_tkt_orders from ssp_tkt_orders where tkt_rec_no = '{arg1}' and customer_id = '{arg2}') 
and chg_or_cancel_date is not null;
"""

fread = open('tmp\TIP_001_001_005_4.csv', 'r') # r : only read mode
fwrite = open('tmp\TIP_001_001_005_4_restore.sql', 'w+') # w+: would reset content
fread.readline() #skip first line

for line in fread.readlines():
    # print(line)
    if line != "":
        arrItem = line.split(",")
        # print(arrItem)

        args = {'arg1': nextDayStr, 'arg2': arrItem[0], 'arg3': arrItem[1]}
        fullStr1 = templateStr_upd1.format(**args).replace('\n','')
        # print(line, fullStr1)
        fwrite.write(fullStr1 + "\n")

        args = {'arg1': nextDayStr, 'arg2': arrItem[0], 'arg3': arrItem[1]}
        fullStr2 = templateStr_upd2.format(**args).replace('\n','')
        # print(line, fullStr2)
        fwrite.write(fullStr2 + "\n")

        args = {'arg1': arrItem[0], 'arg2': arrItem[1]}
        fullStr3 = templateStr_upd3.format(**args).replace('\n','')
        # print(line, fullStr2)
        fwrite.write(fullStr3 + "\n")

fread.close()
fwrite.close()