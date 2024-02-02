#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .decoder import decode_url_to_configs
from .utils import config
import random
from fastapi import APIRouter,BackgroundTasks

router = APIRouter()
@router.get('/')
def getNode()->str:

    subscribeUrl = config["subscribeUrl"]
    NodeList = dump_configs(subscribeUrl)
    NodeStr = RandomNode(NodeList)
    return NodeStr

def RandomNode(NodeList:list)->str:
    #è¿åä¸ä¸ªèç¹ä¿¡æ¯
    return random.choice(NodeList)


def dump_configs(url:str)->list:
    #è¿åå¨é¨èç¹ä¿¡æ¯çåè¡¨
    configs = decode_url_to_configs(url)
    return configs




