#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : github@Michael-C-H https://github.com/Michael-C-H/ql
# @Time : 2023/11/22 13:23
# -------------------------------
# cron "30 8 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('meFrp签到帐号版')

import requests,re

import sys
import os

# export mefrp='邮箱&密码'      多号|号隔开

def main():
    r = 1
    oy = ql_env()
    print("共找到" + str(len(oy)) + "个账号")
    for i in oy:
        print("------------正在执行第" + str(r) + "个账号----------------")
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        sign_in(email, passwd)
        r += 1
def sign_in(email, passwd):
    try:
        body = {"username" : email,"password" : passwd,}
        headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        login_response = requests.post('https://api.mefrp.com/api/v4/public/verify/login', data=body, headers=headers)
        
        if login_response.status_code == 200:
            access_token = login_response.json()['data']['access_token']
            headers['Authorization'] = 'Bearer ' + access_token
            sign_response = requests.post('https://api.mefrp.com/api/v4/auth/user/sign', headers=headers)
            print(sign_response.json()['message'])
        else:
            print(login_response)
            
    except:
        print('请检查帐号配置是否错误')
def ql_env():
    if "mefrp" in os.environ:
        token_list = os.environ['mefrp'].split('|')
        if len(token_list) > 0:
            return token_list
        else:
            print("mefrp变量未启用")
            sys.exit(1)
    else:
        print("未添加mefrp变量")
        sys.exit(0)

if __name__ == '__main__':
    main()
