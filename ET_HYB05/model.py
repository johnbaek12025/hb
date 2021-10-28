import db
import constants
import josa

def get_info():
    sql = f"""
        select  kind.stk_name,
                kind.code,
                fi.header,
                kind.close,
                kind.fluct_ratio,
                CHANG.ORG_NAME, 
                kind.opinion,
                kind.goal_value,
                kind.cont_a,
                kind.cont_b1
        from    (
                    select price.stk_name , 
                        org.code,               
                        price.close , 
                        price.fluct_ratio , 
                        org.opinion,
                        org.goal_value, 
                        org.org_code, 
                        org.cont_a , 
                        org.cont_b1,                              
                        max(length(org.cont_a))len                                               
                    from a3_curprice price
                    inner join ORG_OPINION_MANUAL_MOD org
                            on org.datedeal=price.d_cntr 
                        and  price.stk_code= org.code
                    where org.datedeal= '{constants.TODAY}' 
                    and price.fluct_ratio !=0
                    group by price.stk_name, 
                        org.code,              
                        price.close, 
                        price.fluct_ratio, 
                        org.opinion,
                        org.goal_value, 
                        org.org_code, 
                        org.cont_a, 
                        org.cont_b1, 
                        org.opinion
                ) kind
            inner join fi_outline_cont fi
            on fi.code=kind.code
            inner join STOCK_CHANGKU_CODE chang
            on chang.org_num=kind.org_code
        where kind.opinion is not null
    """
    josa.write_log(constants.LOG_PATH, 'get_info', sql)
    cur=db.DB('tp_stock')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def get_duplication(code):
    sql = f"""
            select  * 
            from    rtbl_news_info 
            where   d_news_crt='{constants.TODAY}' 
            and     stk_code = '{code}'
            and     news_code = '{constants.NEWS_CODE}'
                         """
    josa.write_log(constants.LOG_PATH, 'duplication', sql)
    cur=db.DB('news_user')
    cur.cursor.execute(sql)
    info=cur.cursor.fetchall()
    return info

def check_trade_day():
    sql = f"""
        SELECT  *
        FROM    TRADE_DAY
        WHERE   DATEDEAL ='{constants.TODAY}'
        """
    josa.write_log(constants.LOG_PATH, 'duplication', sql)
    cur = db.DB('rc_team')
    cur.cursor.execute(constants.TRADE_DAY)
    day = cur.cursor.fetchone()
    return day
