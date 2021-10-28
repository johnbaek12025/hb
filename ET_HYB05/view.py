import model
import josa
import constants
from datetime import datetime
import time


def get_para(info):
    josa.write_log(constants.LOG_PATH, 'get_para()', info)
    Low=[]
    for row in info:
        if None in row:
            if row[7]==None or row[6]==None:
                pass
            else:
                continue
        content=[]
        name=row[0]
        code=row[1]
        header=row[2]
        price=josa.numberToKoreanWon(row[3])
        ratio1=josa.get_rise_drop(row[4])
        ratio2 = josa.get_rise_drop_mark(row[4])
        org=row[5]
        opinion=row[6]
        goal_value=row[7]
        article=row[8]
        cont=row[9]
        cont=josa.delete_space(cont)
        eun=josa.def_connect_word(name)[0][-1]
        ro=josa.def_connect_word(header)[-2]
        era = josa.def_connect_word(article)[-4]
        rago = josa.def_connect_word(cont[-1])[-1]
        now = datetime.today().strftime("%H%M")
        hh=josa.am_pm(now[:-2])
        mm=now[-2:]
        opi=josa.filtering_buy(opinion, goal_value)        
        title = f"""[리포트특징주] {name} {ratio1}... '{article}'"""
        # NAME,JOSA, DAY, HOUR, MINUTES, RATIO, PRICE
        para1=constants.PARA1.format(name,eun, constants.DAY, hh, mm ,ratio2, price)
        # NAME, JOSA, HEADER, JOSA
        para2=constants.PARA2.format(name, eun, header, ro)
        url=constants.LINK.format(code)
        link=constants.LINK1.format(url)+'<br><br>'
        #org, josa, name, josa, article, JOSA, opionion
        eun = josa.def_connect_word(org)[0][-1]
        wa = josa.def_connect_word(name)[3][-1]        
        para3=constants.PARA3.format(org, eun, name, wa,  article, era, opi)        
        #cont, rago
        para4=constants.PARA4.format(cont,rago)
        content.append(code)
        content.append(url)
        content.append(title)
        content.append(para1)
        content.append(para2)
        content.append(link)
        content.append(para3)
        content.append(para4)        
        Low.append(content)        
    return Low







if __name__ == '__main__':
    info=model.get_info()
    i=get_para(info)
    for row in i:
        print(row)
