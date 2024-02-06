#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
from fastapi import APIRouter,BackgroundTasks
fileName = "subscribeLink.txt"

def is_subscription_link_valid(subscribeUrl:str)->bool:
    result = requests.get(subscribeUrl).text
    if "error" in result:
        return False
    return True

def delete_invalid_url_in_txt(fileName:str)->"void":
    valid_lines= []
    with open(fileName, "r") as file:
        lines = file.readlines()
    for line in lines:
        email = line.strip().split(",")[0]
        subscription_url = line.strip().split(",")[1]
        if is_subscription_link_valid(subscription_url):
            valid_lines.append(line)
        else:
            print(email+"订阅已经不可用")
    # 将有效行重新写回文件
    with open(fileName, "w") as file:
        file.writelines(valid_lines)

def subscription_link_list(fileName:str)->list:
    SubscribeUrlList = []
    with open(fileName, "r") as f:
        lines = f.readlines()
    for line in lines:
        subscription_url = line.strip().split(",")[1]
        SubscribeUrlList.append(subscription_url)
    return SubscribeUrlList


def subscription_link_valid_list(SubscribeUrlList:list)->list:
    valid_link_list = list(filter(lambda f: is_subscription_link_valid(f), SubscribeUrlList))
    ##返回可用订阅链接前对原始文件进行删除不可用链接操作:
    return valid_link_list


def read_random_line(fileName:str) -> str:
    with open(fileName, "r") as file:
        lines = file.readlines()
    return random.choice(lines)

def randomSubscribeUrl(validSubscribeUrlList:list)->str:
    #返回一个可用的订阅链接信息
    return random.choice(validSubscribeUrlList)

router = APIRouter()

@router.get('/')
def returnRandomSubscribeUrl(background_tasks: BackgroundTasks)->str:
    #返回一个可用的订阅链接信息
    SubscribeUrlList = subscription_link_list(fileName)
    validSubscribeUrlList = subscription_link_valid_list(SubscribeUrlList)
    result = randomSubscribeUrl(validSubscribeUrlList)
    background_tasks.add_task(delete_invalid_url_in_txt, fileName)
    ##事实证明def就行,不用async就可以后台执行，先返回后删除
    # .1: 7996 - "GET /randomSubscribeUrl/ HTTP/1.1"
    # 200
    # OK
    # 971205295 @ qq.com订阅已经不可用
    return result





if __name__ == "__main__":
    print()

    ##思路是随机选取一行订阅检测，如果没问题就返回
    #1订阅有问题，那么
    ##1->对全部订阅扫描，删除不可用的，然后重新随机一个返回,此返回时不用检测
    ##2->如果扫描后没有可用的，那么不做处理让vercel报错

    # 1订阅一个都没有，那么vercel错误提醒(不做处理考虑就行)
