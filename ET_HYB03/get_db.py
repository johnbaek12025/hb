import constants
import db
import josa

#:NEWS_CNTS:IMG, :CODE:TITLE
def get_news(code):
    sql = f"""
        select  * 
        from    RTBL_news_info 
        where   news_code ='{constants.NEWS_CODE}' 
        AND     STK_CODE = {code} 
        AND     D_NEWS_CRT = '{constants.TODAY}'
        """
    cur=db.DB('news_user')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def trade_day_check():
    """오늘 휴장인지 아닌지 TRADE_DAY 테이블을 통해 확인"""
    sql = f"""
        select  NVL(max(DATEDEAL), '휴장') 
        from    TRADE_DAY 
        where   DATEDEAL = {constants.TODAY}
        """
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    datedeal_tuple_list = cur.cursor.fetchall()
    datedeal = datedeal_tuple_list[0][0]
    return datedeal

def get_seq():
    """시퀀스 생성"""
    sql = f"""
        SELECT  NEWS_USER.RTBL_NEWS_SEQUENCE.NEXTVAL 
        FROM    DUAL
        """
    seq=db.DB('news_user')
    josa.write_log(constants.LOG_PATH, 'sequence', sql)
    seq.cursor.execute(sql)    
    seq_tuple_list = seq.cursor.fetchall()
    seq = seq_tuple_list[0][0]
    return seq

def get_kospi():
    """A3_CURPRICE의 FLUCT_RATIO의 수 결정을 위한 코스피 등락률"""
    sql = f"""
        select  case when  total>0  then total else 0 end as total
        from    (
                    select round(sum(ratio)/count(*),2) as total 
                    from   rkospi 
                    where  datedeal='{constants.TODAY}'
                )
        """
    josa.write_log(constants.LOG_PATH, 'kospi_ratio', sql)
    cur=db.DB('rc_team')    
    cur.cursor.execute(sql)
    ratio=cur.cursor.fetchall()
    ratio=ratio[0][0]
    return ratio

def check_trade_day():
    sql = f"""
        SELECT  *
        FROM    TRADE_DAY
        WHERE   DATEDEAL ='{constants.TODAY}'
        """
    josa.write_log(constants.LOG_PATH, 'trade_day', sql)
    cur = db.DB('rc_team')
    cur.cursor.execute(sql)
    day = cur.cursor.fetchone()
    return day

def get_previous_day():
    """EBEST_THEME_MAPPING을 SELECT하기 위해 이전 영업일을 구한다."""
    sql = f"""
        select  NVL(max(DATEDEAL), '휴장') 
        from    TRADE_DAY 
        WHERE   DATEDEAL<'{constants.TODAY}'
        """
    josa.write_log(constants.LOG_PATH, 'previous_day', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    pre_day=cur.cursor.fetchall()
    pre_day = pre_day[0][0]
    # print(pre_day)
    return pre_day


def get_kind(before_day, ratio):
    """종목 추출
    ⓐconstants.EXTRACT_STK의 받아온 비율과 이전 영업일을 통해query를 작동
    ⓑ종목명, 종목코드, 전일대비 상승률, 기업개요 리스트를 return
    ⓒ혹여나 종목이 존재하지 않을경우를 대비해 종목이 없는 경우 오류 값을 반환"""
    sql = f"""
        SELECT  A.STK_NAME, 
                A.STK_CODE, 
                round(A.FLUCT_RATIO,1) as ratio, 
                E.HEADER
        FROM    A3_CURPRICE A
        INNER JOIN (
                        SELECT  DISTINCT STKCODE
                        FROM    EBEST_T1533 B
                        INNER JOIN EBEST_THEME_MAPPING C
                        ON B.THEME_CODE =C.THEMECODE               
                        WHERE   C.DATEDEAL = {before_day}
                        AND     B.DATEDEAL='{constants.TODAY}'
                        AND     B.UPRATE >= '50'
                        AND     AVGDIFF >=  3
                        and     b.timedeal between '{constants.PRVIOUS_TIME}' and '{constants.NOW_TIME}'
                    ) D
        ON A.STK_CODE = D.STKCODE AND  A.FLUCT_RATIO >= {ratio}
        inner join  FI_OUTLINE_CONT E
                ON  E.CODE = A.STK_CODE
        ORDER BY RATIO DESC
        """
    josa.write_log(constants.LOG_PATH, 'extracted_stk', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    if len(info)==0:
        print('선정된 종목이 존재 안함')
        alert='선정된 종목이 존재 안함'
        return alert
    else:
        pass
    return info

def get_theme(before_day, stk_code):
    """해당 종목의 상승률 높은 테마 추출
    ⓐ이전 영업일과 선정된 종목의 종목 코드를 parameter받아옴
    ⓑparameter를 이용해 constants.EXTRACT_HIGH_THEM의 query에서 themecode, themename, 종목 코드를 받아온다.
    ⓒ받아온 테마코드, 테마네임, 종목코드를 리스트로 묶어서 return"""
    sql = f"""
        SELECT  * 
        FROM    (
                    SELECT  E.THEME_CODE, 
                            F.THEMENAME, 
                            F.STKCODE  
                    FROM    EBEST_T1533 E
                    INNER JOIN  EBEST_THEME_MAPPING F
                    ON  E.THEME_CODE = F.THEMECODE 
                    WHERE   E.UPRATE >= '50' AND E.AVGDIFF>='3' 
                    AND     F.STKCODE = {stk_code}
                    AND     E.DATEDEAL = '{constants.TODAY}' 
                    AND     F.DATEDEAL = {before_day}
                    ORDER BY E.AVGDIFF DESC
                )
        WHERE ROWNUM<=1
        """
    josa.write_log(constants.LOG_PATH, 'get_theme', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    # print('테마:',info[0])
    themename=info[0][1]
    themecode=info[0][0]
    stk_code=info[0][2]
    theme=[themename, themecode, stk_code]
    return theme

def get_side(before_day, themecode, code):
    """관련종목 추출
    ⓐ이전 영업일, 테마코드, 선정된 종목의 종목코드를 parameter로 받는다.
    ⓑconstants.EXTRACT_REALTED_STK의 query를 select하는데 parameter를 사용
    ⓒ받아온 것을 for문 안에서 list선언 후 묶고, 그 list들을 차례대로 list로 다시 묶는다.
    ⓓ각 선정된 종목들의 테마와 관련된 종목들로 묶여진 list를 retunn"""
    sql = f"""
            select  *
            from    (
                        SELECT  C.STK_NAME, 
                                round(C.FLUCT_RATIO,1) as ratio
                        FROM    A3_CURPRICE C
                        INNER JOIN
                                    (
                                        SELECT  DISTINCT B.STKCODE
                                        FROM    EBEST_T1533 A
                                        INNER JOIN  EBEST_THEME_MAPPING B
                                        ON          A.THEME_CODE = B.THEMECODE
                                        WHERE   A.DATEDEAL='{constants.TODAY}' AND B.DATEDEAL = {before_day}
                                        AND     UPRATE>='50' AND AVGDIFF>='3' 
                                        and     b.themecode={themecode}
                                    ) D
                        ON  C.STK_CODE =D.STKCODE
                        WHERE   FLUCT_RATIO>='2' 
                        and     stk_code not in {code}
                        order by  fluct_ratio desc
                    )
            where rownum<=3
            """
    side_list=[]
    josa.write_log(constants.LOG_PATH, 'get_theme', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    for row in info:
        # print(row[0],row[1])
        side=[row[0],row[1]]
        side_list.append(side)

    return side_list

if __name__=='__main__':
    ratio=get_kospi()
    pday=get_previous_day()
    # print(pday)
    # print(ratio)
    if int(ratio)<=1:
        stk_list=get_kind(pday, '5')
    else:
        stk_list=get_kind(pday, '7')
    # print('종목 코드, 종목 명,', stk_list)
    # theme=INFO.get_theme('', pday, stk_list[0][1])
    # print(theme)
    # side=INFO.get_side('',pday, theme)
    # print(side)