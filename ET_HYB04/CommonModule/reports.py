import cx_Oracle
from . import constant
from . import db


def get_report(code):
    # DB_RC_TEAM 접속
    # print('11111111111111111111111111111',code)
    cur=db.DB('rc_team')
    cur.cursor.execute(constant.NAVER_ISSUE, stkcode=code)
    info=cur.cursor.fetchall()
    tag_link = list()
    tag_link.append('<br><br>최근 주요 기사')
    # print('최근 주요기사11111111',info)
    if len(info)==0:
        """최근 1개월 동안 특징주 뉴스 없는 경우"""
        tag_link.append('<br>(최근 1개월 동안 특징주 뉴스 없음)')
    else:
        """최근 1개월 동안 특징주 뉴스 있는 경우"""
        for row in info:
            info=row[0]
            date=row[1][4:][:4]
            month=date[:2]
            day=date[2:]
            date = '['+month+'/'+day+']'
            link = '<br><a href="'+row[2]+'"target="_blank">'+date+info+'</a>'
            # print(link)
            tag_link.append(link)
    tag_link.append('<br><br>')

    return tag_link




if __name__=='__main__':
    try:
        c=get_report('003550')
        print(c)

    except Exception as err:
        print('Generate Error')