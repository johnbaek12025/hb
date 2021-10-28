from datetime import datetime
#오늘 날짜
TODAY=str(datetime.today().strftime("%Y%m%d"))

import datetime
today = datetime.date.today()
first = today.replace(day=1)
before= first - datetime.timedelta(days=1)
before=before.strftime("%Y%m")
BEFORE=str(before+TODAY[-2:])

LINK1 = 'https://finance.naver.com/item/coinfo.nhn?code={}'
TAG1 = '기업개요 : <a href=' + '" {} "' + ' target="_blank">{}</a>'

#기업 개요 구하는 부분
SUMMARY_SQL = "select code, header from FI_OUTLINE_CONT where code=:code order by reg_date desc"

#최신 공시
RPTNM_SQL="""select * from (select 
rcpno, rptnm,to_char(indt) 
from TB_main where STCKCD=:STCKCD AND RCPDT BETWEEN '{}' AND '{}' order by rcpdt desc) where rownum<=5""".format(BEFORE, TODAY)

#최근 주요 기사
NAVER_ISSUE = """select * from(select title, pubdate, original_url
from NAVER_NEWS_STOCKISSUE
where stkcode=:stkcode and substr(pubdate, 1,8) between '{}'  and '{}'  order by pubdate desc) where rownum<=5""".format(BEFORE, TODAY)

