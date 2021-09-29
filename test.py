from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import requests

def httpApiTestTemplate(url, method, expectedStatusCode=200, expectedResponseData=None, postForm=None):
    """ HTTP接口测试模板 """
    

def ahuBackEndApiMonitor():
    """ 安大通后端接口监控 """
    
    # 后端域名
    backEndDomain = "https://ahuer.cn/"
    # 测试接口地址
    helloApiUrl = "api/"
    
    
    print("现在是: ", datetime.now())
    
if __name__ == '__main__':
    
    scheduler = BlockingScheduler()
    
    try:
        scheduler.start()
    except (SystemExit, KeyboardInterrupt):
        print("application已被强制结束")