#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from .decoder import decode_url_to_configs
from .utils import config
import random
from fastapi import APIRouter,BackgroundTasks

router = APIRouter()
@router.get('/')
def getNode()->str:
    getNodeBaseUrl = config["getNodeBaseUrl"]
    randomSubscribeUrl = requests.get(getNodeBaseUrl)
    NodeList = dump_configs(randomSubscribeUrl)
    NodeStr = RandomNode(NodeList)
    return NodeStr

def RandomNode(NodeList:list)->str:
    #返回一个节点信息
    return random.choice(NodeList)


def dump_configs(url:str)->list:
    #返回全部节点信息的列表
    configs = decode_url_to_configs(url)
    return configs




