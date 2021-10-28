import db
import datetime
from datetime import timedelta, datetime
import six
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import replace


def def_connect_word(name):
	import re
	# 리스트 형태로 받아야 함
	base_code, chosung, jungsung = 44032, 588, 28
	# 초성 리스트. 00 ~ 18
	chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
	# 중성 리스트. 00 ~ 20
	jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
					 'ㅣ']
	# 종성 리스트. 00 ~ 27 + 1(1개 없음)
	jongsung_list = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
					 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

	names_eunnun = []  # 은,는
	names_ega = []  # 이,가
	names_ullul = []  # 을,를
	names_gwawa = []  # 과,와
	names_eornone = []  # 이, ''(~~이라며, ~~~라며)
	for i in range(0, len(name)):
		name_keyword = name[i][-1:]
		name_keyword_list = list(name_keyword)
		name_josa = list()
		for k in range(0, len(name_keyword_list)):
			if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', name_keyword_list[k]) is not None:
				char_code = ord(name_keyword_list[k]) - base_code
				char1 = int(char_code / chosung)
				name_josa.append(chosung_list[char1])
				char2 = int((char_code - (chosung * char1)) / jungsung)
				name_josa.append(jungsung_list[char2])
				char3 = int((char_code - (chosung * char1) - (jungsung * char2)))
				name_josa.append(jongsung_list[char3])
			else:
				name_josa.append(name_keyword_list[k])
			eunnun = '는' if name_josa[-1] == ' ' else '은'
			ega = '가' if name_josa[-1] == ' ' else '이'
			ullul = '를' if name_josa[-1] == ' ' else '을'
			wagwa = '와' if name_josa[-1] == ' ' else '과'
			eornone = '' if name_josa[-1] == ' ' else '이'
			ranuneranun = '라며' if name_josa[-1] == ' ' else '이라며'
			be = '였다' if name_josa[-1] == ' ' else '이었다'
			ero = "로" if name_josa[-1] == ' ' else '으로'
			rago = '라고' if name_josa[-1] == ' ' else '이라고'
		names_eunnun.append(eunnun)
		names_ega.append(ega)
		names_ullul.append(ullul)
		names_gwawa.append(wagwa)
		names_eornone.append(eornone)
	return names_eunnun, names_ega, names_ullul, names_gwawa, names_eornone, ranuneranun, be, ero, rago

def get_comma(num):
	if int(num) < 0:
		if len(str(num)[1:]) < 4:
			num = str(num)
			return num
		elif len(str(num)[1:]) >=4 and len(str(num)[1:]) < 7:
			mark = str(num)[0]
			num = str(num)[1:]
			num = mark + str(num)[:-3] + ',' + str(num)[-3:]
			return num
		else:
			mark = str(num)[0]
			num = str(num)[1:]
			num = mark + str(num)[:-6] + ',' + str(num)[-6:][-3:] + ',' + str(num)[-6:][:-3]
			return num
	elif int(num) > 0:
		if len(str(num)) < 4:
			num = str(num)
			return num
		elif len(str(num)) >= 4 and len(str(num)) < 7:
			num = str(num)[:-3] + ',' + str(num)[-3:]
			return num
		else:
			num = str(num)[:-6] + ',' + str(num)[-6:][-3:] + ',' + str(num)[-6:][:-3]
			return num
	else:
		num = '-'
		return num


def numberToKoreanWon(num):
	# print(num)
	num = str(num)
	unit_word = ['원', '만', '억', '조', '경', '해']
	num_list = [ ]
	iteration = len(num) / 4
	if num == '0':
		return '0원'

	while(iteration > 1):
		num_list.append(num[-4:])
		num = num[:-4]
		iteration = len(num) / 4
	num_list.append(num)
	ko_won = ""
	# print(num_list)
	for i in reversed(range(len(num_list))):
		temp_str = num_list[i]
		while(temp_str[0] == "0"):
			temp_str = temp_str[1:]
			if len(temp_str) == 0:
				break

		if not len(temp_str) == 0:
			if len(temp_str) == 4:
				temp_str = temp_str[0] +  temp_str[1:]
			ko_won = ko_won + " " + temp_str +  unit_word[i]
	
	if ko_won[-1] == '원':
		pass
	else:
		ko_won = ko_won + "원"

	return ko_won[1:]

def numberToKoreanZoo(num):
	if num < 0:
		temp_append_str = '-'
	else:
		temp_append_str = ''

	num = str(abs(num))
	unit_word = ['주', '만', '억', '조', '경', '해']
	num_list = []
	iteration = len(num) / 4
	if num == '0':
		return '0주'
	
	while(iteration > 1):
		num_list.append(num[-4:])
		num = num[:-4]
		iteration = len(num) / 4
	num_list.append(num)
	ko_won = ""

	for i in reversed(range(len(num_list))):
		temp_str = num_list[i]
		while(temp_str[0] == "0"):
			temp_str = temp_str[1:]
			if len(temp_str) == 0:
				break

		if not len(temp_str) == 0:
			ko_won = ko_won + " " + temp_str +  unit_word[i]
	if ko_won[-1] == '주':
		pass
	else:
		ko_won = ko_won + " 주"

	return temp_append_str + ko_won[1:]

def getDayName(a):
	a = datetime.strptime(a, "%Y%m%d")
	return ['월','화','수','목','금','토','일'][datetime.date(a).weekday()]

# 특정일을 기준으로 개장일만 구하기
def get_day(day):
	today = datetime.today().strftime("%Y%m%d")
	cur = db.DB('rc_team')
	BUSINESS_DAY = """SELECT* 
	                FROM(select DATEDEAL 
	                     from TRADE_DAY 
	                     WHERE DATEDEAL<=:DATEDEAL 
	                     ORDER BY DATEDEAL DESC) 
	                 WHERE ROWNUM<='{}'""".format(day)
	cur.cursor.execute(BUSINESS_DAY, datedeal=today)
	info=cur.cursor.fetchall()
	info=info[int(day)-1][0]
	return info

# 코스피, 코스닥에 따라서 호가 단위 구하는 함수 
def getHogaUnit(price, marketType):
	# price의 자릿수 구하기
	print("getHogaUnit에 들어왔다")
	posNumber = 0
	temp_price = price
	hogaUnit = 0
	while (temp_price > 10):
		temp_price = temp_price / 10 
		posNumber += 1
	print(posNumber)
	# 코스피 
	if marketType == 0:
		front_price_val = price / 10**posNumber
		if front_price_val > 5:
			hogaUnit += 1
		elif front_price_val < 5:
			hogaUnit += 5

		if price < 500000:
			if posNumber <= 3:
				re_val = hogaUnit * (10**(posNumber -2))
			elif posNumber > 3:
				re_val = hogaUnit * (10**(posNumber -3))
			
			print("호가 단위는")
			print(re_val)
			print("이다")
			return re_val
		else:
			return 1000
	
	# 코스닥 
	elif marketType == 1:
		front_price_val = price / 10**posNumber
		if front_price_val > 5:
			hogaUnit += 1
		elif front_price_val < 5:
			hogaUnit += 5

		if price < 50000:
			return hogaUnit * (10**(posNumber -3))
		else:
			return 100

	# 둘 다 아니라서 None 타입 객체를 반환 
	else:
		print("마켓타입이 잘못되었습니다. DB에서 marketType을 잘 가져오는지 확인하세요. ")
		return None

# 상한가에 갔는지 확인한다. 1이면 상한가이고 0이면 아니며 None이면 market 타입등 변수가 잘못 설정되어서 오류가 발생한 경우이다.
def sanghanCheck(yesterdayJongga, toadyJongga, marketType):
	yesterday_temp_hoga = getHogaUnit(yesterdayJongga, marketType)
	today_temp_hoga = getHogaUnit(toadyJongga, marketType)
	# 오늘의 종가가 더 크니 상한가를 갔는지 확인
	if yesterdayJongga < toadyJongga:
		if yesterday_temp_hoga == None or today_temp_hoga == None:
			return None
		else:
			print("상한 체크에 들어왔다. ")
			print(yesterday_temp_hoga)
			print(toadyJongga)
			print(yesterdayJongga)
			temp_sanghanga = yesterdayJongga * 0.3 
			print(temp_sanghanga)
			a = temp_sanghanga % yesterday_temp_hoga
			temp_sanghanga = temp_sanghanga - a
			print(a)
			print(temp_sanghanga)
			temp_sanghanga = yesterdayJongga + temp_sanghanga

			yesterday_temp_hoga = getHogaUnit(temp_sanghanga, marketType)
			c = temp_sanghanga % yesterday_temp_hoga
			temp_sanghanga = temp_sanghanga - c
			print(c)
			print("어제 것과 오늘 것을 비교한다")
			print(temp_sanghanga)
			print(toadyJongga)
		
		if toadyJongga == int(temp_sanghanga):
			return 1
		else:
			return 0

	# 하한가를 갔는지 확인
	else:
		if yesterday_temp_hoga == None or today_temp_hoga == None:
			return None
		else:
			temp_sanghanga = yesterdayJongga * 0.3 
			a = temp_sanghanga % yesterday_temp_hoga
			temp_sanghanga = temp_sanghanga - a
			temp_sanghanga = yesterdayJongga - temp_sanghanga

			yesterday_temp_hoga = getHogaUnit(temp_sanghanga, marketType)
			c = temp_sanghanga % yesterday_temp_hoga
			temp_sanghanga = temp_sanghanga - c

		if toadyJongga == int(temp_sanghanga):
			return 1
		else:
			return 0

def am_pm(time):
	time=int(time)
	if time>12:
		hh='오후 '+str(int(time)-12)
		return hh
	else:
		time='오전 '+str(time)
		return time
#기간을 PARAMETER로 받아서
#기간이 30일보다 작으면 그냥 RETURN
#60일 보다 많으면 달로 계산하여 RETURN
def count_month(num):
    month=int(num/30)
    if month<1:
        return str(num)+'일'
    elif month == 1:
        return str(num)+'일'
    else:
        return str(month)+'개월'

#순매매량을 받아서
#-가 있으면 -빼고 순매도를 붙여서 RETURN
#- 없으면 순매수를 붙여서 RETURN
def net(num):
	if num[0]=='-':
		num=num.replace("-", '')
		num=num+' 순매도'
		return num
	else:
		num=num+' 순매수'
		return num
#시퀀스 생성
def get_seq():
	seq=db.DB('news_user')
	SEQ_SQL="""SELECT NEWS_USER.RTBL_NEWS_SEQUENCE.NEXTVAL FROM DUAL"""
	seq.cursor.execute(SEQ_SQL)
	seq_tuple_list = seq.cursor.fetchall()
	seq = seq_tuple_list[0][0]
	return seq

#재귀
def find_last_index(target, org_string, last_idx):
	target_idx = org_string[last_idx+1:].find(target)
	if target_idx != -1:
		return find_last_index(target=target, org_string=org_string, last_idx= 1 + last_idx + target_idx)
	else:
		return last_idx

def get_mark(ratio):
	if float(ratio) < 0:
		return '▼' + str(ratio)[1:]
	elif float(ratio) > 0:
		return '▲' + str(ratio)
	else:
		return '-'

def get_div(num):
	if len(str(num)) == 4:
		num = str(num)
		num = num[:-2] + ':' + num[-2:]+' 잠정'
		return num
	else:
		num = str(num)
		num = num[:-4] + '/' + num[-4:][:-2] + '/' + num[-4:][-2:]
		return num

def get_table(info, code):
	# 표를 위한 데이터를 구한다
	# 폰트 사이즈 및 배경 색 조정
	font_size_px = 23
	font_size_pt = 13
	title_font_size = font_size_pt
	index_col_font_size = font_size_pt
	data_font_size = font_size_pt
	edge_colors = '#C9C9C9'
	face_colors = '#ffffff'
	title_face_colors = '#f3f3f3'
	title_face_colors2 = '#677485'
	now_quarter_face_colors = '#F6EEE1'
	title_font_colors = '#474747'
	font_colors = '#474747'
	font_colors2 = '#ffffff'
	red_color = '#ed3c3c'
	blue_color = '#1262d0'
	font_path = 'C:/Windows/Fonts/malgun.ttf'
	fontprop = fm.FontProperties(fname=font_path)

	# 차트 크기
	size = (6.0, 3)
	fig, ax = plt.subplots(figsize=size, dpi=100, facecolor=font_colors2)
	plt.rcParams['figure.facecolor'] = font_colors2
	margins = {  # vvv margin in inches                 # 여백
		"left": 0,
		"bottom": 0.005,
		"right": 0.996,
		"top": 0.999
	}
	fig.subplots_adjust(**margins)

	# 타이틀1
	table_title_list = [['날짜 (등락률)', '외국인 (거래량대비)', '기관계 (거래량대비)']]
	table_title = plt.table(cellText=table_title_list,
							loc='center',
							cellLoc='center',  # 각 셀 가운데 정렬
							bbox=[0.0, 0.8334, 1, 0.1666],  # 좌우 # 상하 #너비 #높이
							)

	table_title.auto_set_font_size(False)
	table_title.set_fontsize(title_font_size)

	# tabl1
	mark=get_mark(info[0][1])
	fore = get_comma(info[0][2])
	org = get_comma(info[0][4])
	date=get_div(info[0][0])
	table_data1_list = [[ date+ ' (' + mark + '% )', fore + ' ' + '(' + str(info[0][3]) + '%)', org + ' ' + '(' + str(info[0][5]) + '% )']]
	table_data1 = plt.table(cellText=table_data1_list,
							loc='center',
							cellLoc='right',  # 각 셀 가운데 정렬
							bbox=[0, 0.6668, 1.0, 0.1666],  # 좌우 # 상하 #너비 #높이
							)

	table_data1.auto_set_font_size(False)
	table_data1.set_fontsize(data_font_size)

	# tabl2
	date=get_div(info[1][0])
	mark=get_mark(info[1][1])
	fore=get_comma(info[1][2])
	org = get_comma(info[1][4])
	table_data2_list = [[date+ ' (' + mark + '% )', str(fore) + ' ' + '('+str(info[1][3])+'%)', str(org) + ' ' + '('+ str(info[1][5])+ '%)']]
	table_data2 = plt.table(cellText=table_data2_list,
							loc='bottom',
							cellLoc='right',  # 각 셀 가운데 정렬
							bbox=[0, 0.5002, 1.0, 0.1666],  # 좌우 # 상하 #너비 #높이
							)
	table_data2.auto_set_font_size(False)
	table_data2.set_fontsize(data_font_size)

	# tabl3
	date=get_div(info[2][0])
	mark=get_mark(info[2][1])
	fore = get_comma(info[2][2])
	org = get_comma(info[2][4])
	table_data3_list = [[date + ' (' + mark + '% )', fore + ' ' + '(' + str(info[2][3]) + '%)', org + ' ' + '(' + str(info[2][5]) + '%)']]
	table_data3 = plt.table(cellText=table_data3_list,
							loc='bottom',
							cellLoc='right',  # 각 셀 가운데 정렬
							bbox=[0, 0.3336, 1.0, 0.1666],  # 좌우 # 상하 #너비 #높이
							)
	table_data3.auto_set_font_size(False)
	table_data3.set_fontsize(data_font_size)

	# tabl4
	date = get_div(info[3][0])
	mark=get_mark(info[3][1])
	fore = get_comma(info[3][2])
	org = get_comma(info[3][4])
	table_data4_list = [[date + ' (' + mark + '% )', fore + ' ' + '(' + str(info[3][3]) + '%)', org + ' ' + '(' + str(info[3][5]) + '%)']]
	table_data4 = plt.table(cellText=table_data4_list,
							loc='bottom',
							cellLoc='right',  # 각 셀 가운데 정렬
							bbox=[0, 0.167, 1.0, 0.1666],  # 좌우 # 상하 #너비 #높이
							)
	table_data4.auto_set_font_size(False)
	table_data4.set_fontsize(data_font_size)

	# table5
	date = get_div(info[4][0])
	mark=get_mark(info[4][1])
	fore = get_comma(info[4][2])
	org = get_comma(info[4][4])
	table_data5_list = [[date + ' (' + mark + '% )', fore + ' ' + '(' + str(info[4][3]) + '%)', org + ' ' + '(' + str(info[4][5]) + '%)']]
	table_data5 = plt.table(cellText=table_data5_list,
							loc='bottom',
							cellLoc='right',  # 각 셀 가운데 정렬
							bbox=[0, 0.0, 1.0, 0.167],  # 좌우 # 상하 #너비 #높이
							)
	table_data5.auto_set_font_size(False)
	table_data5.set_fontsize(data_font_size)

	# 타이틀 컬러 입히기
	for j, cell in six.iteritems(table_title._cells):
		cell.set_facecolor(title_face_colors2)
		cell.set_edgecolor(edge_colors)
		cell.set_text_props(fontproperties=fontprop, color=font_colors2)
		table_title.set_fontsize(data_font_size)
		if j[1] == 0:
			cell._loc = 'center'

	get_color(table_data1, info[0][2], info[0][4])
	get_color(table_data2, info[1][2], info[1][4])
	get_color(table_data3, info[2][2], info[2][4])
	get_color(table_data4, info[3][2], info[3][4])
	get_color(table_data5, info[4][2], info[4][4])

	ax.axis('off')
	plt.xticks([])

	# 차트 이미지를 저장한다
	TODAY = datetime.today().strftime("%Y%m%d")
	plt.savefig('.\\img\\'+TODAY+'test_ET_HYB04_'+code+'.jpeg')
	plt.close('all')


def get_color(table, fore, org):
	font_size_pt = 13
	data_font_size = font_size_pt
	edge_colors = '#C9C9C9'
	font_colors = '#474747'
	red_color = '#ed3c3c'
	blue_color = '#1262d0'
	font_path = 'C:/Windows/Fonts/malgun.ttf'
	fontprop = fm.FontProperties(fname=font_path)
	# 데이터1 컬러 입히기
	for j, cell in six.iteritems(table._cells):
		cell.set_edgecolor(edge_colors)
		cell.set_text_props(fontproperties=fontprop, color=font_colors)

		table.set_fontsize(data_font_size)
		if j[1] == 0:
			cell._loc = 'center'
		# cell.set_facecolor(title_face_colors)
		if j[1] == 1:
			if fore < 0:
				cell.set_text_props(weight='normal', color=blue_color)

			if fore > 0:
				cell.set_text_props(weight='normal', color=red_color)
		if j[1] == 2:
			if org > 0:
				cell.set_text_props(weight='normal', color=red_color)
			if org < 0:
				cell.set_text_props(weight='normal', color=blue_color)

def get_rise_drop_mark(ratio):
	if float(ratio) < 0:
		r = f"{str(ratio)[1:]}% 하락한"
		return r
	else:
		r = f"{str(ratio)}% 상승한"
		return r

def get_rise_drop(ratio):
	if float(ratio) < 0:
		r = f"-{str(ratio)[1:]}% 하락"
		return r
	else:
		r = f"+{str(ratio)}% 상승"
		return r

def filtering_buy(opinion, goal_value):
	"""buy나 hold 같은 것을 goal_value에 따라 필터링 함수"""
	if goal_value==None:
		return ''
	else:
		if 'B' in opinion:
			return " 투자의견 '"+opinion+"'의"
		else:
			return ''
def delete_space(para):
	para=para.replace('.', '')
	if para[-1]==' ':
		return para[:-1]
	else :
		return para

def write_log(path, name, something):
    f = open("{}{}.txt".format(path,name), 'w')
    f.write(str(something))
    f.close()