from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime, time

import requests
import time

from exceptions.http_api_error import HttpApiIncorrectStatusCodeError, HttpApiIncorrectDataError, BaseHttpApiError
import notify
import threading


def httpApiTestTemplate(url: str, method: str, headers: dict = None,
                        expectedStatusCode: int = 200, expectedResponseData: str = None,
                        postData: dict = None) -> int:
    """
    Http接口测试模板
    @param url: http api接口链接地址
    @param method: 测试方法，支持[GET, POST]
    @param headers: 请求头
    @param expectedStatusCode: 预期的HTTP状态码。默认为200
    @param expectedResponseData: 预期的返回值。默认为空
    @param postData: 使用POST方法时，提交的数据。默认为空
    @return: 测试通过，返回0；不通过，抛出异常
    """

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=postData)
    else:
        raise Exception("method方法选择错误")

    if response.status_code != expectedStatusCode:
        raise HttpApiIncorrectStatusCodeError(expectedStatusCode, url)

    realData = response.text
    if expectedResponseData is not None and realData != expectedResponseData:
        raise HttpApiIncorrectDataError(url, expectedResponseData, realData)

    return 0


def httpGetApiTest200StatusCode(url: str):
    """
    使用http get方法测试api是否返回200状态码
    @param url: 地址
    @return: 测试通过，返回0；不通过，抛出异常
    """

    httpApiTestTemplate(url, method='GET')


def ahuBackEndApiTest() -> int:
    """ 安大通后端接口测试 """
    
    urls = ["http://1.15.150.206:5000/", "https://ahuer.cn/api"]
    
    for url in urls:

        try:
            httpGetApiTest200StatusCode(url)
            print(f"接口测试通过, url=[{url}], [{datetime.now()}]")
        except BaseHttpApiError as error:
            msg = error.message
            print(f"接口测试出现异常, message={msg}, [{datetime.now()}]")
            notify.sendMonitorEmail(msg)
            return -1
    return 0


def ahuBackEndApiMonitor():

    # 间隔时间的基数初始值
    timeSplitRadixInit = 2
    # 间隔时间的基数
    timeSplitRadix = timeSplitRadixInit

    while True:

        apiTestRes = ahuBackEndApiTest()
        # 如果测试结果是不通过
        if apiTestRes != 0:
            # 间隔时间的基数加1
            timeSplitRadix += 1
        else:
            # 否则重置
            timeSplitRadix = timeSplitRadixInit
        # 暂停4的基数次方秒再测试
        time.sleep(4**timeSplitRadix)


if __name__ == '__main__':

    scheduler = BlockingScheduler()

    try:
        scheduler.add_job(ahuBackEndApiMonitor(), 'date')
        print("***** 定时调度任务启动 ***** ")
        scheduler.start()
    except (SystemExit, KeyboardInterrupt):
        print("application已被强制结束")
