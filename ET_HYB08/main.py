from datetime import datetime
import controller
import model
from standardcode import josa, db
import logging, traceback, os
logging.basicConfig(level=logging.ERROR)
import constants
import make_table
import sys

def run():
    trade = model.check_trade_day()
    if not trade:
        josa.write_log(constants.LOG_PATH, 'trade_day', '휴장')
        sys.exit()

    josa.write_log(constants.LOG_PATH, 'arranging()', None)
    hh=int(constants.HH)
    josa.write_log(constants.LOG_PATH, '현재시간', hh)
    if hh<9:
        result=controller.before_market()
        josa.write_log(constants.LOG_PATH, '장 시작전', result)
        arranging(result)
    elif hh>=9 and hh<16:
        result=controller.middle_market()
        josa.write_log(constants.LOG_PATH, '장 중', result)
        arranging(result)
    else:
        result=controller.end_market()
        josa.write_log(constants.LOG_PATH, '장 마감후', result)
        arranging(result)

def arranging(result:list):
        josa.write_log(constants.LOG_PATH, 'arranging()', result)
        for row in result:
            keyword=row[0]
            codes=row[1]
            names=row[2]
            info=row[3]
            title=row[4]
            paras=row[5:]
            # signal=model.get_duplication(keyword+'%')
            # if len(signal)!=0:
            #     print('중복')
            #     continue
            img_path=make_table.get_table(info, keyword)
            localpath = img_path
            filepath = constants.FILEPATH.format(constants.TODAY,constants.NEWS_CODE, keyword)            
            url=constants.URL.format(constants.TODAY,constants.NEWS_CODE,keyword)
            db.DB.get_trans('', localpath, filepath)
            news_sn=controller.make_news(keyword, codes,url,title, paras,names)
            # controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)

if __name__ == "__main__":
    try:
        run()
    except Exception as err:
        print(err)
        logging.error(traceback.format_exc())