import view
from standardcode import db, josa
from CommonModule import main as cm
import socket
import constants
import model, make_table
import logging, traceback, os
logging.basicConfig(level=logging.ERROR)
# path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\img\\'

def before_market(L=[]):
    """장전"""
    before=josa.get_day(2)
    day5=josa.get_day(7)    
    keywords=model.get_keyword(before)
    if len(keywords)==0:
        print('keyword 없음')
        return ''    
    kind=view.get_first_para(keywords, before)
    for row in kind: 
        collect=[]    
        hh=josa.am_pm(constants.HH)
        name1=row[2][0]
        code1=row[2][1]
        eun1=josa.def_connect_word(name1)[0][-1]        
        price1=josa.numberToKoreanWon(row[2][2])
        ratio1=josa.rise_fall_mark(row[2][3])
        name2=row[3][0]
        code2=row[3][1]
        eun2=josa.def_connect_word(name2)[0][-1]        
        price2=josa.numberToKoreanWon(row[3][2])
        ratio2=josa.rise_fall_mark(row[3][3])  
        title=constants.TITLE.format(row[0],name1, ratio1, name2, ratio2)
        para1=constants.PARA1.format(row[0], ', '.join(row[1]))
        #NAME, JOSA, PRICE, RATIO, NAME, JOSA, PRICE, RATIO
        para2=constants.PRE_PARA2.format(name1, eun1, price1, ratio1, name2, eun2, price2, ratio2)
        para3=view.get_trading_signal(code1, code2, before, day5)
        info=view.get_collect(row[4])
        codes = []
        names = []
        for code in row[4]:
            codes.append(code[1])
            names.append(code[0])
        collect.append(row[0])   
        collect.append(codes)
        collect.append(names)
        collect.append(info)
        collect.append(title)
        collect.append(para1)
        collect.append(para2)   
        collect.append(para3)        
        L.append(collect)
    josa.write_log(constants.LOG_PATH, 'before_market()', L)
    return L

def middle_market(L=[]):
    """장중"""
    today=josa.get_day(1)
    day5=josa.get_day(6)
    keywords=model.get_keyword(today)
    if len(keywords)==0:
        print('keyword 없음')
        return ''
    kind=view.get_first_para_2(keywords, today)
    for row in kind:
        collect=[]                
        hh=josa.am_pm(constants.HH)
        name1=row[2][0]
        code1=row[2][1]
        eun1=josa.def_connect_word(name1)[0][-1]        
        price1=josa.numberToKoreanWon(row[2][2])
        ratio1=josa.get_rise_drop(row[2][3])
        name2=row[3][0]
        code2=row[3][1]
        eun2=josa.def_connect_word(name2)[0][-1]        
        price2=josa.numberToKoreanWon(row[3][2])
        ratio2=josa.get_rise_drop(row[3][3])        
        title=constants.TITLE.format(row[0], name1, josa.get_rise_drop(row[2][3]))
        para1=constants.PARA1.format(row[0], ', '.join(row[1]))
        para2=constants.MID_PARA2.format(constants.DAY, hh, constants.MM, name1, eun1, ratio1, price1, name2, eun2, ratio2, price2)                
        para3=view.get_trading_signal(code1, code2, today, day5)        
        info=view.get_collect(row[4])
        codes = []
        names = []
        for code in row[4]:
            codes.append(code[1])
            names.append(code[0])
        collect.append(row[0])   
        collect.append(codes)
        collect.append(names)
        collect.append(info)
        collect.append(title)
        collect.append(para1)
        collect.append(para2)   
        collect.append(para3)                
        L.append(collect)
    josa.write_log(constants.LOG_PATH, 'middle_market()', L)
    return L

def end_market(L=[]):
    """장마감"""
    today=josa.get_day(1)
    day5=josa.get_day(6)
    keywords=model.get_keyword(today)
    if len(keywords)==0:
        print('keyword 없음')
        return ''
    kind=view.get_first_para_2(keywords, today)
    for row in kind:                 
        collect=[]                
        hh=josa.am_pm(constants.HH)
        name1=row[2][0]
        code1=row[2][1]
        eun1=josa.def_connect_word(name1)[0][-1]        
        price1=josa.numberToKoreanWon(row[2][2])
        ratio1=josa.rise_fall_mark(row[2][3])
        name2=row[3][0]
        code2=row[3][1]
        eun2=josa.def_connect_word(name2)[0][-1]        
        price2=josa.numberToKoreanWon(row[3][2])
        ratio2=josa.rise_fall_mark(row[3][3])    
        title=constants.TITLE.format(row[0], name1, ratio1, name2, ratio2)                
        para1=constants.PARA1.format(row[0], ', '.join(row[1]))
        #DATE, NAME, JOSA, PRICE, RATIO, NAME, JOSA, PROCE, RATIO
        para2=constants.END_PARA2.format(constants.DAY, name1, eun1, price1, ratio1, name2, eun2, price2, ratio2)
        para3=view.get_trading_signal(code1, code2, today, day5)        
        info=view.get_collect(row[4])
        codes = []
        names = []
        for code in row[4]:
            codes.append(code[1])
            names.append(code[0])
        collect.append(row[0])   
        collect.append(codes)
        collect.append(names)
        collect.append(info)
        collect.append(title)
        collect.append(para1)
        collect.append(para2)
        collect.append(para3)             
        L.append(collect)
    josa.write_log(constants.LOG_PATH, 'end_market()', L)
    return L

def make_news(keyword:str, codes:str, url:str, title:str, paragraph:str, names:list)->str:
    josa.write_log(constants.LOG_PATH, 'make_news()', codes)
    """뉴스 만드는 구간"""
    NEWS_SN=josa.get_seq()    
    T_NEWS_CRT=constants.NOW_TIME
    cur=db.DB('news_user')
    com=[]    
    for k,code in enumerate(codes):
        name=names[k]
        h='■{}<br>'.format(name)
        com.append(h)
        com.append(cm.run(code))
        cur.cursor.execute(constants.RELACTED_STK_CODE, sn=NEWS_SN, d_crt=constants.TODAY, rsc_code=code)

    content=''.join(paragraph)+constants.HTML.format(keyword, url)
    # print(content)
    print('여기까지')
    cur.cursor.execute(constants.MODULE_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, T_NEWS_CRT=T_NEWS_CRT, NEWS_CODE=constants.NEWS_CODE,
                         NEWS_TITLE=title, NEWS_INP_KIND=constants.NEWS_INP_KIND, RNEWS_CODE=constants.NEWS_CODE, D_EVENT_RNEWS=constants.TODAY)
    cur.cursor.execute(constants.HTML_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, CNTS_TYPE=constants.CNTS_TYPE,
                        D_NEWS_CNTS_CRT=constants.TODAY, T_NEWS_CNTS_CRT=T_NEWS_CRT, NEWS_CNTS=''.join(content), NEWS_CODE=constants.NEWS_CODE, RPST_IMG_URL=url)
    cur.cursor.execute(constants.COMMON_MODULE_SQL, NEWS_SN=NEWS_SN, D_NEWS_CRT=constants.TODAY, CNL_CODE=constants.CHENNEL_CODE, COINFO_CNTS=''.join(com))
    cur.con.commit()
    print('성공')
    return str(NEWS_SN)

def news_auto_sender(sn:str, dt:str, news_code:str):
    josa.write_log(constants.LOG_PATH, 'news_auto_sender()', news_code)
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


if __name__ == "__main__":
    para=before_market()
    
    # middle_market()
    # end_market()
