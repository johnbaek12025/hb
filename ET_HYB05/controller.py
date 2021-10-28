import constants
from datetime import datetime
import josa
import sys
from CommonModule import main as cm
import db, socket


def make_news(code:str, url:str, title:str, paragraph:str)->str:
    josa.write_log(constants.LOG_PATH, 'make_news()', code)
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
    josa.write_log(constants.LOG_PATH, 'auto_sender()', news_code)
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