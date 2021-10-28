from datetime import datetime
import os

#오늘 날짜
TODAY=datetime.today().strftime("%Y%m%d")
DAY=TODAY[-4:][-2:]

NOW_TIME = datetime.today().strftime("%H%M%S")

# HH='08'
NOW_MINUTE = datetime.today().strftime("%H%M")
HH=NOW_MINUTE[:2]
MM=NOW_MINUTE[2:]

NEWS_CODE='test_ET_HYB18'
PATH='./img/'
LOG_PATH=os.getcwd()+'/log/'
#{}. format(TODAY news_code, code)
FILEPATH='/ref/img/ET_HYB18/{}_{}_{}.jpeg'
URL="https://rcd1.rassiro.com/news/ref/img/ET_HYB18/{}_{}_{}.jpeg"
HTML="""[{} 관련주] 
      <div><img src="{}"></div>"""
MAKER='씽크풀'
#채널 코드
CHENNEL_CODE='PnNpH1'
CNTS_TYPE = "T"  # 본문형태(T:Text, H:Html, I:Image, A:Audio, V:Video, N:Nothing)
NEWS_INP_KIND = "I"

"""para"""
TITLE="[이슈종목]{} 관련... {} {}"
PARA1="AI와 빅데이터 기술로 투자 정보를 제공하는 ET라씨로의 분석결과에 따르면, 이 시간 투자자들은 ‘{}‘ 관련주를 많이 검색하고 있으며 해당 종목으로 {} 등인 것으로 나타났다. <br><br>"
#NAME, JOSA, PRICE, RATIO, NAME, JOSA, PRICE, RATIO
PRE_PARA2="전일 {}{} {} ({})에 거래가 마감되었고, {}{} {}({})으로 장을 마무리했다. <br><br>"
#DATE, AM PM HOUR, MM, NAME, JOSA, RATIO, RISING OR FALLING, PRICE, NAME, JOSA, RATIO, RISING OR FALLING, PRICE
MID_PARA2="{}일 {}시 {}분 현재 {}{} 전일보다 {}한 {}에 거래되고 있고, {}{} {}한 {}에 거래되고 있다.<br><br>"
#DATE, NAME, JOSA, PRICE, RATIO, NAME, JOSA, PROCE, RATIO
END_PARA2="{}일 {}{} {} ({})에 거래가 마감되었고, {}{} {}({})으로 거래를 마쳤다. <br><br>"



"""QUERY"""
KEYWORD="""select distinct(keyword) 
            from STOCK_RELATED_KEYWORDS 
            where datedeal=:DAY"""

MIDDLE_NAME_PRICE_RATIO = """
select PRICE.STK_NAME, PRICE.STK_CODE, PRICE.CLOSE, PRICE.FLUCT_RATIO from 
STOCK_RELATED_KEYWORDS keyword
inner join a3_curprice price
          on PRICE.STK_CODE=KEYWORD.STKCODE 
          AND KEYWORD.DATEDEAL=PRICE.D_CNTR
where KEYWORD.datedeal = :DAY AND keyword.KEYWORD=:KEYWORD        
order by price.fluct_ratio desc
"""

START_NAME_PRICE_RATIO = """
select PRICE.STK_NAME, DAY.CODE, DAY.JONGGA, DAY.RATIO from 
STOCK_RELATED_KEYWORDS keyword
inner join STOCK_1_DAY DAY
         ON DAY.DATEDEAL = KEYWORD.DATEDEAL 
              AND KEYWORD.STKCODE = DAY.CODE
INNER JOIN A3_CURPRICE PRICE
           ON DAY.CODE = PRICE.STK_CODE               
WHERE KEYWORD.DATEDEAL = : DAY AND KEYWORD.KEYWORD = :KEYWORD
order by day.ratio desc
"""



GET_SIGNAL="""
SELECT stock_code, stock_name, signal, length(signal) FROM
(select stock_code, stock_name, 
    case when buy_dttm>sell_dttm then buy_price||'     \'||buy_dttm 
            When sell_dttm>buy_dttm then profit_rate||' '||sell_dttm  
            else buy_price||'     \'||buy_dttm  end as signal
             from 
(select  stock_code, stock_name, substr(buy_dttm, 1, 8)buy_dttm, buy_price, substr(sell_dttm , 1,8)sell_dttm, profit_rate
  from RASSI.TRADE_SIGNAL  
where substr(buy_dttm, 1, 8)  between :day5 and :today or 
           substr(sell_dttm , 1,8) between :day5 and :today
           ) 
where 
stock_code =: code and 
profit_rate>1 
order by signal desc)
WHERE ROWNUM<=1
"""

GET_HEADER="""
SELECT HEADER FROM FI_OUTLINE_CONT WHERE CODE=:CODE
"""


TRADE_DAY= f"""SELECT  *
            FROM    TRADE_DAY
            WHERE   DATEDEAL ='{TODAY}'"""

# RTBL_NEWS_INFO
MODULE_INSERT_SQL = "insert into RTBL_NEWS_INFO (D_NEWS_CRT, NEWS_SN, T_NEWS_CRT, NEWS_CODE, NEWS_TITLE, " \
                    "NEWS_INP_KIND, RNEWS_CODE, D_EVENT_RNEWS) values (:D_NEWS_CRT, :NEWS_SN, :T_NEWS_CRT, :NEWS_CODE, " \
                    ":NEWS_TITLE, :NEWS_INP_KIND, :RNEWS_CODE, :D_EVENT_RNEWS)"

# RTBL_NEWS_CNTS_ATYPE
HTML_INSERT_SQL = "insert into RTBL_NEWS_CNTS_ATYPE (D_NEWS_CRT, NEWS_SN, CNTS_TYPE, D_NEWS_CNTS_CRT, " \
                          "T_NEWS_CNTS_CRT, NEWS_CNTS, NEWS_CODE, RPST_IMG_URL) values (:D_NEWS_CRT, :NEWS_SN, :CNTS_TYPE, " \
                          ":D_NEWS_CNTS_CRT, :T_NEWS_CNTS_CRT, :NEWS_CNTS, :NEWS_CODE, :RPST_IMG_URL)"
#RTBL_COM_COINFO
COMMON_MODULE_SQL='insert into RTBL_COM_COINFO (SN, D_CRT, CNL_CODE, COINFO_CNTS) VALUES(:NEWS_SN, :D_NEWS_CRT, :CNL_CODE, :COINFO_CNTS)'

RELACTED_STK_CODE="INSERT INTO RTBL_COM_RSC(SN, D_CRT, RSC_CODE) VALUES(:sn, :d_crt, :rsc_code)"

#이전 데이터 비교 select
COMPARING_DUPLICATION="""select news_title from rtbl_news_info 
                         where d_news_crt='{}' 
                         and news_title like :keyword
                         and news_code='{}'""".format(TODAY, NEWS_CODE)          