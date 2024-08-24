#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
from fastapi import APIRouter, BackgroundTasks

fileName = "subscribeLink.txt"
# 添加headers模拟浏览器访问（针对juzi等特殊订阅）
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}


def is_subscription_link_valid(subscribeUrl: str) -> bool:
    result = requests.get(subscribeUrl, headers=headers).text
    if "error" in result:
        return False
    return True


def delete_invalid_url_in_txt(fileName: str) -> "void":
    valid_lines = []
    with open(fileName, "r") as file:
        lines = file.readlines()
    for line in lines:
        email = line.strip().split(",")[0]
        subscription_url = line.strip().split(",")[1]
        if is_subscription_link_valid(subscription_url):
            valid_lines.append(line)
        else:
            print(email + "订阅已经不可用")
    # 将有效行重新写回文件
    with open(fileName, "w") as file:
        file.writelines(valid_lines)


def subscription_link_list(fileName: str) -> list:
    SubscribeUrlList = []
    with open(fileName, "r") as f:
        lines = f.readlines()
    for line in lines:
        subscription_url = line.strip().split(",")[1]
        SubscribeUrlList.append(subscription_url)
    return SubscribeUrlList


def subscription_link_valid_list(SubscribeUrlList: list) -> list:
    valid_link_list = list(filter(lambda f: is_subscription_link_valid(f), SubscribeUrlList))
    ##返回可用订阅链接前对原始文件进行删除不可用链接操作:
    return valid_link_list


def read_random_line(fileName: str) -> str:
    with open(fileName, "r") as file:
        lines = file.readlines()
    return random.choice(lines)


def randomSubscribeUrl(validSubscribeUrlList: list) -> str:
    # 返回一个可用的订阅链接信息
    return random.choice(validSubscribeUrlList)


def hf_test():
    from urllib.request import getproxies
    print(getproxies())

    result = requests.get('https://s.juzicloud.vip/link/3Dv3anqm7fBcTxcT?sub=3', headers=headers)

    print("hf test订阅请求结果：")
    print(result.content)
    return 'hf test'


router = APIRouter()


@router.get('/')
def returnRandomSubscribeUrl(background_tasks: BackgroundTasks) -> str:
    # 返回一个可用的订阅链接信息
    SubscribeUrlList = subscription_link_list(fileName)
    validSubscribeUrlList = subscription_link_valid_list(SubscribeUrlList)
    result = randomSubscribeUrl(validSubscribeUrlList)
    background_tasks.add_task(delete_invalid_url_in_txt, fileName)
    return result

    # return hf_test()


if __name__ == "__main__":
    print()

    ##思路是随机选取一行订阅检测，如果没问题就返回
    # 1订阅有问题，那么
    ##1->对全部订阅扫描，删除不可用的，然后重新随机一个返回,此返回时不用检测
    ##2->如果扫描后没有可用的，那么不做处理让vercel报错

    # 1订阅一个都没有，那么vercel错误提醒(不做处理考虑就行)
