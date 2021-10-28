
from datetime import datetime, timedelta
import cx_Oracle

def def_connect_word(name):
    import re
    # 리스트 형태로 받아야 함
    base_code, chosung, jungsung = 44032, 588, 28
    # 초성 리스트. 00 ~ 18
    chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    # 중성 리스트. 00 ~ 20
    jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
    jongsung_list = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    names_eunnun = []       # 은,는
    names_ega = []          # 이,가
    names_ullul = []        # 을,를
    names_gwawa = []        # 과,와
    names_eornone = []      # 이, ''(~~이라며, ~~~라며)
    for i in range(0, len(name)) :
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
            ranuneranun = '라는' if name_josa[-1] == ' ' else '이라는'
            be = '였다' if name_josa[-1] == ' ' else '이었다'
            ero = "로" if name_josa[-1] == ' ' else '으로'
            rago = '라고' if name_josa[-1] == ' ' else '이라고'
        names_eunnun.append(eunnun)
        names_ega.append(ega)
        names_ullul.append(ullul)
        names_gwawa.append(wagwa)
        names_eornone.append(eornone)
    return names_eunnun, names_ega, names_ullul, names_gwawa, names_eornone, ranuneranun, be, ero, rago

def numberToKoreanWon(num):
	print(num)
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
	print(num_list)
	for i in reversed(range(len(num_list))):
		temp_str = num_list[i]
		while(temp_str[0] == "0"):
			temp_str = temp_str[1:]
			if len(temp_str) == 0:
				break

		if not len(temp_str) == 0:
			if len(temp_str) == 4:
				temp_str = temp_str[0] + temp_str[1:]
			ko_won = ko_won + " " + temp_str +  unit_word[i]
	
	if ko_won[-1] == '원':
		pass
	else:
		ko_won = ko_won + " 원"

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
def getWeekdate(today, day):
	before_4day = {}
	#최근 4일 전의 날짜 구하기
	week_date = []
	sql = "select datedeal from (select distinct datedeal from trade_day where datedeal <=:today order by datedeal desc) where rownum <=:day"
	cur.execute(sql, today = today, day=day)
	today_date = datetime.strptime(today, "%Y%m%d").date()
	for row in cur:
	    before_4day[row[0]] = 1
	
	minusday = day -1
	for i in before_4day:
		temp_Date = today_date - timedelta(minusday)
		temp_Date = temp_Date.strftime('%Y%m%d')
		value = before_4day.get(temp_Date, None)
		if value is not None:
				week_date.append(temp_Date)
		minusday -= 1
	return week_date

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

def write_log(path, name, something):
    f = open("{}{}.txt".format(path, name), 'w')
    f.write(str(something))
    f.close()