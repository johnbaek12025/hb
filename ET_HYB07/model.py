import constants, os
from standardcode import josa, db

def get_high_cap(today:str, range1:int, range2:int)->tuple:
    sql = f"""
        select  price.stk_name, 
                price.stk_code, 
                price.close, 
                price.fluct_ratio, 
                nvl(FI.HEADER,' ')
        from    A3_CURPRICE price
                inner join  (
                            select *
                            from   (
                                    select  code, 
                                            name , 
                                            row_number() over(order by capital desc) as cap_rank
                                    from    KOSPI_MASTER 
                                    where   datedeal = '{today}'
                                    )
                            where cap_rank between {range1} and {range2}
                            union 
                            select  * 
                            from    (
                                    select  code, 
                                            name , 
                                            row_number() over(order by capital desc) as cap_rank 
                                    from    KOSDAQ_MASTER 
                                    where   datedeal = '{today}'
                                    )
                            where   cap_rank between {range1} and {range2}
                            ) capital
                on          capital.code = price.STK_CODE 
                and         PRICE.FLUCT_RATIO != '0'
                left outer join     fi_outline_cont fi
                on                  fi.code = price.stk_code
        """
    josa.write_log(constants.LOG_PATH, 'get_high_cap', sql)
    cur=db.DB('tp_stock')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_today_amount(code:str, today:str)->list:
    """ 특정 종목에 대해 외국인과 기관의 잠성 순매매량 추출"""
    sql = f"""
        SELECT  TIMEDEAL, 
                FORR, 
                ORGR,
                volume 
        FROM    cybos_cpsvr7210  
        WHERE   STKCODE = '{code}' 
        AND     DATEDEAL = '{today}'
        order by timedeal desc
        """
    josa.write_log(constants.LOG_PATH, 'get_today_amount', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
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

def get_net(code:str, before:str)-> list:
    """5일동안의 외국인, 기관, 개인의 순매매량을 구하기위한 함수
        ⓐ52주 신고가 경신한 종목과 5영업일 이전의 날짜를 parameter로 받는다.
        ⓑconstants.NET_BUYING query에 인자로 보내 외국인, 기관, 개인의 순매매량을 tuple(int)로 받음
        ⓒtuple을 return"""
    sql = f"""
        select  sum(for_buy),
                sum(for_sell), 
                sum(org_buy), 
                sum(org_sell), 
                sum(etc_buy), 
                sum(etc_sell)
        from    (
                    select  DATEDEAL, 
                            VOL , 
                            FOR_BUY, 
                            FOR_SELL,
                            ORG_BUY,
                            ORG_SELL,
                            ETC_BUY,
                            ETC_SELL 
                    from    INFO_STOCK_TOJAJA 
                    where   CODE = '{code}'
                    and     DATEDEAL BETWEEN '{before}' AND '{constants.TODAY}'
                    order by DATEDEAL desc
                )
        """
    josa.write_log(constants.LOG_PATH, 'net_amount', sql)
    cur=db.DB('tp_stock')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_continuous_amount(code:str, day5:str, day2:str)->tuple:
    """특정 종목에 대한 어제와 5일전의 외국인과 기관의 순매매량 추출"""
    sql = f"""
        SELECT  DATEDEAL, 
                FOR_SONMEME_CNT, 
                ORG_SONMEME_CNT
        FROM    CYBOS_CpSvr7254 
        WHERE   STKCODE = '{code}'
        AND     DATEDEAL BETWEEN '{day5}' AND '{day2}'
        ORDER BY DATEDEAL DESC
        """
    josa.write_log(constants.LOG_PATH, 'continuous_amount', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_ratio(code:str, before:str, now:str)->tuple:
    """특정 종목에 대한 어제와 5일전의 외국인과 기관의 순매매량 추출"""
    sql = f"""
        select  ROUND(RATIO,2)RATIO, 
                VOL 
        from    STOCK_1_DAY
        WHERE   CODE = '{code}' 
        AND     DATEDEAL BETWEEN '{before}' AND '{now}'
        """
    josa.write_log(constants.LOG_PATH, 'get_ratio', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info = cur.cursor.fetchall()
    return info


def get_duplication(code:str)->list:
    sql = f"""
        select  * 
        from    rtbl_news_info 
        where   d_news_crt='{constants.TODAY}' 
        and     stk_code = '{code}'
        and     news_code='{constants.NEWS_CODE}'
        """
    josa.write_log(constants.LOG_PATH, 'get_duplication', sql)
    cur=db.DB('news_user')
    cur.cursor.execute(constants.COMPARING_DUPLICATION, CODE=code)
    info=cur.cursor.fetchall()
    return info