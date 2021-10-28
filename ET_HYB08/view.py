import model
import constants
from standardcode import db, josa

def get_first_para(keywords:list,date:str, L=[])->list:
    josa.write_log(constants.LOG_PATH, 'get_first_para()', keywords)
    for keyword in keywords:
        collect=[]        
        if None in keyword:
            continue
        collect.append(keyword[0])
        keyword=keyword[0] 
        stkkind=model.get_kind(date, keyword)
        josa.write_log(constants.LOG_PATH, 'model.get_kind()', stkkind)
        if len(stkkind)<2:
            continue
        kind=[]
        content=[]
        for row in stkkind:
            cont=[]                                  
            kind.append(row[0])            
            cont.append(row[0])
            cont.append(row[1])
            cont.append(row[3])
            content.append(cont)
        collect.append(kind)                                                
        collect.append(stkkind[0])
        collect.append(stkkind[1])                
        collect.append(content)
        L.append(collect)        
    return L        

def get_first_para_2(keywords:list,date:str, L=[])->list:
    josa.write_log(constants.LOG_PATH, 'get_first_para_2()', keywords)
    for keyword in keywords:
        collect=[]        
        if None in keyword:
            continue
        collect.append(keyword[0])
        keyword=keyword[0] 
        stkkind=model.get_kind_2(date, keyword)
        josa.write_log(constants.LOG_PATH, 'model.get_kind()', stkkind)
        if len(stkkind)<2:
            continue
        kind=[]
        content=[]
        for row in stkkind:
            cont=[]                                  
            kind.append(row[0])            
            cont.append(row[0])
            cont.append(row[1])
            cont.append(row[3])
            content.append(cont)
        collect.append(kind)                                                
        collect.append(stkkind[0])
        collect.append(stkkind[1])                
        collect.append(content)
        L.append(collect)        
    return L        

def get_trading_signal(code1:str, code2:str, day:str, day5:str)->str:
    signal1=model.extract_signal(code1, day, day5)
    josa.write_log(constants.LOG_PATH, 'signal1', signal1)
    signal2=model.extract_signal(code2, day, day5)
    josa.write_log(constants.LOG_PATH, 'signal2', signal2)
    if len(signal1)==0 and len(signal2)==0:
        return ''
    if len(signal1)==0:
        name2=signal2[0][1]
        residue=signal2[0][2]
        para1=josa.signal_make_para(name2, residue)+'됐다. <br><br>'
        return para1        
    elif len(signal2)==0:            
        name1=signal1[0][1]
        residue=signal1[0][2]        
        para2=josa.signal_make_para(name1, residue)+'하였다. <br><br>'
        return para2
    else:
        name1=signal1[0][1]
        residue1=signal1[0][2]        
        para1=josa.signal_make_para(name1, residue1)
        name2=signal2[0][1]
        residue2=signal2[0][2]
        para2=josa.signal_make_para(name2, residue2)
        para=para1+'했고, '+para2+'하였다. <br><br>'
        return para

def get_collect(contents:list):
    josa.write_log(constants.LOG_PATH, 'get_collect()', contents)
    L=[]
    # print('contents',contents)
    for row in contents:
        collect=[]        
        ratio=str(row[2])
        header=model.extract_header(row[1])
        if len(header)==0:
            header='-'        
        collect.append(row[0])
        collect.append(ratio)
        collect.append(header[0][0])
        L.append(collect)
    josa.write_log(constants.LOG_PATH, 'get_collect', L)
    return L
        
        

if __name__ == "__main__":
    date='20201224'
    