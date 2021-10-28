import get_db
import constants
import josa
import db


def get_up_down(value):
    if value > 0:
        return "↑"
    return "↓"

def get_size_rising(value):
    if value > 0:
        return "상승"
    return "하락"

def get_contents(themename, name, ratio, summary, kind):
        josa.write_log(constants.LOG_PATH, 'get_contents1', [themename, name, ratio, summary, kind])

        """제목, 첫번째 문단 구성
        ⓐparameter로 선정된 종목의 
          테마명, 선정된 종목명, 종목의 전일대비 등락율, 선정된 종목의 기업개요, 
          선정된 종목의 테마와 관련있는 다른 종목과 종목의 전일 대비 등락율 받아온다.
        ⓑ 받아온 parameter들로 테마특징주의 제목, 첫번째 문단 그리고 
           선정된 종목의 기업개요가 있는 경우와 없는 경우를 비교
        ⓒ기업 개요 없는 경우 두번째 문단 생성 하지 않는다.
        ⓓ기업 개요가 있는 경우 첫번째 문단에 붙인다.
        ⓔ선정된 종목의 테마와 관련된 기업들이 있는 경우와 
           그 개수에 따른 두번째 문단생성 coding
        ⓕ각각의 정보가 존재 하지 않을 경우에 대해 return을 다르게 함"""
        day = constants.TODAY[-2:]
        title = f"[테마특징주]{name}, {themename} 테마 {get_size_rising(float(ratio))}에  {ratio}% {get_up_down(float(ratio))}"
        first_para= day+'일 '+themename+' 관련 종목들이 강세를 보이는 가운데, '+name+'도 전일 대비 '+ratio+'% 상승하며 급등하고 있다. '
        if len(summary)==0:
            alert='기업 개요 없으므로 두번째 문단 생성하지 않음'
            print(alert)
            return title, first_para, ''
        else:
            pass
        #조사 모듈 사용
        eun = josa.def_connect_word(name)
        ro = josa.def_connect_word(summary)
        # print(ro)
        # print(eun[0][-1:])
        first_para=first_para+name+eun[0][-1:][0]+' '+summary+ro[7]+' 알려져 있다.'
        # print(first_para)
        print('--------------------')
        if len(kind)==0:
            alert = '관련 종목 없으므로 두번째 문단 생성 하지 않음'
            print(alert)
            return title, first_para, ''
        elif len(kind)==1:
            second_para=themename+'관련 종목 등은 '+name+' 이외에도 '+kind[0][0]+'('+str(kind[0][1])+'%) 등이 오름세를 보이고 있다.'
        elif len(kind)==2:
            second_para=themename+'관련 종목 등은 '+name+' 이외에도 '+kind[0][0]+'('+str(kind[0][1])+'%), ' \
                                ''+kind[1][0]+'('+str(kind[1][1])+'%) 등이 오름세를 보이고 있다.'
        else:
            second_para = themename + '관련 종목 등은 ' + name + ' 이외에도 ' + kind[0][0] + '(' + str(kind[0][1])+'%), ' \
                          + kind[1][0] + '(' + str(kind[1][1])+'%), ' + kind[2][0] + '(' + str(kind[2][1])+'%) 등이 오름세를 보이고 있다.'



        return title, first_para, second_para







if __name__=='__main__':
    cur=db.DB('rc_team')
    cur.cursor.execute(constants.KOSPIRATIO)
    kospi=cur.cursor.fetchall()
    kospi=kospi[0][0]
    pday=get_db.get_previous_day()
    if kospi<=1.0:
        stk_list=get_db.get_kind(pday, '5')
    else:
        stk_list=get_db.get_kind(pday, '7')
    # print(stk_list)
    for row in stk_list:
        # print('선정된 종목:',row)
        theme=get_db.get_theme(pday,row[1])
        # print('선정된 종목의 평균등락률이 가장 높은 테마명:',theme)
        rname=get_db.get_side(pday, theme[1], theme[2])
        # print('위의 테마명에 해당 하는 선정된 종목 이외의 종목들:',rname)
        #(themename, name, ratio, summary, kind)
        # print(theme[0])
        # print(row[0])
        # print(str(row[2]))
        # print(row[3])
        # print(len(rname))
        s,b=get_contents(theme[0], row[0], str(row[2]), row[3], list(rname))
        # print(s,b)
