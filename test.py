from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import requests

from exceptions.http_api_error import HttpApiIncorrectStatusCodeError, HttpApiIncorrectDataError, BaseHttpApiError


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


def ahuBackEndApiMonitor():
    """ 安大通后端接口监控 """

    # 后端域名
    backEndDomain = "https://ahuer.cn/"
    # 测试接口地址
    helloApiUrl = "api/"

    try:
        url = backEndDomain+helloApiUrl
        httpGetApiTest200StatusCode(url)
        print(f"接口测试通过, url=[{url}], [{datetime.now()}]")
    except BaseHttpApiError as error:
        print(f"接口测试出现异常, message={error.message}, [{datetime.now()}]")


if __name__ == '__main__':

    scheduler = BlockingScheduler()

    try:
        scheduler.add_job(ahuBackEndApiMonitor, 'interval', seconds=3)
        scheduler.start()
        print("***** 定时调度任务启动 ***** ")
    except (SystemExit, KeyboardInterrupt):
        print("application已被强制结束")
