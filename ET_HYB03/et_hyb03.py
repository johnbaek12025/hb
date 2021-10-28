import controller
import time
import get_db
import constants, josa
import sys

def run():
    """실행 및 비교 후 뉴스 생성
    ⓐcontroller.buil_up에서 선정된 종목코드, 제목, 첫번째 문단, 차트구간, 두번째 문단, 공통모듈 list를 변수에 저장
    ⓑfor문을 돌려서 각각을 controller.make_news에 보내기전 rtbl_news_info를 select해서 중복 체크를 한다.
    ⓒ중복 된것이 없다면, news_maker로 보내서 rtbl_cnt"""
    trade = get_db.check_trade_day()
    if not trade:
        sys.exit()
    cont = controller.build_up()
    josa.write_log(constants.LOG_PATH, 'run()', cont)
    # [title + first + link + second + common_module]
    if cont=='선정된 종목이 존재 안함':
        alert='선정된 종목이 존재 안함'
        return alert
    # print('____________________________________________________________________________________________________________')
    for row in cont:
        info=get_db.get_news(row[0])
        print(info)
        if len(info)!= 0:
            continue
        news_sn= controller.make_news(row[0], row[1], row[2], row[3], row[4], row[5])
        # controller.news_auto_sender(news_sn, constants.TODAY, constants.NEWS_CODE)
    # # print('success')
    # time.sleep(5)


 
if __name__=='__main__':
    try:
        warn=run()
    except Exception as err:
        
        print('오류',err)