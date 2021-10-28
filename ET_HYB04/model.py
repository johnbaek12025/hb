import db
import josa
import constants

def get_curprice():
    """전일비 3% 이상 종목"""
    sql = f"""
        SELECT STK_NAME, 
                STK_CODE, 
                CLOSE, 
                ROUND(FLUCT_RATIO,1)FLUCT_RATIO 
        FROM    A3_CURPRICE 
        WHERE   FLUCT_RATIO >= 3 
        AND     D_CNTR = '{constants.TODAY}'
        """
    josa.write_log(constants.LOG_PATH, 'curprice', sql)
    cur=db.DB("rc_team")
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def check_trade_day():
    sql = f"""
        SELECT  *
        FROM    TRADE_DAY
        WHERE   DATEDEAL ='{constants.TODAY}'
        """
    josa.write_log(constants.LOG_PATH, 'check_trade_day', sql)
    cur = db.DB('rc_team')
    cur.cursor.execute(sql)
    day = cur.cursor.fetchone()
    return day

def get_org(code, before, now):
    """당일 기관 순매수 1만주 이상"""
    sql = f"""
        SELECT  ORGR 
        FROM    cybos_cpsvr7210 
        WHERE   STKCODE = '{code}'
        AND     ORGR >= 10000
        AND     DATEDEAL='{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'get_org', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_for(code, before, now):
    """당일 외국인 순매수 1만주 이상"""
    sql = f"""
        SELECT  FORR 
        FROM    cybos_cpsvr7210 
        WHERE   STKCODE = '{code}'
        AND     FORR >= 10000
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'get_for', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def abs_org_value(code):
    """기관 최근10개(당일제외, 날짜무시) "순매매절대값" 평균값"""
    sql = f"""
        SELECT  STKCODE, 
                round(SUM(ABS(ORG_SONMEME_CNT)/10),0)ORG_SUM
        FROM    (
                    SELECT  DATEDEAL, 
                            STKCODE, 
                            ORG_SONMEME_CNT  
                    FROM    CYBOS_CpSvr7254
                    WHERE   STKCODE = '{code}'
                    ORDER BY DATEDEAL DESC
                )
        WHERE   ROWNUM <= 10
        GROUP BY STKCODE
        """
    josa.write_log(constants.LOG_PATH, 'sum_org_cnt', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def abs_for_value(code):
    """외국인 최근10개(당일제외, 날짜무시) "순매매절대값" 평균값"""
    sql = f"""
        SELECT  STKCODE, 
                round(SUM(ABS(FOR_SONMEME_CNT)/10),0)FOR_SUM
        FROM    (
                    SELECT  DATEDEAL, 
                            STKCODE,
                            FOR_SONMEME_CNT
                    FROM    CYBOS_CpSvr7254
                    WHERE   STKCODE = '{code}'
                    ORDER BY DATEDEAL DESC
                )
        WHERE   ROWNUM <= 10
        GROUP BY STKCODE
        """
    josa.write_log(constants.LOG_PATH, 'sum_for_cnt', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def today_org(code, before, now):
    """기관이 오늘 산 종목"""
    sql = f"""
        SELECT  ORGR  
        FROM    cybos_cpsvr7210  
        WHERE   ORGR > 0
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        AND     STKCODE = '{code}'
        """
    josa.write_log(constants.LOG_PATH, 'today_org', sql)
    cur=db.DB("rc_team")
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def today_for(code, before, now):
    """외국인이 오늘 산 종목"""
    sql = f"""
        SELECT  FORR  
        FROM    cybos_cpsvr7210  
        WHERE   FORR > 0
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        AND     STKCODE = '{code}'
        """
    josa.write_log(constants.LOG_PATH, 'today_for', sql)
    cur=db.DB("rc_team")
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_org_continuous(code, day):
    """기관 연속순매매"""
    sql = f"""
        SELECT  STKCODE, 
                DATEDEAL, 
                ORG_SONMEME_CNT                
        FROM    CYBOS_CpSvr7254 
        WHERE   ORG_SONMEME_CNT > 0  
        AND     STKCODE = '{code}'
        AND     DATEDEAL = '{day}'
        ORDER BY DATEDEAL DESC
        """
    josa.write_log(constants.LOG_PATH, 'get_org_continuous', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_for_continuous(code, day):
    """외국인 연속순매매"""
    sql = f"""
        SELECT  STKCODE, 
                DATEDEAL, 
                FOR_SONMEME_CNT
        FROM    CYBOS_CpSvr7254 
        WHERE   FOR_SONMEME_CNT > 0 
        AND     STKCODE = '{code}'
        AND     DATEDEAL = '{day}'
        ORDER BY DATEDEAL DESC
        """
    josa.write_log(constants.LOG_PATH, 'get_for_continuous', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_together(code, before, now):
    """당일 기관 순매수 3000주 이상 & 외인 순매수 3000주 이상인 종목"""
    sql = f"""
        SELECT  orgr, 
                forr 
        FROM    cybos_cpsvr7210 
        WHERE   STKCODE = '{code}' 
        AND     ORGR >= 3000 
        AND     FORR >= 3000
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'org_for_together', sql)
    cur = db.DB("rc_team")
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_detail(code, before, now):
    sql = f"""
        SELECT  ORG1, 
                ORG2, 
                ORG3, 
                ORG4 
        FROM    cybos_cpsvr7210 
        WHERE   STKCODE = '{code}'
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        """    
    josa.write_log(constants.LOG_PATH, 'detail_amount', sql)
    cur=db.DB("rc_team")
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_ratio(code, before, now):
    sql = f"""
        select  ROUND(RATIO,2)RATIO, 
                VOL 
        from    STOCK_1_DAY
        WHERE   CODE = '{code}' 
        AND     DATEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'detail_amount', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_today_amount(code, before, now):
    sql = f"""
        SELECT  TIMEDEAL, 
                FORR, 
                ORGR,
                volume 
        FROM    cybos_cpsvr7210  
        WHERE   STKCODE = '{code}' 
        AND     DATEDEAL = '{constants.TODAY}' 
        AND     TIMEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'today_amt', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info

def get_continuous_amount(code, day5, day2):
    sql = f"""
        SELECT  DATEDEAL, 
                FOR_SONMEME_CNT, 
                ORG_SONMEME_CNT
        FROM    CYBOS_CpSvr7254 
        WHERE   STKCODE = '{code}'
        AND     DATEDEAL BETWEEN '{day5}' AND '{day2}'
        ORDER BY DATEDEAL DESC
        """
    josa.write_log(constants.LOG_PATH, 'continuous_amt_5days', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_duplication(code):
    sql = f"""
        select  * 
        from    rtbl_news_info 
        where   d_news_crt = '{constants.TODAY}' 
        and     stk_code = '{code}'
        and     news_code = '{constants.NEWS_CODE}'
        """
    josa.write_log(constants.LOG_PATH, 'duplication', sql)
    cur=db.DB('news_user')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info


