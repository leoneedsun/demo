from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400  # （错误请求） 服务器不理解请求的语法
    unauth = 401  # （未授权） 请求要求身份验证。 对于需要登录的网页，服务器可能返回此响应
    methoderror = 405  # （方法禁用） 禁用请求中指定的方法
    servererror = 500  # （服务器内部错误） 服务器遇到错误，无法完成请求


# {'code':400, 'message':'', 'data':{}, 'token'}
def result(code=HttpCode.ok, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}

    # 如果有参数kwargs,且为字典，且有值（keys），则添加至json_dict
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def ok():
    return result()


def params_error(message='', data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message='', data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message='', data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message='', data=None):
    return result(code=HttpCode.servererror, message=message, data=data)
