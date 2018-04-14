
"""
update tms_op_seat_od od
set fk_tms_seat_kind_code = '{arg1}',  --座位種類_舊
    seat_status_code = (select case when is_saleable = 'Y' then 1 else 2 end from tms_seat_kind_code kind where od.fk_tms_seat_kind_code = kind.pk_tms_seat_kind_code)
where
    trn_op_no = '{arg2}'              --年月日8碼+車次'
    and seat_ori_sta_code = '{arg3}'  --起站
    and seat_dst_sta_code = '{arg4}'  --迄站
    and car_no = '{arg5}'               --車號
    and seat_no = '{arg6}'              --座位號
"""

templateStr_upd = """
update tms_op_seat_od  od
 set fk_tms_seat_kind_code = '{arg1}', 
    seat_status_code = (select case when is_saleable = 'Y' then 1 else 2 end from tms_seat_kind_code kind where od.fk_tms_seat_kind_code = kind.pk_tms_seat_kind_code)
 where
    trn_op_no = '{arg2}' 
    and seat_ori_sta_code = '{arg3}' 
    and seat_dst_sta_code = '{arg4}' 
    and car_no = '{arg5}' 
    and seat_no = '{arg6}'; 
"""

fread = open('tmp\TMS_001_002_001_001.csv', 'r') # r : only read mode
fwrite = open('tmp\TMS_001_002_001_001_restore.sql', 'w+') # w+: would reset content
fread.readline() #skip first line

for line in fread.readlines():
    # print(line)
    if line != "":
        arrItem = line.split(",")
        # print(arrItem)

        args = {'arg1': arrItem[8], 'arg2': arrItem[0].replace(".","")+arrItem[1], 'arg3': arrItem[2], 'arg4': arrItem[3], 'arg5': arrItem[4], 'arg6': arrItem[5]}
        fullStr = templateStr_upd.format(**args).replace('\n','')
        # print(line, fullStr)
        fwrite.write(fullStr + "\n")

fread.close()
fwrite.close()