from . import header
from . import disclosure
from . import reports


def run(code):

    dis=disclosure.get_dis(code)
    gayo = header.get_header(code)
    report=reports.get_report(code)
    # print('------------------------------------')
    content = gayo+''.join(dis)+''.join(report)
    # print(content)

    return content






if __name__=='__main__':

    cont=run('036170')

    cont=run('005930')

    print(cont)