from datetime import datetime
import josa
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import datetime as dt
import os

#news_code
NEWS_CODE='test_ET_HYB14'
MAKER='씽크풀'
#채널 코드
CHENNEL_CODE='PnNpH1'
CNTS_TYPE = "T"  # 본문형태(T:Text, H:Html, I:Image, A:Audio, V:Video, N:Nothing)
NEWS_INP_KIND = "I"
LOG_PATH=os.getcwd()+'/log/'

I = dt.datetime.now()
NOW=I.strftime("%H%M")
J = dt.datetime.strptime(NOW, "%H%M%S") - dt.timedelta(minutes=120)
BEFORE=J.strftime("%H%M")
# NOW='1030'
# BEFORE='0950'

#오늘 날짜
TODAY=datetime.today().strftime("%Y%m%d")
DAY=TODAY[-4:][-2:]
CHENNEL_CODE='PnNpH1'
NOW_TIME = datetime.today().strftime("%H%M")
HH=NOW_TIME[:-2]
MM=NOW_TIME[-2:]

DAY5=josa.get_day(5)

YESTERDAY = josa.get_day(2)

#para1-> name, ratio, who, amount, net buying 
#para2-> name, ratio, who, period, net buying
TITLE='[수급특징주]{} +{}%↑, {} {} {}'
#para3-> name, ratio
TITLE2='[수급특징주]{} +{}%↑, 외국인/기관 동시 순매수'
#날짜 시, 분, 종목명, 코드, 조사, 기관or 외국인, 순매수량, 비율, 현재가
PARA1='{}일 {}시 {}분 기준으로 {}({}){} {}이 {} 대량으로 순매수(잠정) 하면서 전일 대비 {}%(현재가 {}) 상승하고 있다. <br><br>'
#날짜, 시간, 분, 종목명, 코드, 조사, 비율, 가격, 기관or 외국인, 연속일, 누적 순매수량
PARA2='{}일 {}시 {}분 기준으로 {}({}){} 전일 대비 {}%(현재가 {}) 상승했고, {}이 최근 {}일 연속 순매수 (누적 {}, 잠정) 행진을 하고 있다. <br><br>'
#날짜, 시, 분, 종목명, 코드, 조사, 외국인 순매수량, 기관 순매수량, 비율, 가격
PARA3='{}일 {}시 {}분 기준으로 {}({}){} 외국인과 기관이 각각 {}, {} 순매수(잠정) 하면서 전일 대비 {}%(현재가 {}) 상승하고 있다. <br><br>'

#{}. format(news_code, news_code, code)
FILEPATH='/ref/img/ET_HYB14/'+TODAY+'{}_{}.jpeg'

#News_code, News_code, stk_code
HTML='[{}] 외국인ㆍ기관 순매매량 (단위 주) ' \
     '<div><img src="https://rcd1.rassiro.com/news/ref/img/ET_HYB14/'+TODAY+'{}_{}.jpeg"></div>' \
     '<br>※ 장중 매매동향은 잠정치이므로 실제 매매동향과 차이가 발생할수 있음 <br><br>'

#News_code, News_code, stk_code
URL='https://rcd1.rassiro.com/news/ref/img/{}/'+TODAY+'{}_{}.jpeg'

SECOND_PARA='증권사 잠정집계에 따르면 세부 기관별로 {} 하는 것으로 나타났다.  <br><br>'

A3_CURPRICE="""SELECT STK_NAME, STK_CODE, CLOSE, ROUND(FLUCT_RATIO,1)FLUCT_RATIO 
               FROM A3_CURPRICE WHERE FLUCT_RATIO>='3' AND D_CNTR='{}'""".format(TODAY)

#기관이 1만주 이상 산 종목들 불러오는 QUERY
ORG_NET="""SELECT ORGR FROM cybos_cpsvr7210 
           WHERE STKCODE=:CODE AND ORGR>='10000' AND DATEDEAL='{}' 
           AND TIMEDEAL BETWEEN :PRE AND :POST""".format(TODAY)

#외국인이 1만주 이상 산 종목들 불러오는 QUERY
FOR_NET="""SELECT FORR FROM cybos_cpsvr7210 
            WHERE STKCODE=:CODE AND FORR>='10000' AND 
            DATEDEAL='{}' AND TIMEDEAL BETWEEN :PRE AND :POST""".format(TODAY)

# ORG_FOR_NET에서 구한 종목을 여기에 넣어서 절대값의 합의 평균 을 구한다.
# 그리고  ORG_FOR_NET QUERY에서 구한 당일 기관과 외국인의 순매수량과 비교하여 2배 이상 이 아니면 제외
SUM_ORG="""SELECT  STKCODE, round(SUM(ABS(ORG_SONMEME_CNT)/10),0)ORG_SUM
FROM
(SELECT DATEDEAL, STKCODE, ORG_SONMEME_CNT  
FROM CYBOS_CpSvr7254
WHERE STKCODE= :CODE
ORDER BY DATEDEAL DESC)
WHERE ROWNUM<=10
GROUP BY STKCODE"""

SUM_FOR="""SELECT STKCODE, round(SUM(ABS(FOR_SONMEME_CNT)/10),0)FOR_SUM
FROM
(SELECT DATEDEAL, STKCODE,FOR_SONMEME_CNT  
FROM CYBOS_CpSvr7254
WHERE STKCODE= :CODE
ORDER BY DATEDEAL DESC)
WHERE ROWNUM<=10
GROUP BY STKCODE """

# - (기관연속순매수일) 중에 큰 수 > 4 인 종목
CONTINUOUS_ORG_BUYING="""SELECT STKCODE, DATEDEAL, ORG_SONMEME_CNT
FROM CYBOS_CpSvr7254 
WHERE ORG_SONMEME_CNT>0 
AND STKCODE=:CODE 
AND DATEDEAL =:DAY
ORDER BY DATEDEAL DESC"""

#A3_CURPRICE가 FLUCT_RATIO>=3%인 종목을 cybos_cpsvr7210에 넣어서 외국인이 오늘 순매수했는지 아닌지 필터링 
TODAY_FOR="""SELECT FORR  FROM cybos_cpsvr7210  
WHERE FORR>'0' AND DATEDEAL='{}' AND TIMEDEAL BETWEEN :PRE AND :POST AND STKCODE=:CODE""".format(TODAY)

#A3_CURPRICE가 FLUCT_RATIO>=3%인 종목을 cybos_cpsvr7210에 넣어서 기관이 오늘 순매수했는지 아닌지 필터링
TODAY_ORG="""SELECT ORGR  FROM cybos_cpsvr7210  
WHERE  ORGR>'0' AND DATEDEAL='{}' AND TIMEDEAL BETWEEN :PRE AND :POST AND STKCODE=:CODE""".format(TODAY)

# - (외국인연속순매수일) 중에 큰 수 > 4 인 종목
CONTINUOUS_FOR_BUYING="""SELECT STKCODE, DATEDEAL, FOR_SONMEME_CNT
FROM CYBOS_CpSvr7254 
WHERE FOR_SONMEME_CNT>0  
AND STKCODE=:CODE 
AND DATEDEAL=:DAY
ORDER BY DATEDEAL DESC"""

# - 당일 기관 순매수 3000주 이상 & 외인 순매수 3000주 이상인 종목
TOGETHER_NET="""SELECT orgr, forr FROM cybos_cpsvr7210 
                WHERE STKCODE=:CODE AND ORGR>='3000' AND FORR>='3000' AND DATEDEAL='{}' 
                AND TIMEDEAL BETWEEN :PRE AND :POST""".format(TODAY)


#보험기타금융 , 투신, 은행, 연기금
DETAIL_NET="""SELECT ORG1, ORG2, ORG3, ORG4 FROM cybos_cpsvr7210 WHERE 
STKCODE=:CODE AND 
DATEDEAL='{}' AND TIMEDEAL BETWEEN :PRE AND :POST""".format(TODAY)



#CODE를 넣어서 오늘 매매량 출력
TODAY_AMOUNT="""SELECT TIMEDEAL, FORR, ORGR,volume FROM cybos_cpsvr7210  
                WHERE STKCODE=:CODE AND DATEDEAL='{}' AND 
                TIMEDEAL BETWEEN :PRE AND :POST""".format(TODAY)

#코드와 기간을 넣어서 지난 4일간의 매매량 출력
CONTINUOUS_AMOUNT="""SELECT DATEDEAL, FOR_SONMEME_CNT, ORG_SONMEME_CNT
                    FROM CYBOS_CpSvr7254 
                    WHERE STKCODE=:CODE 
                    AND DATEDEAL BETWEEN :PREVIOUS AND :YESTERDAY
                    ORDER BY DATEDEAL DESC"""

RATIO="""select ROUND(RATIO,2)RATIO, VOL from STOCK_1_DAY
 WHERE CODE=:CODE AND DATEDEAL BETWEEN :PRE AND :POST"""

#이전 데이터 비교 select
COMPARING_DUPLICATION="""select * from rtbl_news_info 
                         where d_news_crt='{}' and stk_code=:code 
                         and news_code='{}'""".format(TODAY, NEWS_CODE)

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