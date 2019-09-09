#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from .forms import CommentForm
# Create your views here.

class CommentView(TemplateView):
    http_method_names = ["post"]
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid:
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }

        return self.render_to_response(context)


class VerifyCaptcha(View):
    # 生成验证码
    def get(self, request):
        captcha_id = CaptchaStore.generate_key()
        return JsonResponse({
            'captcha_id':captcha_id,
            'image_src':captcha_image_url(captcha_id),
        })

    #校验验证码
    def post(self,request):
        captcha_id = request.POST.get('captcha_id')
        captcha = request.POST.get('captcha', "")
        captcha = captcha.lower()

        try:
            CaptchaStore.objects.get(respnose=captcha,hashkey=captcha_id,expiration__gt=timezone.now().delete())
        except CaptchaStore.DoesNotExist:
            return JsonResponse({'msg':'验证码错误'}, status=400)
        return JsonResponse({})
