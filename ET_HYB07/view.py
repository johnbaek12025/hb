import model
from standardcode import josa
import constants


def get_para(today:str, range1:int, range2:int, L=[])->list:
    info=model.get_high_cap(today, range1, range2)
    josa.write_log(constants.LOCAL_PATH, 'get_para()', info)     
    x = {}
    for i in info:
        collect=[]
        eul = josa.def_connect_word(i[0])
        eul = eul[2][-1]
        temp_amount=model.get_today_amount(i[1], today)
        collect.append(i[0])
        collect.append(i[1])
        collect.append(i[2])
        collect.append(i[3])
        collect.append(i[4])
        if len(temp_amount)==0:            
            collect.append('')
            collect.append('')
            collect.append('')
        elif temp_amount[0][1]==0 and temp_amount[0][2]==0:
            collect.append('')
            collect.append('')
            collect.append('')
        elif None in temp_amount:
            collect.append('')
            collect.append('')
            collect.append('')
        else:
            temp_amount=temp_amount[0]                        
            if temp_amount[1]==0:        
                collect.append('')    
                collect.append(f'기관은 {i[0]}{eul} {josa.net(josa.numberToKoreanZoo(temp_amount[2]))}')
                collect.append(f", 이 시간 기관은  {josa.net(josa.numberToKoreanZoo(temp_amount[2]))}")       
            elif temp_amount[2]==0:                             
                collect.append(f'외국인은 {i[0]}{eul} {josa.net(josa.numberToKoreanZoo(temp_amount[1]))}')
                collect.append('')
                collect.append(f", 이 시간 외국인은  {josa.net(josa.numberToKoreanZoo(temp_amount[1]))}")       
            else:                
                collect.append(f'외국인은 {i[0]}{eul} {josa.net(josa.numberToKoreanZoo(temp_amount[1]))} 하고 ')
                collect.append('기관은 '+josa.net(josa.numberToKoreanZoo(temp_amount[2])))
                if abs(temp_amount[1]) > abs(temp_amount[2]):
                    collect.append(f", 이 시간 외국인 {josa.net(josa.numberToKoreanZoo(temp_amount[1]))}")
                else:
                    collect.append(f", 이 시간 기관 {josa.net(josa.numberToKoreanZoo(temp_amount[2]))}")
        L.append(collect)
        josa.write_log(constants.LOCAL_PATH, 'get_para()', L)
    return L

def get_sales(code, day5):
    josa.write_log(constants.LOCAL_PATH, 'get_sales()', code)
    info = model.get_net(code, day5)[0]
    # print(info)
    if None in info:
        alert = ''
        print('순매매량에 대한 자료가 없음')
        return alert
    for_net = josa.numberToKoreanZoo(info[0] - info[1])
    org_net = josa.numberToKoreanZoo(info[2] - info[3])
    pr_net = josa.numberToKoreanZoo(info[4] - info[5])    
    if for_net == '0주':
        alert = ''
        print('외국인의 순매매량이 0이라 기사 생성 안함')
        return alert
    elif org_net == '0주':
        if pr_net == '0주':
            para = constants.PARAGRAPH.format(f"외국인은 {josa.net(for_net)}")
            return para
        else:
            para = constants.PARAGRAPH.format(f"개인 투자자들은 {josa.net(pr_net)} 했고, 외국인은 {josa.net(for_net)}")
            return para
    else:
        if pr_net == '0주':
            para = constants.PARAGRAPH.format(f"외국인은 {josa.net(for_net)} 했고, 기관은 {josa.net(org_net)}")
            return para
        else:
            para = constants.PARAGRAPH.format(f"개인 투자자들은 {josa.net(pr_net)} 했고, 외국인과 기관은 각각  {josa.net(for_net)}, {josa.net(org_net)}")
            return para

def get_info(code:str, path:str, ratio:str, today:str)->list:
    """테이블 만들기
        거래량 대비 = 순매매량/해당 날짜 거래량
        오늘 잠정"""
    info=model.get_today_amount(code, today)    
    amount = []
    if not info:
        josa.write_log(constants.LOCAL_PATH, f'there is no data of {code}', info)
        return ''
    elif info[0][3] == 0 or info[0][3]==None:#거래량
        # print('거래량이 0이므로 해당종목 뉴스 생성 않함')        
        return ''    
    proportion1= round(abs(int(info[0][1]))/abs(int(info[0][3])) *100,2)
    proportion2 = round(abs(int(info[0][2])) / abs(int(info[0][3])) * 100,2)
    ele=[info[0][0] , ratio, info[0][1], proportion1, info[0][2], proportion2 ]
    amount.append(ele)
    cont=model.get_continuous_amount(code, constants.DAY4, constants.YESTERDAY)
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
        if proportion1==0 and proportion2==0 and proportion3==0 and proportion4==0:
            print('거래량이 0임')
            josa.write_log(constants.LOCAL_PATH, 'get_info()', '거래량이 0임')
            return ''                   
    if len(amount)<5:
        print('5일치의 데이터가 생성이 안됐으므로 테이블 생성 안함')
        return ''
    #info:list, path:str, news_code:str,code:str
    img_path=josa.get_table(amount, path, constants.NEWS_CODE,code)#테이블 만드는 구간
    return img_path
        

if __name__=='__main__':        
    get_para(constants.TODAY, 1, 50, '0950', '1050')
