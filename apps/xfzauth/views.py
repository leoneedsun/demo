from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from utils import restful
from django.shortcuts import redirect, reverse
from utils.captcha.xfzcaptcha import Captcha, SmsCaptcha
from io import BytesIO
from django.http import HttpResponse
from utils.CCPSDK import CCPRestSDK
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


# 一般信息反馈格式：
# {"code": 400, "message": "", "data": {}}

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message='您的账号已经被冻结！')
        else:
            return restful.params_error(message='手机号或者密码错误！')
    else:
        errors = form.get_errors()
        # {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.object.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO:相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df:12Df.lower() 即key和value，再设置过期时间
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response


def sms_captcha(request):
    # /smscode?telephone=XXXXXXXXX
    telephone = request.GET.get('telephone')
    code = SmsCaptcha.gene_text()
    accountSid = '8a216da87291bbcd01729da8375206e0'
    authToken = '0d2f68f3082a47c79f1c9db2c8533131'
    appId = '8a216da87291bbcd01729da8386406e6'
    sms_template = 1
    rest = CCPRestSDK.REST(accountSid, authToken, appId)
    result = rest.sendTemplateSMS(telephone, [code], sms_template)
    cache.set(telephone, code, 5 * 60)
    print(result)
    if result['statusCode'] == '000000':
        return restful.ok()
    elif result['statusCode'] == '160044':
        return restful.unauth(message=None)
    else:
        return restful.params_error(message='验证码发送失败！')
    # print('验证码：', code)
    # return restful.ok()


def cache_test(request):
    cache.set('username', 'alllight', 60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')
