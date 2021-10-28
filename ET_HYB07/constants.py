from datetime import datetime
from standardcode import josa
import datetime as dt
import os

path=os.path.abspath(__file__)
#오늘 날짜
TODAY=datetime.today().strftime("%Y%m%d")
DAY=TODAY[-4:][-2:]
#5영업일 전
DAY5=josa.get_day(6)
DAY4=josa.get_day(5)
#어제
YESTERDAY = josa.get_day(2)

LOG_PATH=os.getcwd()+'/log/'

I = dt.datetime.now()
NOW=I.strftime("%H%M")
J = dt.datetime.strptime(NOW, "%H%M%S") - dt.timedelta(minutes=40)
BEFORE=J.strftime("%H%M")

# NOW='1020'
# BEFORE='0950'

LOCAL_PATH=os.getcwd()+'/log/'

#news_code
NEWS_CODE='test_ET_HYB17'
MAKER='씽크풀'
#채널 코드
CHENNEL_CODE='PnNpH1'
CNTS_TYPE = "T"  # 본문형태(T:Text, H:Html, I:Image, A:Audio, V:Video, N:Nothing)
NEWS_INP_KIND = "I"


#paragraph part

#name, ratio, info
TITLE="{} {}{}"

#name, josa, day, hour, minute, ratio, price
PARA1="{}{} {}일 {}시 {}분 현재 전일보다 {}한 {}에 거래중이다 <br><br>"
#NAME JOSA< HEADER JOSA
PARA2="{}{} {}{} 알려져 있다. <br><br>"
#NAME,josa who, WHO
PARA3="이시간 {}{} 하는 것으로 잠정 집계되고 있다. <br><br>"
PARAGRAPH='최근 5일동안 {} 했다.<br><br>'


#{}. format(news_code,TODAY news_code, code)
FILEPATH='/ref/img/ET_HYB17/{}{}_{}.jpeg'

URL="https://rcd1.rassiro.com/news/ref/img/ET_HYB17/{}{}_{}.jpeg"
#News_code, News_code, stk_code
HTML="""
     [{}] 외국인ㆍ기관 순매매량 (단위 주)
      <div><img src="{}"></div>
     <br>※ 장중 매매동향은 잠정치이므로 실제 매매동향과 차이가 발생할수 있음 <br><br>"""

# query part
KOSPI_KOSDAQ="""
select price.stk_name, price.stk_code, price.close, price.fluct_ratio, nvl(FI.HEADER,' ')
from
A3_CURPRICE price
inner join
(select *
  from (select code, name , row_number() over(order by capital desc) as cap_rank
           from KOSPI_MASTER 
          where datedeal =:today)
  where cap_rank between :range1 and :range2
union 
select * 
from (select code, name , row_number() over(order by capital desc) as cap_rank 
         from KOSDAQ_MASTER 
         where datedeal =:today)
where cap_rank between :range1 and :range2
) capital
on capital.code=price.STK_CODE and PRICE.FLUCT_RATIO!='0'
left outer join fi_outline_cont fi
on fi.code = price.stk_code"""

NET_BUYING="""select sum(for_buy),sum(for_sell), sum(org_buy), sum(org_sell), sum(etc_buy), sum(etc_sell)from
       (select DATEDEAL, VOL , FOR_BUY, FOR_SELL,ORG_BUY,ORG_SELL,ETC_BUY,ETC_SELL 
        from INFO_STOCK_TOJAJA 
        where CODE=:CODE and DATEDEAL BETWEEN :PRE AND :POST         
        order by DATEDEAL desc)"""

#CODE를 넣어서 오늘 매매량 출력
TODAY_AMOUNT="""SELECT TIMEDEAL, FORR, ORGR,volume FROM cybos_cpsvr7210  
                WHERE STKCODE=:CODE AND DATEDEAL=:today 
                order by timedeal desc"""

#코드와 기간을 넣어서 지난 4일간의 매매량 출력
CONTINUOUS_AMOUNT="""SELECT DATEDEAL, FOR_SONMEME_CNT, ORG_SONMEME_CNT
                    FROM CYBOS_CpSvr7254 
                    WHERE STKCODE=:CODE 
                    AND DATEDEAL BETWEEN :PREVIOUS AND :YESTERDAY
                    ORDER BY DATEDEAL DESC"""

RATIO="""select ROUND(RATIO,2)RATIO, VOL from STOCK_1_DAY
 WHERE CODE=:CODE AND DATEDEAL BETWEEN :PRE AND :POST"""


TRADE_DAY= f"""SELECT  *
            FROM    TRADE_DAY
            WHERE   DATEDEAL ='{TODAY}'"""

# RTBL_NEWS_INFO
MODULE_INSERT_SQL = "insert into RTBL_NEWS_INFO (D_NEWS_CRT, NEWS_SN, T_NEWS_CRT, NEWS_CODE, NEWS_TITLE, " \
                    "NEWS_INP_KIND, RNEWS_CODE, D_EVENT_RNEWS, STK_CODE) values (:D_NEWS_CRT, :NEWS_SN, :T_NEWS_CRT, :NEWS_CODE, " \
                    ":NEWS_TITLE, :NEWS_INP_KIND, :RNEWS_CODE, :D_EVENT_RNEWS, :STK_CODE)"

# RTBL_NEWS_CNTS_ATYPE
HTML_INSERT_SQL = "insert into RTBL_NEWS_CNTS_ATYPE (D_NEWS_CRT, NEWS_SN, CNTS_TYPE, D_NEWS_CNTS_CRT, " \
                          "T_NEWS_CNTS_CRT, NEWS_CNTS, NEWS_CODE, RPST_IMG_URL) values (:D_NEWS_CRT, :NEWS_SN, :CNTS_TYPE, " \
                          ":D_NEWS_CNTS_CRT, :T_NEWS_CNTS_CRT, :NEWS_CNTS, :NEWS_CODE, :RPST_IMG_URL)"
#RTBL_COM_COINFO
COMMON_MODULE_SQL='insert into RTBL_COM_COINFO (SN, D_CRT, CNL_CODE, COINFO_CNTS) VALUES(:NEWS_SN, :D_NEWS_CRT, :CNL_CODE, :COINFO_CNTS)'

#이전 데이터 비교 select
COMPARING_DUPLICATION="""select * from rtbl_news_info 
                         where d_news_crt='{}' and stk_code=:code 
                         and news_code='{}'""".format(TODAY, NEWS_CODE)
