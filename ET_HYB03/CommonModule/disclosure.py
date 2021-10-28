import cx_Oracle
import sys
from . import db
from . import constant



def get_dis(code):
    # BARISTA DB 접속
    cur=db.DB('user_barista')
    cur.cursor.execute(constant.RPTNM_SQL, STCKCD=code)
    info=cur.cursor.fetchall()
    tag_link=list()
    tag_link.append('<br><br>최신공시')
    # print(len(info))
    if len(info)==0:
        """최근 1개월 동안 신규 공시 없는 경우"""
        tag_link.append('<br>(최근 1개월 동안 신규 공시 없음)')
    else:
        """최근 1개월 동안 신규 공시 있는 경우"""
        for row in info:
            # print('----------',str(row[2])[:-16][-5:])
            rcp_no = row[0]
            disclosure = row[1]
            date = str(row[2])[:-16][-5:]
            date ='['+str(date)+']'
            # print(date)
            link = '<br><a href="http://dart.fss.or.kr/dsaf001/main.do?rcpNo='+ str(rcp_no)+'"target="_blank">'+date+disclosure+'</a>'
            tag_link.append(link)
            # print(link)
    return tag_link





if __name__=='__main__':
    try:
        s=get_dis('036170')
        print(s)
    except Exception as err:
        print('Generate Error')