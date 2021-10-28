import constants
from datetime import datetime
import josa
import view
import model
import controller
import sys
import logging, traceback, os

logging.basicConfig(level=logging.ERROR)


def run():
    trade = model.check_trade_day()
    if not trade:
        josa.write_log(constants.LOG_PATH, 'trade day', '휴장')
        sys.exit()

    info = model.get_info()
    josa.write_log(constants.LOG_PATH, 'run()', info)
    if len(info) == 0:
        alert = '장 시작 전 이거나 자료가 없음'
        return alert
    sorted_list = []
    for row in info:
        if None in row:
            alert = 'DB tuple에 None 값이 존재'
            continue
        sorted_list.append(row)
    i = view.get_para(sorted_list)
    for row in i:
        code = row[0]
        url = row[1]
        title = row[2]
        paragraph = ''.join(row[3]) + ''.join(row[4]) + ''.join(row[5]) + ''.join(row[6]) + ''.join(row[7])        
        signal = model.get_duplication(code)
        if len(signal) != 0:
            print('중복')
            continue
        news_sn = controller.make_news(code, url, title, paragraph)
        # controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)


if __name__ == '__main__':
    try:
        result = run()
        print(result)
    except Exception as err:
        print(err)
        logging.error(traceback.format_exc())
        sys.exit()