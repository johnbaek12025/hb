import view
from standardcode import josa, db
import constants
import model
from datetime import datetime
from CommonModule import main as cm
import socket

def make_para(today:str, range1:int, range2:int, L=[])->list:
    info=view.get_para(today, range1, range2)
    for i in info:
        collect=[]
        fore=i[5]    
        org=i[6]
        name=i[0]
        code=i[1]
        price=josa.numberToKoreanWon(i[2])
        ratio=i[3]
        header=i[4]        
        deta = i[7]
        rate=josa.get_rise_drop(ratio)
        title=constants.TITLE.format(name, rate, deta)
        # print(f"title is \n {title} \n")
        eun=josa.def_connect_word(name)[0][-1]                
        #name, josa, day, hour, minute, ratio, price
        hh=josa.am_pm(constants.NOW[:2])        
        mm=constants.NOW[2:]        
        para1=constants.PARA1.format(name, eun, constants.DAY, hh, mm, rate, price)
        # print(f"first para is \n {para1} \n")
        ro=josa.def_connect_word(header)[-2]
        if len(header)<3:
            para2=''
        else:
            para2=constants.PARA2.format(name, eun, header, ro)        
        if len(fore) ==0 and len(org)==0:
             para3=''
             net=view.get_sales(code, constants.DAY5)
        else:
            eur=josa.def_connect_word(name)[2][-1]
            para3=constants.PARA3.format(fore, org)
            net=view.get_sales(code, constants.DAY5)
        # print(f"second para is \n {para2} \n")
        # print(f"third para is \n {para3} \n")
        # print(f"fourth para is \n {net} \n")
        # print('\n')
        collect.append(code)                
        collect.append(title)
        collect.append(ratio)
        collect.append(para1)
        collect.append(para2)
        collect.append(para3)
        collect.append(net)
        L.append(collect)
    return L

def get_info(code:str, path:str, ratio:str)->list:
    """테이블 만들기
        거래량 대비 = 순매매량/해당 날짜 거래량
        오늘 잠정"""    
    info=model.get_today_amount(code)
    if not info:
        josa.write_log(constants.LOG_PATH, f"{code} no data", f"the amount of trading of {code} is not existed today")
        return ''
    amount = []           
    if info[0][3] == 0:#거래량
        print('거래량이 0이므로 해당종목 뉴스 생성 않함')
        return ''
    proportion1= round(int(info[0][1])/int(info[0][3]) *100,2)
    proportion2 = round(int(info[0][2]) / int(info[0][3]) * 100,2)
    ele=[info[0][0] , ratio, info[0][1], proportion1, info[0][2], proportion2 ]
    amount.append(ele)
    cont=model.get_continuous_amount(code, constants.DAY5, constants.YESTERDAY)
    rate=model.get_ratio(code,constants.DAY5, constants.YESTERDAY)
    k=0
    for i in cont:
        if None in i:
            print('테이블 만들기위한 정보 추출과정에서 None이 나옴')
            return ''
        ele2=[]        
        if int(rate[k][1])==0:
            continue
        ele2.append(i[0])
        ele2.append(rate[k][0])
        ele2.append(i[1])
        proportion3=round(int(i[1])/int(rate[k][1])*100,2)
        ele2.append(proportion3)
        ele2.append(i[2])
        proportion4 = round(int(i[2]) / int(rate[k][1]) * 100, 2)
        ele2.append(proportion4)
        amount.append(ele2)
        k=k+1
    if len(amount)!=5:
        print('5일치의 데이터가 생성이 안됐으므로 테이블 생성 안함')
        return ''        
    #info:list, path:str, news_code:str,code:str
    img_path=josa.get_table(amount, path, constants.NEWS_CODE,code)#테이블 만드는 구간            
    return img_path


def make_news(code:str, url:str, title:str, paragraph:str)->str:
    """뉴스 만드는 구간
    ⓐparameter로 테마특징주의 타이틀, 첫번째 문단, 차트링크, 두번째문단, 공통모듈을 받는다.
    ⓑget_db.get_seq로 NEWS_SN을 위해 query 작동
    ⓒT_NEWS_CRT를 위해 현재 시간을 constants.NOW_TIME변수를 가져온다.
    ⓓ첫번째문단과 링크, 두번째문단 그리고 공통모듈을 묶는다.
    ⓔ공통모듈은 나중에 다른 테이블에 INSERT를 할 것이다.
    ⓕRTBL_NEWS_INFO와 RTBL_NEWS_CNTS_ATYPE에서 insert """
    NEWS_SN=josa.get_seq()    
    T_NEWS_CRT=datetime.now().strftime("%H%M%S")
    com=cm.run(code)
    content=paragraph
    cur=db.DB('news_user')
    print('여기까지')
    cur.cursor.execute(constants.MODULE_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, T_NEWS_CRT=T_NEWS_CRT, NEWS_CODE=constants.NEWS_CODE,
                       STK_CODE=code, NEWS_TITLE=title, NEWS_INP_KIND=constants.NEWS_INP_KIND, RNEWS_CODE=constants.NEWS_CODE, D_EVENT_RNEWS=constants.TODAY)
    cur.cursor.execute(constants.HTML_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, CNTS_TYPE=constants.CNTS_TYPE,
                       D_NEWS_CNTS_CRT=constants.TODAY, T_NEWS_CNTS_CRT=T_NEWS_CRT, NEWS_CNTS=content, NEWS_CODE=constants.NEWS_CODE, RPST_IMG_URL=url)
    cur.cursor.execute(constants.COMMON_MODULE_SQL, NEWS_SN=NEWS_SN, D_NEWS_CRT=constants.TODAY, CNL_CODE=constants.CHENNEL_CODE, COINFO_CNTS=''.join(com))
    cur.con.commit()
    print('성공')
    return str(NEWS_SN)


def news_auto_sender(sn:str, dt:str, news_code:str):
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

if __name__=='__main__':
    make_para(constants.TODAY, 1, 50, '0950', '1050')