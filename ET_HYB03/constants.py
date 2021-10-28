from datetime import datetime
import datetime as dt
import os

#오늘 날짜
TODAY=datetime.today().strftime("%Y%m%d")

CHENNEL_CODE='PnNpH1'

LOG_PATH=os.getcwd()+'/log/'
#현재시간
NOW_TIME = datetime.today().strftime("%H%M%S")
#2분전 시간
FIVE_MIS_AGO = dt.datetime.strptime(NOW_TIME, "%H%M%S") - dt.timedelta(minutes=5)
PRVIOUS_TIME = FIVE_MIS_AGO.strftime("%H%M%S")

# NOW_TIME='153534'
# PRVIOUS_TIME='153234'

#차트 링크
LINK1='<img src="http://webchart.thinkpool.com/stock1day/A'
LINK2='.gif">'

#뉴스코드 & 뉴스 생성시 입력할 것들
NEWS_CODE = 'test_ET_HYB13'
MAKER='씽크풀'
CNTS_TYPE = "T"  # 본문형태(T:Text, H:Html, I:Image, A:Audio, V:Video, N:Nothing)
NEWS_INP_KIND = "I"

"""QUERIES"""


#코스피 전일비 비교
KOSPIRATIO = f"""
            select case when  total>0  then total else 0 end as total
            from    (
                        select round(sum(ratio)/count(*),2) as total 
                        from   rkospi 
                        where  datedeal='{TODAY}'
                    )
            """

# 이전 영업일
PREVIOUS_B_DAY="""select NVL(max(DATEDEAL), '휴장') from TRADE_DAY WHERE DATEDEAL<'{}'""".format(TODAY)

#시퀀스
SEQ_SQL = "SELECT NEWS_USER.RTBL_NEWS_SEQUENCE.NEXTVAL FROM DUAL"

#휴장판단
TRADE_DAY_SQL = "select NVL(max(DATEDEAL), '휴장') from TRADE_DAY where DATEDEAL=:DATEDEAL"

# 평균등락률 3% 이상 & 상승종목비율 50% 이상인 테마에 속한 종목 중
# 현재 시간 보다 10분 이내에 업데이트 된것 중에 마지막 데이터 & 상승 종목 추출 : 전일비 n% 이상인 종목
# 이전 영업일 str(BEFORE) 오늘날짜 str(TODAY), 코스피 등락률에 따른 전일 비 str(S), 현재 시간 str(NOW), 10분전 str(PREVIOUS)
# seelct 하기 위해서 fluct_ratio의 비율 및 이전 영업일 BEFORE 넣어줘야 한다.
EXTRACT_STK = f"""SELECT A.STK_NAME, A.STK_CODE, round(A.FLUCT_RATIO,1), E.HEADER
FROM A3_CURPRICE A
INNER JOIN
(SELECT
DISTINCT STKCODE
FROM  EBEST_T1533 B
INNER JOIN EBEST_THEME_MAPPING C
            ON B.THEME_CODE =C.THEMECODE               
WHERE C.DATEDEAL=:BEFORE AND B.DATEDEAL='{TODAY}'
AND B.UPRATE >='50'AND AVGDIFF>=3
and b.timedeal between '{PRVIOUS_TIME}' and '{NOW_TIME}') D
ON A.STK_CODE= D.STKCODE AND  A.FLUCT_RATIO>=:RATIO
inner join  FI_OUTLINE_CONT E
          ON E.CODE = A.STK_CODE
ORDER BY FLUCT_RATIO DESC"""

TRADE_DAY= f"""SELECT  *
            FROM    TRADE_DAY
            WHERE   DATEDEAL ='{TODAY}'"""

# 해당 종목의 상승률 높은 테마 추출 (종목이 여러 테마에 속할 수 있기 때문에 필요한 과정)
# 해당 종목이 속한 테마 중에 평균등락률 3% 이상 & 상승종목비율 50% 이상인 테마 중에 (테마 마지막 업데이트 시간 체크 필요)
# 당일 평균 등락률이 가장 높은 테마 1개 선택
# 추출된 종목이 여러 테마에 속 할 수 있기에 그 에따른 종목코드 str(CODE), str(TODAY), 이전 영업일 str(BEFORE), EBEST_T1533테이블의 가장 마지막 ROWDATA의 시간 LAST
# select 하기 위해 code, 이전영업일 넣어줘야 한다.
EXTRACT_HIGH_THEM=f"""SELECT * 
FROM
(SELECT E.THEME_CODE, F.THEMENAME, F.STKCODE  FROM  EBEST_T1533 E
INNER JOIN EBEST_THEME_MAPPING F
ON E.THEME_CODE = F.THEMECODE 
WHERE E.UPRATE>='50' AND E.AVGDIFF>='3' AND F.STKCODE=:CODE
AND E.DATEDEAL='{TODAY}' AND F.DATEDEAL=:BEFORE 
ORDER BY E.AVGDIFF DESC)
WHERE ROWNUM<=1"""

# 해당 테마에서 이 종목을 제외하고 전일비가 2% 이상인 종목 중에
# 전일비 상위 1~3개 추출
# 예외처리 * 해당되는 종목이 0개인 경우에는 두번째 문단 생성 안함
# TODAY, 이전 영업일 BEFORE, 그리고 추출된 종목의 테마에 대해 추출된 종목이외의 다른 종목을 위한 THEMECODE와 추출된 종목 CODE
# select 하기위해 themecode, code, 이전 영업일 BEFORE 를 넣어줘야 한다.
EXTRACT_REALTED_STK=f"""select*from
(SELECT C.STK_NAME, round(C.FLUCT_RATIO,1)
FROM A3_CURPRICE C
INNER JOIN
(SELECT 
DISTINCT B.STKCODE
FROM EBEST_T1533 A
INNER JOIN EBEST_THEME_MAPPING B
            ON A.THEME_CODE = B.THEMECODE
WHERE A.DATEDEAL='{TODAY}' AND B.DATEDEAL=:BEFORE AND
          UPRATE>='50' AND AVGDIFF>='3' and b.themecode=:themecode) D
          ON C.STK_CODE =D.STKCODE
WHERE FLUCT_RATIO>='2' 
and stk_code not in :code
order by  fluct_ratio desc)
where rownum<=3"""

#기업개요가 없는 경우 두번째 문장 생성하지 않기위한 비교 수단
SUMMARY="""select header from FI_OUTLINE_CONT where code =:CODE"""

# RTBL_NEWS_INFO
MODULE_INSERT_SQL = "insert into RTBL_NEWS_INFO (D_NEWS_CRT, NEWS_SN, T_NEWS_CRT, NEWS_CODE, NEWS_TITLE, " \
                    "NEWS_INP_KIND, RNEWS_CODE, D_EVENT_RNEWS, STK_CODE) values (:D_NEWS_CRT, :NEWS_SN, :T_NEWS_CRT, :NEWS_CODE, " \
                    ":NEWS_TITLE, :NEWS_INP_KIND, :RNEWS_CODE, :D_EVENT_RNEWS, :STK_CODE)"

# RTBL_NEWS_CNTS_ATYPE
HTML_INSERT_SQL = "insert into RTBL_NEWS_CNTS_ATYPE (D_NEWS_CRT, NEWS_SN, CNTS_TYPE, D_NEWS_CNTS_CRT, " \
                          "T_NEWS_CNTS_CRT, NEWS_CNTS, NEWS_CODE, RPST_IMG_URL) values (:D_NEWS_CRT, :NEWS_SN, :CNTS_TYPE, " \
                          ":D_NEWS_CNTS_CRT, :T_NEWS_CNTS_CRT, :NEWS_CNTS, :NEWS_CODE, :RPST_IMG_URL)"

#중복 INSERT 방지하기 위해 RTBL_NEWS_CNTS_ATYPE과 RTBL_NEWS_INFO SELECT하는 구간을 가져옴
NEWS_INFO=f"""select * from RTBL_news_info where news_code='{NEWS_CODE}' AND STK_CODE=:CODE AND D_NEWS_CRT='{TODAY}'"""