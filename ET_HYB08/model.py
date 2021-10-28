import constants
from standardcode import db, josa

def get_keyword(date:str)->tuple:
    sql = f"""
        select  distinct(keyword) 
        from    STOCK_RELATED_KEYWORDS 
        where   datedeal = {date}
        """    
    josa.write_log(constants.LOG_PATH, 'get_keyword', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(constants.KEYWORD, DAY=date)
    info=cur.cursor.fetchall()
    return info

def get_kind(date:str, keyword:str)->tuple:
    sql = f"""
        select  PRICE.STK_NAME, 
                DAY.CODE, 
                DAY.JONGGA, 
                DAY.RATIO 
        from    STOCK_RELATED_KEYWORDS keyword
        inner join STOCK_1_DAY DAY
                ON DAY.DATEDEAL = KEYWORD.DATEDEAL 
                    AND KEYWORD.STKCODE = DAY.CODE
        INNER JOIN A3_CURPRICE PRICE
                ON DAY.CODE = PRICE.STK_CODE               
        WHERE   KEYWORD.DATEDEAL = '{date}'
        AND     KEYWORD.KEYWORD = '{keyword}'
        order by day.ratio desc
        """
    josa.write_log(constants.LOG_PATH, 'get_kind', sql)
    cur=db.DB('rc_team')        
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_kind_2(date:str, keyword:str)->tuple:
    sql = f"""
        select  PRICE.STK_NAME, 
                price.stk_code,
                price.close,
                price.fluct_ratio
        from    STOCK_RELATED_KEYWORDS keyword        
        INNER JOIN A3_CURPRICE PRICE
                ON keyword.stkCODE = PRICE.STK_CODE               
        WHERE   KEYWORD.DATEDEAL = '{date}'
        AND     KEYWORD.KEYWORD = '{keyword}'
        order by price.fluct_ratio desc
        """
    josa.write_log(constants.LOG_PATH, 'get_kind_2', sql)
    cur=db.DB('rc_team')        
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

def extract_signal(code:str, day:str, day5:str)->tuple:
    sql = f"""
        SELECT  stock_code, 
                stock_name, 
                signal, 
                length(signal) 
        FROM    (
                    select  stock_code, 
                            stock_name, 
                            case when   buy_dttm>sell_dttm  
                            then        buy_price||'     \'||buy_dttm 
                            When        sell_dttm>buy_dttm then profit_rate||' '||sell_dttm  
                            else        buy_price||'     \'||buy_dttm  end as signal
                    from    (
                                select  stock_code, 
                                        stock_name, 
                                        substr(buy_dttm, 1, 8)buy_dttm, 
                                        buy_price, substr(sell_dttm , 1,8)sell_dttm, 
                                        profit_rate
                                from    RASSI.TRADE_SIGNAL  
                                where   substr(buy_dttm, 1, 8)  between {day5} and {day}
                                or      substr(sell_dttm , 1,8) between {day5} and {day}
                            ) 
                    where   stock_code = '{code}'
                    and     profit_rate > 1 
                    order by signal desc
                )
        WHERE ROWNUM <= 1
        """
    josa.write_log(constants.LOG_PATH, 'extract_signal', sql)
    cur=db.DB('rc_team')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def extract_header(code:str)->tuple:
    sql = f"""
        SELECT  HEADER 
        FROM    FI_OUTLINE_CONT 
        WHERE   CODE = '{code}'
        """
    josa.write_log(constants.LOG_PATH, 'extract_header', sql)
    cur=db.DB('rc_team')    
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info


def get_duplication(keyword:str)->list:
    sql = f"""
        select  news_title 
        from    rtbl_news_info 
        where   d_news_crt = '{constants.TODAY}' 
        and     news_title like '{keyword}'
        and     news_code = '{constants.NEWS_CODE}'
        """
    josa.write_log(constants.LOG_PATH, 'duplication_check', sql)
    cur=db.DB('news_user')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info    

