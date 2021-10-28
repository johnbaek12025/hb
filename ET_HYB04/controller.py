import view
import model
import constants
import josa
import db
from datetime import datetime
import socket, os, sys
path=os.path.abspath('.\\img')

def para1(curprice, L=[]):
    josa.write_log(constants.LOG_PATH,'para1()', curprice)
    org = view.get_para1(curprice, model.get_org, model.abs_org_value, '기관') 
    fore = view.get_para1(curprice, model.get_for, model.abs_for_value, '외국인')    
    for row in fore:
        if None in row:
            print('첫번째 문장의 첫번째 문단의 None 값 포함')
            continue
        ele=[]
        # print(row)
        name=row[0]
        code=row[1]
        price=row[2]
        ratio=row[3]
        amount=row[4]
        who=row[5]
        # 날짜 시, 분, 종목명, 코드, 조사, 기관or 외국인, 순매수량, 비율, 현재가
        eun=josa.def_connect_word(name)[0][-1]
        buy=josa.numberToKoreanZoo(amount)
        price=josa.numberToKoreanWon(price)        
        info=constants.PARA1.format(constants.DAY, constants.HH, constants.MM, name, code, eun,who, buy ,ratio, price)
        ele.append(code)
        ele.append(ratio)
        ele.append(name)
        ele.append(who)
        ele.append(buy)
        ele.append(info)
        L.append(ele)
    return L

def para2(curprice, L=[]):
    josa.write_log(constants.LOG_PATH,'para2()', curprice)
    fore=view.get_para2(curprice, model.today_for, model.get_for_continuous, '외국인')
    org=view.get_para2(curprice, model.today_org, model.get_org_continuous, '기관')
    com=view.comapare_big(fore, org)
    # print('===========================',com)
    for row in com:
        # print(row)
        ele=[]
        name = row[0]
        code = row[1]
        price = row[2]
        ratio = row[3]
        who = row[4]
        amount = row[5]
        term = row[6]
        # 날짜, 시간, 분, 종목명, 코드, 조사, 비율, 가격, 기관or 외국인, 연속일, 누적 순매수량
        eun = josa.def_connect_word(name)[0][-1]
        buy = josa.numberToKoreanZoo(amount)
        price = josa.numberToKoreanWon(price)
        info = constants.PARA2.format(constants.DAY, constants.HH, constants.MM, name, code,eun, ratio, price, who, term, buy)
        # print(info)
        ele.append(code)
        ele.append(ratio)
        ele.append(name)
        ele.append(who)
        ele.append(term)
        ele.append(info)
        L.append(ele)
    return L

def para3(curprice, L=[]):
    josa.write_log(constants.LOG_PATH,'para3()', curprice)
    together=view.get_now(curprice)
    for row in together:
        if None in row:
            print('첫번째 문장의 세번째 문단의 None 값 포함')
            continue
        ele = []
        name = row[0]
        code = row[1]
        price = row[2]
        ratio = row[3]       
        org_amount = row[4]
        fore_amount = row[5]

        # 날짜, 시, 분, 종목명, 코드, 조사, 외국인 순매수량, 기관 순매수량, 비율, 가격
        eun = josa.def_connect_word(name)[0][-1]
        org_buy = josa.numberToKoreanZoo(org_amount)
        fore_buy = josa.numberToKoreanZoo(fore_amount)
        price = josa.numberToKoreanWon(price)
        info=constants.PARA3.format(constants.DAY, constants.HH, constants.MM, name, code,eun, fore_buy, org_buy, ratio, price)
        # print(info)
        ele.append(code)
        ele.append(ratio)
        ele.append(name)
        ele.append(info)
        L.append(ele)
    return L

def second_para(code):
    josa.write_log(constants.LOG_PATH,'second_para()', code)
    # 보험기타금융 , 투신, 은행, 연기금
    L=[]    
    amount=view.get_second(code)
    ele=[]
    # print('세부 기관별------------------------------------------------------------------------------------',amount[0])
    if amount[0][0]==0 and amount[0][1]==0 and amount[0][2]==0 and amount[0][3]==0:
            L.append('')
            return L
    else:
        if amount[0][0] != 0:
            buy=josa.numberToKoreanZoo(amount[0][0])
            div=josa.net(buy)
            i1='보험 등에서 '+div
            ele.append(i1)
        if amount[0][1] != 0:
            buy = josa.numberToKoreanZoo(amount[0][1])
            div = josa.net(buy)
            i2='투자신탁에서 '+div
            ele.append(i2)
        if amount[0][2] != 0:
            buy = josa.numberToKoreanZoo(amount[0][2])
            div = josa.net(buy)
            i3='은행에서 '+div
            ele.append(i3)
        if amount[0][3] != 0:
            buy = josa.numberToKoreanZoo(amount[0][3])
            div = josa.net(buy)
            i4='연기금이 '+div
            ele.append(i4)
        info=constants.SECOND_PARA.format(', '.join(ele))
        L.append(info)
        return L

def make_news(code, title, content, second, html, com)->str:
    josa.write_log(constants.LOG_PATH,'make_news()', code)
    """뉴스 만드는 구간
    ⓐparameter로 테마특징주의 타이틀, 첫번째 문단, 차트링크, 두번째문단, 공통모듈을 받는다.
    ⓑget_db.get_seq로 NEWS_SN을 위해 query 작동
    ⓒT_NEWS_CRT를 위해 현재 시간을 constants.NOW_TIME변수를 가져온다.
    ⓓ첫번째문단과 링크, 두번째문단 그리고 공통모듈을 묶는다.
    ⓔ공통모듈은 나중에 다른 테이블에 INSERT를 할 것이다.
    ⓕRTBL_NEWS_INFO와 RTBL_NEWS_CNTS_ATYPE에서 insert """
    NEWS_SN=josa.get_seq()
    T_NEWS_CRT=datetime.now().strftime("%H%M%S")
    content = ''.join(content) + ''.join(second)  + html
    # News_code, News_code, stk_code
    link=constants.URL.format(constants.NEWS_CODE, constants.NEWS_CODE,code)
    cur=db.DB('news_user')
    # print('여기까지')
    cur.cursor.execute(constants.MODULE_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, T_NEWS_CRT=T_NEWS_CRT, NEWS_CODE=constants.NEWS_CODE,
                       STK_CODE=code, NEWS_TITLE=title, NEWS_INP_KIND=constants.NEWS_INP_KIND, RNEWS_CODE=constants.NEWS_CODE, D_EVENT_RNEWS=constants.TODAY)
    cur.cursor.execute(constants.HTML_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, CNTS_TYPE=constants.CNTS_TYPE,
                       D_NEWS_CNTS_CRT=constants.TODAY, T_NEWS_CNTS_CRT=T_NEWS_CRT, NEWS_CNTS=content, NEWS_CODE=constants.NEWS_CODE, RPST_IMG_URL=link)
    cur.cursor.execute(constants.COMMON_MODULE_SQL, NEWS_SN=NEWS_SN, D_NEWS_CRT=constants.TODAY, CNL_CODE=constants.CHENNEL_CODE, COINFO_CNTS=''.join(com))
    cur.con.commit()    
    return str(NEWS_SN)

def news_auto_sender(sn:str, dt:str, news_code:str):
    josa.write_log(constants.LOG_PATH,'news_auto_sender()', sn)
    """
    기존 전송 시스템과 새로운 전송 시스템 양쪽 모두 호출
    기존 전송 시스템 "121.254.150.89", 6603
    새로운 전송 시스템 "121.254.150.199" 6603 (새로운 전송 시스템은 이중화 되어 있기 때문에 L4 호출)
    """
    server_list = [("121.254.150.89", 6603), ("121.254.150.199", 6603)]
    
    
    for ser_ip, ser_port in server_list:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ser_ip, ser_port))
        s.settimeout(3)
        send_data = '<?xml version="1.0" encoding="euc-kr"?> <news_info sn="' + sn + '" news_code="'+ news_code + '" date="' + dt + '" />'
        s.send(send_data.encode())
        data = s.recv(4096)
        print("data recv: ", data)
        s.close()

if  __name__=='__main__':    
    curprice=model.get_curprice()
    # info=para1(curprice)
    # info=para2(curprice)
    info=para3(curprice)
    for row in info:
        print(row)
        second=second_para(row[0])
        print(second)
        info=view.get_info(row[0], row[1])

