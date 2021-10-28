from datetime import datetime
import os

#오늘 날짜
TODAY=datetime.today().strftime("%Y%m%d")
DAY=TODAY[-4:][-2:]
#news_code
NEWS_CODE='test_ET_HYB15'

LOG_PATH=os.getcwd()+'/log/'
MAKER='씽크풀'
#채널 코드
CHENNEL_CODE='PnNpH1'
CNTS_TYPE = "T"  # 본문형태(T:Text, H:Html, I:Image, A:Audio, V:Video, N:Nothing)
NEWS_INP_KIND = "I"
#code
LINK1='<img src="{}">'
LINK='http://webchart.thinkpool.com/stock1day/A{}.gif'
#NAME,JOSA, DAY, HOUR, MINUTES, RATIO, PRICE
PARA1='{}{} {}일 {}시 {}분 현재 전일보다 {} {}에 거래 중이다. '
#NAME, JOSA, HEADER, JOSA
PARA2='{}{} {}{} 알려져 있다. <br><br>'
#org,josa name, josa, article, JOSA, opionion
PARA3="{}{} {}{} 관련해 '{}'{}{} 리포트를 발표했다. <br><br>"
#cont, josa
PARA4="해당 리포트에 따르면 '{}' {} 분석했다.<br><br>"

sql=f"""
select kind.stk_name,
          kind.code,
          fi.header,
          kind.close,
          kind.fluct_ratio,
          CHANG.ORG_NAME, 
          kind.opinion,
          kind.goal_value,
          kind.cont_a,
          kind.cont_b1
from
        (select price.stk_name , 
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
                  and price.stk_code= org.code
        where org.datedeal= '{TODAY}' 
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
                  org.opinion) kind
inner join fi_outline_cont fi
          on fi.code=kind.code
inner join STOCK_CHANGKU_CODE chang
         on chang.org_num=kind.org_code
where kind.opinion is not null
"""

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