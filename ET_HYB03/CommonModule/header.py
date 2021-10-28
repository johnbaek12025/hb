import cx_Oracle
from . import constant
from . import db

def get_header(code):
    "# TP_STOCK DB 접속"
    cur=db.DB('tp_stock')
    cur.cursor.execute(constant.SUMMARY_SQL, code=code)
    info = cur.cursor.fetchall()

    code = info[0][0]
    link = 'https://finance.naver.com/item/coinfo.nhn?code='+code
    header = info[0][1]

    if len(header) == 0:
        header = '자세히보기 ==>'

    tag='기업개요 : <a href='+'"'+link+'"'+' target="_blank">'+header+'</a>'


    if len(info) == 0:
        header = '자세히보기 ==>'
        tag=constant.TAG1.format(constant.LINK1.format(code),header )
        return tag
    code = info[0][0]
    header = info[0][1]
    tag = constant.TAG1.format(constant.LINK1.format(code), header)

    # print(tag)
    return tag



if __name__=='__main__':
    try:
        h=get_header('003550')
        print(h)

    except Exception as err:
        print('Generate Error')





