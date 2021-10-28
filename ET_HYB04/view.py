import model
import datetime
import josa
import constants
import sys, db
import logging, traceback, os
logging.basicConfig(level=logging.ERROR)

def get_comparea(info, val):
    """당일 외국인, 기관이 순매수 1만주 이상 샀는지 비교"""
    group=[]
    if None in info:
        print('당일 외국인, 기관이 순매수 1만주 이상 샀는지 비교하는 과정에서 None이 나옴')
        sys.exit()
    elif len(info)==0:
        print('현재 전일대비 3%이상인 종목 없음')
        alert='현재 전일대비 3%이상인 종목 없음'
        return alert
    for row in info:
        sub=[]
        # print(row)
        amount=val(row[1], constants.BEFORE, constants.NOW)
        # print(amount)
        if len(amount)==0:
            continue
        elif amount[0] == None:
            print('기관이나 외국인의 순매수량 값이 None')
            continue
        else:
            sub.append(row[0])
            sub.append(row[1])
            sub.append(row[2])
            sub.append(row[3])
            sub.append(amount[0][0])
            group.append(sub)
    return group

def get_compareb(val,group):
    """최근10개(당일제외, 날짜무시) "순매매절대값" 평균의 2배 이상인지 비교"""
    article=[]
    info=val(group[1])
    josa.write_log(constants.LOG_PATH, 'get_compareb()', info)
    if None in info:
        print('최근10개(당일제외, 날짜무시) "순매매절대값" 평균의 2배 이상인지 비교하는 과정에서 None이 나옴')
        sys.exit()
    # print(info)
    if group[4]<2*int(info[0][1]):
        return ''
    else:        
        article.append(group[0])
        article.append(group[1])
        article.append(group[2])
        article.append(group[3])
        article.append(group[4])
    return article

def get_para1(curprice, val1, val2,  who, filter=[]):
    josa.write_log(constants.LOG_PATH, 'get_para1()', curprice)
    """val1 = model.get_org or model.get_for
       val2 = model.abs_org_value or model.abs_for_value
       ⓐ전일대비 3%이상인 종목 외국인, 기관의 model의 함수를 매개로 받는다.
       ⓑ해당 종목에 대해 잠정적으로 1만주 이상 순매수 했는지 비교
       ⓒ비교한후 그것을 list로 받는다.
       ⓓ다시 for문을 돌리면서 걸러진 종목에 대해 순매매절대값 평균의 2배이상인지 비교
       ⓔ걸러진 종목의 정보를 list로 return"""    
    info = get_comparea(curprice,val1)
    for row in info:
        cont=get_compareb(val2,row)
        if len(cont) == 0:
            continue
        elif None in cont:
            continue
        sub=[]
        sub.append(cont[0])
        sub.append(cont[1])
        sub.append(cont[2])
        sub.append(cont[3])
        sub.append(cont[4])
        sub.append(who)
        filter.append(sub)
    return filter

def get_today(curprice, val, who):
    """기관이나 외국인이 오늘 순매매한 종목을 추출"""
    article=[]
    for row in curprice:
        info=val(row[1], constants.BEFORE, constants.NOW)
        if len(info)==0:
            continue
        elif None in info:
            continue
        inven=[]        
        inven.append(row[0])
        inven.append(row[1])
        inven.append(row[2])
        inven.append(row[3])
        inven.append(who)
        inven.append(info[0][0])
        article.append(inven)
    return article

def get_period():
    period = []
    for i in range(2, 21):
        day = josa.get_day(i)
        period.append(str(day))
    return period

def get_continu(article,val):
    """기관이나 외국인이 연속적으로 순매매를 했는지 체크하기위한"""
    straigt = []
    period=get_period()
    for row in article:
        k = 1
        sum=row[5]
        for n,i in enumerate(period):
            info=val(row[1], i)
            if None in info:
                continue
            if len(info)==0:
                break
            if len(straigt)!=0: #중복 제거하는 부분
                for x in straigt:
                    if row[0] in x:
                        straigt.remove(x)
            continuous=[]
            k = k + 1
            continuous.append( row[0])
            continuous.append(row[1])
            continuous.append(row[2])
            continuous.append(row[3])
            continuous.append( row[4])
            sum = sum + info[0][2]
            continuous.append(sum)
            continuous.append(k)
            straigt.append(continuous)
    follow=[]
    for i in straigt:
        if i[6]<5:
            continue
        cont=[]
        cont.append(i[0])
        cont.append(i[1])
        cont.append(i[2])
        cont.append(i[3])
        cont.append(i[4])
        cont.append(i[5])
        cont.append(i[6])
        follow.append(cont)
    # print(follow)
    return follow

def get_para2(curprice, val1, val2, who):
    josa.write_log(constants.LOG_PATH,'get_para2()', curprice)
    """val1=model.today_org or model.today_for
   val2=model.get_org_continuous or model.get_for_continuous
   해당 종목에 대해 몇일간 순매수 하는지"""
    info=get_today(curprice, val1, who)
    josa.write_log(constants.LOG_PATH, 'get_today()', info)
    total=get_continu(info, val2)
    josa.write_log(constants.LOG_PATH, 'get_continue()', total)
    return total

def comapare_big(l1, l2):
    josa.write_log(constants.LOG_PATH,'compare_big()', l1)
    new_l=[]
    if len(l1)==0:
        return l2
    elif len(l2)==0:
        return l1
    for row in l1:
        for col in l2:
            if row[0]==col[0] and row[1]==col[1]:
                if row[5]>col[5]:
                    new_l.append(row)
                else:
                    continue
            else:
                if row in new_l:
                    if col in new_l:
                        continue
                    else:
                        new_l.append(col)
                else:
                    new_l.append(row)
    return new_l
        
def get_now(curprice):
    josa.write_log(constants.LOG_PATH,'get_now()', curprice)
    """동시순매매
        ⓐ전일대비 3%이상인 종목을 매개변수로 받아온다.
        ⓑ당일 기관과 외국인이 3000주이상 순매매한 종목인지 걸른다.
        """
    accompany=[]
    for row in curprice:        
        info=model.get_together(row[1], constants.BEFORE, constants.NOW)
        if len(info)==0:
            continue
        elif None in info:
            continue
        gather=[]
        gather.append(row[0])
        gather.append(row[1])
        gather.append(row[2])
        gather.append(row[3])
        gather.append(info[0][0])
        gather.append(info[0][1])
        accompany.append(gather)
    return accompany

def get_second(code):
    josa.write_log(constants.LOG_PATH,'get_second()', code)
    """추출한 종목에 대해서 오늘 포함 5영업일간 순매수량 추출"""
    info=model.get_detail(code, constants.BEFORE, constants.NOW)
    return info

def get_info(code:str, path:str, ratio:str)->list:
    josa.write_log(constants.LOG_PATH,'get_info()', code)
    """테이블 만들기
        거래량 대비 = 순매매량/해당 날짜 거래량
        오늘 잠정"""
    info=model.get_today_amount(code, constants.BEFORE, constants.NOW)
    amount = []
    if info[0][3] == 0 or info[0][3]==None:#거래량
        print('거래량이 0이므로 해당종목 뉴스 생성 않함')
        josa.write_log(constants.LOG_PATH,'get_info()1', '1')
        return ''
    josa.write_log(constants.LOG_PATH,'get_info()2', '1')
    proportion1= round(abs(int(info[0][1]))/abs(int(info[0][3])) *100,2)
    proportion2 = round(abs(int(info[0][2])) / abs(int(info[0][3])) * 100,2)
    ele=[info[0][0] , ratio, info[0][1], proportion1, info[0][2], proportion2 ]
    amount.append(ele)
    cont=model.get_continuous_amount(code, constants.DAY5, constants.YESTERDAY)
    rate=model.get_ratio(code,constants.DAY5, constants.YESTERDAY)
    k=0
    for i in cont:
        if None in i:
            print('테이블 만들기위한 정보 추출과정에서 None이 나옴')
            return ''
        ele2=[]
        if int(rate[k][1])==0:
            continue
        ele2.append(i[0])
        ele2.append(rate[k][0])
        ele2.append(i[1])
        proportion3=round(abs(int(i[1]))/abs(int(rate[k][1]))*100,2)
        ele2.append(proportion3)
        ele2.append(i[2])
        proportion4 = round(abs(int(i[2])) / abs(int(rate[k][1])) * 100, 2)
        ele2.append(proportion4)
        amount.append(ele2)
        k=k+1
    if len(amount)<5:
        print('5일치의 데이터가 생성이 안됐으므로 테이블 생성 안함')
        return ''
    #info:list, path:str, news_code:str,code:str
    img_path=josa.get_table(amount, path, constants.NEWS_CODE,code)#테이블 만드는 구간
    return img_path


if __name__=='__main__':
    # curprice=model.get_curprice()
    # fore=get_para2(curprice, model.today_for, model.get_for_continuous, '외국인')
    # print('외국인')
    # org=get_para2(curprice, model.today_org, model.get_org_continuous)
    # print('기관')
    # print(fore)
    # print(org)

    # together=get_now(curprice)
    info=get_info('336260','10.4')

    # for row in together:
    #     print(row)
 
