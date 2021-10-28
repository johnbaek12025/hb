import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import six
import datetime
from datetime import timedelta, datetime
from standardcode import josa
import constants

def get_table(info:list, code:str)->str:
	# 표를 위한 데이터를 구한다
	# 폰트 사이즈 및 배경 색 조정       
    font_size_pt = 10
    title_font_size = font_size_pt    
    data_font_size = font_size_pt
    edge_colors = '#C9C9C9'
    title_face_colors = '#f3f3f3'
    title_face_colors2 = '#333333'
    now_quarter_face_colors = '#F6EEE1'
    title_font_colors = '#474747'
    font_colors = '#474747'
    font_colors2 = '#ffffff'
    red_color = '#ed3c3c'
    blue_color = '#1262d0'
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    fontprop = fm.FontProperties(fname=font_path)
    
	# 차트 크기    
    fig, ax = plt.subplots(figsize=(6, len(info)*0.5), dpi=100, facecolor=font_colors2)      
    plt.rcParams['figure.facecolor'] = font_colors2
    margins = {  # vvv margin in inches                 # 여백
        "left": 0,
        "bottom": 0.005,
        "right": 0.996,
        "top": 0.999
    }
    fig.subplots_adjust(**margins)
    header_len=[]
    name_len=[]
    rate_len=[]
    for i in info:
        name=i[0]
        rate=i[1]
        header=i[2]
        rate_len.append(rate)
        name_len.append(name)
        header_len.append(header)
    # h_len=len(max(header_len, key=len))
    n_len=len(max(name_len, key=len))
    r_len=n_len=len(max(rate_len, key=len))
    x=n_len*0.3
    y=r_len*0.15
    z=r_len*0.95

    h=1/(len(info)+1)
    pose=1-h
    # 타이틀
    table_title_list = [['관련종목', '전일비', '종목개요']]
    table_title = plt.table(cellText=table_title_list,
                            colWidths=[x, y, z],    
                            cellLoc='center',  # 각 셀 가운데 정렬
                            bbox=[0, pose, 1, h],  # 좌우 # 상하 #너비 #높이
                            edges='closed'
                            )    
    table_title.auto_set_font_size(False)
    table_title.set_fontsize(title_font_size)
    t=pose-h

    for row in info:
        # tabl
        name=row[0]
        ratio=josa.rise_fall_mark(row[1])
        header=row[2]    
        table_data_list=[[name,ratio, header]]
        table_data = plt.table( cellText=table_data_list,
                                colWidths=[x,y,z],
                                cellLoc='center',  # 각 셀 가운데 정렬
                                bbox=[0, t, 1, h],  # 좌우 # 상하 #너비 #높이
                                edges='closed',
                                loc = 'bottom')
        plt.rcParams['axes.grid'] = True
        # table_data.auto_set_font_size(False)
        table_data.set_fontsize(10)
        get_color(table_data, ratio)
        t=t-h

    # 타이틀 컬러 입히기
    for j, cell in six.iteritems(table_title._cells):
        cell.set_facecolor(title_face_colors2)
        cell.set_edgecolor(edge_colors)        
        cell.set_text_props(fontproperties=fontprop, color=font_colors2)
        table_title.set_fontsize(data_font_size)    
    ax.axis('tight')       
    ax.axis('off')
    
    
    # print(tb[0,2]._loc)
    # print('\n')
    # for j, cell in six.iteritems(table_data._cells):      
    #     if j[1] == 2:              
    #         table_data._cells[0, 2]._loc = "left"
    # plt.xticks([])
    # plt.show()

    # 차트 이미지를 저장한다
    TODAY = datetime.today().strftime("%Y%m%d")      
    img='{}{}_{}_{}.jpeg'.format(constants.PATH, TODAY, constants.NEWS_CODE, code)	
    plt.savefig(img)
    plt.close('all')
    return img


def get_color(table, ratio):    
    font_size_pt = 10
    data_font_size = font_size_pt
    edge_colors = '#C9C9C9'
    font_colors = '#474747'
    red_color = '#ed3c3c'
    blue_color = '#1262d0'
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    fontprop = fm.FontProperties(fname=font_path)
    # 데이터 컬러 입히기
    for j, cell in six.iteritems(table._cells):        
        cell.set_edgecolor(edge_colors)
        cell.set_text_props(fontproperties=fontprop, color=font_colors)
        table.set_fontsize(data_font_size)
        if j[1] == 0:
            cell._loc = 'center'            
        # cell.set_facecolor(title_face_colors)
        if j[1] == 1:
            if ratio[0] == '+':                
                cell.set_text_props(weight='normal', color=red_color)                              
            elif ratio[0] == '-':
                cell.set_text_props(weight='normal', color=blue_color)
            else:
                cell.set_text_props(weight='normal', color=font_colors)
        if j[1] == 2:
            cell.set_text_props(ha='left')