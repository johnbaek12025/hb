import contents
import db
import constants
import get_db
import sys
from CommonModule import main as cm
import socket, josa

def build_up():
    """테마특징주 기사 합치
    ⓐ코스피의 평균 등락률 비교
    ⓑ코스피 등락률 1%초과 또는 이하인경우에 따라 get_db.get_kind에 5나 7을 parameter로 보낸다.
    ⓒ stk_list에 종목명 종목코드, 전일대비 등락율, 기업개요 list를 저장
    ⓓstk_list에 선정된 종목에 대한 정보가 저장이 안되면 '선정된 종목이 존재 안함'을 return
    ⓔ선정된 종목이 존재하는 경우 종목코드를 get_db.get_theme에 parameter로 보낸다.
    ⓕ테마명, 테마코드, 종목코드 list를 theme에 저장
    ⓖ해당 테마에 속한 선정된 종목이외의 종목들을 출력을 위해 
      get_db.get_side에 테마코드와 종목코드를 parameter로 보낸다.
    ⓗ관련종목의 종목명과 전일대비 등락률 list를 rname에 저장
    ⓘ해당종목의 차트를 위해 link를 coding
    ⓙ위에서 구한 테마명, 선정된 종목명, 해당 종목의 전일대비 등락률, 기업개요,
      테마관련 다른 종목들을 contents.get_contents에 parameter로 보낸다.
    ⓚ조립을 하고 그것을 link_list와 return"""
    content=[]
    #코스피 평균 등락률 출력
    cur = db.DB('rc_team')
    cur.cursor.execute(constants.KOSPIRATIO)
    josa.write_log(constants.LOG_PATH, 'KOSPIRATIO_SQL', constants.KOSPIRATIO)
    kospi = cur.cursor.fetchall()
    kospi = kospi[0][0]    
    josa.write_log(constants.LOG_PATH, 'kospi_index', kospi)
    # print(type(kospi), kospi)
    #이전 영업기준일 출력
    pday = get_db.get_previous_day()
    # 코스피 평균 등락률에 따른 종목의 전일대비 등락율
    if kospi <= 1:
        stk_list = get_db.get_kind(pday, '3')
        josa.write_log(constants.LOG_PATH, 'stk_list_3%', stk_list)
    else:
        stk_list = get_db.get_kind(pday, '5')
        josa.write_log(constants.LOG_PATH, 'stk_list_5%', stk_list)

    if stk_list == '선정된 종목이 존재 안함':
        print('선정된 종목이 존재 안함')
        alert = '선정된 종목이 존재 안함'
        return alert
    josa.write_log(constants.LOG_PATH, 'build_up()', stk_list)
    for row in stk_list:
        # print('선정된 종목:', row)
        theme = get_db.get_theme(pday, row[1])
        # print('선정된 종목의 평균등락률이 가장 높은 테마명:', theme)
        rname = get_db.get_side(pday, theme[1], theme[2])
        # print('위의 테마명에 해당 하는 선정된 종목 이외의 종목들:', rname)
        # # (themename, name, ratio, summary, kind)
        # print(theme[0])
        # print(row[0])
        # print(str(row[2]))
        # print(row[3])
        # print(len(rname))
        link=constants.LINK1+row[1]+constants.LINK2
        #themename, name, ratio, summary, kind => 테마명, 선정된 종목명, 해당 종목의 전일대비 등락률, 기업개요, 테마관련 다른 종목들
        common_module=cm.run(row[1])
        # print(common_module)
        title,first, second = contents.get_contents(theme[0], row[0], str(row[2]), row[3], list(rname))
        cont=[]
        cont.append(row[1])
        cont.append(title)
        cont.append(first)
        cont.append(link)
        cont.append(second)
        cont.append(common_module)
        content.append(cont)
    josa.write_log(constants.LOG_PATH, 'build_up()', content)
    return content

def make_news(code,title, first, link, second, module)->str:
    # print(code)
    # print(title)
    # print(first)
    # print(link)
    # print(second)
    # print(module)
    """뉴스 만드는 구간
    ⓐparameter로 테마특징주의 타이틀, 첫번째 문단, 차트링크, 두번째문단, 공통모듈을 받는다.
    ⓑget_db.get_seq로 NEWS_SN을 위해 query 작동
    ⓒT_NEWS_CRT를 위해 현재 시간을 constants.NOW_TIME변수를 가져온다.
    ⓓ첫번째문단과 링크, 두번째문단 그리고 공통모듈을 묶는다.
    ⓔ공통모듈은 나중에 다른 테이블에 INSERT를 할 것이다.
    ⓕRTBL_NEWS_INFO와 RTBL_NEWS_CNTS_ATYPE에서 insert """
    NEWS_SN=get_db.get_seq()
    T_NEWS_CRT=constants.NOW_TIME
    content = ''.join(first) + '<br><br>' + link + '<br><br>' + ''.join(second) + '<br><br>'
    cur=db.DB('news_user')

    cur.cursor.execute(constants.MODULE_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, T_NEWS_CRT=T_NEWS_CRT, NEWS_CODE=constants.NEWS_CODE,
                       STK_CODE=code,NEWS_TITLE=title, NEWS_INP_KIND=constants.NEWS_INP_KIND, RNEWS_CODE=constants.NEWS_CODE, D_EVENT_RNEWS=constants.NOW_TIME)
    cur.cursor.execute(constants.HTML_INSERT_SQL, D_NEWS_CRT=constants.TODAY, NEWS_SN=NEWS_SN, CNTS_TYPE=constants.CNTS_TYPE,
                        D_NEWS_CNTS_CRT=constants.TODAY, T_NEWS_CNTS_CRT=constants.NOW_TIME, NEWS_CNTS=content, NEWS_CODE=constants.NEWS_CODE, RPST_IMG_URL=link)
    cur.con.commit()

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
    cont=build_up()
    #[title + first + link + second + common_module]
    for row in cont:
        print(row)