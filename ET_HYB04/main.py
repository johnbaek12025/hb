import controller
import model
import view
import constants
import josa
import db
import sys
from CommonModule import main as cm
import time
import logging, traceback, os
logging.basicConfig(level=logging.ERROR)
logging.error(traceback.format_exc())
path=os.path.dirname(os.path.abspath(__file__))+'\\img'

def run():
    trade = model.check_trade_day()
    if not trade:
        sys.exit()

    curprice = model.get_curprice()
    info = controller.para1(curprice)
    josa.write_log(constants.LOG_PATH, 'run1()', info)
    for row in info:
        """ para1->code,ratio,name,who,amount,info"""
        code = row[0]
        ratio = row[1]
        name = row[2]
        who = row[3]
        amount = row[4]
        content = row[5]
        article = model.get_duplication(code)
        if len(article) > 0:
            print('중복된 기사')
            continue
        img_path = view.get_info(code, path, ratio)
        if len(img_path) == 0:
            continue
        localpath = img_path
        filepath = constants.FILEPATH.format(constants.NEWS_CODE, code)
        db.DB.get_trans('', localpath, filepath)
        dt = josa.get_separated_date(constants.TODAY)
        html = constants.HTML.format(dt, constants.NEWS_CODE,code)
        #para1-> name, ratio, who, amount, net buying
        deal = josa.get_dealing_str(int(ratio))
        title = constants.TITLE.format(name, ratio, who, amount, f'대량 {deal}')
        second = controller.second_para(code)
        com = cm.run(code)        
        news_sn=controller.make_news(code, title, content, second, html, com)
        controller.news_auto_sender(news_sn, constants.TODAY ,constants.NEWS_CODE)

    info = controller.para2(curprice)
    josa.write_log(constants.LOG_PATH, 'run2()', info)
    for row in info:
        """para2->code,ratio,name,who,term,info"""
        code = row[0]
        ratio = row[1]
        name = row[2] 
        who = row[3]
        term = row[4]
        content = row[5]
        article = model.get_duplication(code)
        if len(article) > 0:
            continue
        img_path = view.get_info(code, path, ratio)
        if len(img_path) == 0:
            continue
        localpath = img_path
        filepath = constants.FILEPATH.format(constants.NEWS_CODE, code)
        db.DB.get_trans('', localpath, filepath)
        dt = josa.get_separated_date(constants.TODAY)
        html = constants.HTML.format(dt, constants.NEWS_CODE,code)
        #para2-> name, ratio, who, period, net buying
        deal = josa.get_dealing_str(int(ratio))
        title = constants.TITLE.format(name, ratio, who, str(term) + '일', f'연속 {deal}행진')
        second = controller.second_para(code)
        com = cm.run(code)
        news_sn = controller.make_news(code, title, content, second, html, com)
        controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)

    info = controller.para3(curprice)
    josa.write_log(constants.LOG_PATH, 'run3()', info)
    for row in info:
        """para3->code,ratio,name,info"""
        code = row[0]
        ratio = row[1]
        name = row[2]
        content = row[3]
        article = model.get_duplication(code)
        if len(article) > 0:
            continue
        img_path = view.get_info(code, path, ratio)
        if len(img_path) == 0:
            continue
        localpath = img_path
        filepath = constants.FILEPATH.format(constants.NEWS_CODE, code)
        db.DB.get_trans('', localpath, filepath)
        dt = josa.get_separated_date(constants.TODAY)
        title = constants.TITLE2.format(name, ratio)
        second = controller.second_para(code)
        html = constants.HTML.format(dt, constants.NEWS_CODE,code)
        com = cm.run(code)
        news_sn = controller.make_news(code, title, content, second, html, com)
        # controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)

if __name__ == '__main__':
    try:
            run()

    except Exception as err:
        logging.error(traceback.format_exc())
        time.sleep(5)
        sys.exit()