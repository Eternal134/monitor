# -*- coding:utf-8 -*-
# author: qiumao
# datetime:2021/9/29 13:29

class BaseHttpApiError(BaseException):

    def __init__(self, url, message):
        # 测试的http接口
        self.url = url
        # 描述信息
        self.message = message


class HttpApiIncorrectDataError(BaseHttpApiError):
    """ HTTP接口返回数据不正确
    """

    def __init__(self, url: str, exceptData: str, realData: str, message: str = ""):
        """
        @param url: HTTP地址
        @param exceptData: 期望的数据
        @param realData: 实际的数据
        @param message: 描述信息
        @return: HttpApiIncorrectDataError
        """
        presetMessage = f"地址 = {url} 返回的数据不正确。\n 期望的数据为: {exceptData} \n 实际的数据为: {realData}"
        _message = message if message != "" else presetMessage
        super().__init__(url, _message)


class HttpApiIncorrectStatusCodeError(BaseHttpApiError):
    """ HTTP接口状态码不正确 """

    def __init__(self, exceptStatusCode: int, url: str, message: str = ""):

        presetMessage = f"地址 = {url} 返回的状态码不是 {exceptStatusCode} ！"
        _message = message if message != "" else presetMessage
        super().__init__(url, _message)


class HttpApiNot200ErrorError(HttpApiIncorrectStatusCodeError):
    """ HTTP接口状态码非200错误码
    """

    def __init__(self, url, message=""):

        super().__init__(200, url, message)
