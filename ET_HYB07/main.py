import controller
from standardcode import josa, db
import constants
import logging, traceback, os
logging.basicConfig(level=logging.ERROR)
log=os.path.dirname(os.path.abspath(__file__))
path=os.path.dirname(os.path.abspath(__file__))+'\\img'
import model
import view
import sys

def run(range1:int, range2:int):
    trade = model.check_trade_day()
    if not trade:
        josa.write_log(constants.LOCAL_PATH, 'trade day', '휴장')
        sys.exit()


    info=controller.make_para(constants.TODAY, range1, range2)  
    if len(info)==0:
        josa.writed_error(constants.LOCAL_PATH, 'Non data', info)
        sys.exit()
    for row in info:        
        code=row[0]
        title=row[1]
        ratio=row[2]
        paragraph=''.join(row[3:]) 
        signal=model.get_duplication(code)
        if len(signal)!=0:
            print('duplication')       
        img_path = view.get_info(code, path, ratio, constants.TODAY)
        if not img_path:
            continue
        localpath = img_path
        filepath = constants.FILEPATH.format(constants.TODAY,constants.NEWS_CODE, code)        
        db.DB.get_trans('', localpath, filepath)
        url = constants.URL.format(constants.TODAY,constants.NEWS_CODE, code)
        dt = josa.get_separated_date(constants.TODAY)
        html=constants.HTML.format(dt, url)
        paragraph=paragraph+html
        news_sn=controller.make_news(code, url, title, paragraph)
        # controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)

if __name__=='__main__':
    try:
        if int(constants.NOW[:2])<12:
            run(1,50)
        else:
            run(51,100)
    except Exception as err:
        print(err)
        logging.error(traceback.format_exc())
