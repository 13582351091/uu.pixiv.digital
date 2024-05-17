#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
from base64 import b64decode
from typing import Dict, Iterator, List, Union
from .resource import Resource
from dataclasses import dataclass
from urllib import parse


class BaseDecoder:
    def __init__(self, encode_str: str, nameinfo: str = ""):
        self.encode_str = encode_str
        self.decode_str: str
        self.nameinfo = nameinfo

    @staticmethod
    def _bytesto_str(iobytes: bytes) -> str:
        return iobytes.decode('utf-8')


    def decode(self) -> None:
        self.decode_str = self._bytesto_str(b64decode(self.encode_str))


@dataclass
class EncodedCfg:
    encoded_config_str: str
    nameinfo: str = ""


class ListDecoder(BaseDecoder):
    def iter_encode_config(self) -> Iterator[EncodedCfg]:
        for config_str in self.decode_str.splitlines():
            _config_str = re.sub(r"(vmess|ss)://", "", config_str)
            nameinfo = ""
            if "#" in _config_str:
                _config_str, nameinfo = _config_str.split("#", 1)
                nameinfo = parse.unquote(nameinfo)

            _encoded_config_str = _config_str + (
                (4 - len(_config_str) % 4) * "="
            )

            if "best" or "com" in _encoded_config_str and '25' not in nameinfo: 
                if "allowInsecure" in _encoded_config_str:
                     yield _encoded_config_str.replace('allowInsecure=0', 'allowInsecure=1')+"#"+"随机节点"
                else:
                     yield _encoded_config_str.replace('type=tcp====', '')+"&allowInsecure=1"+"#"+"随机节点"

            if "trojan" in config_str :
                if "allowInsecure" in config_str:
                     yield _encoded_config_str.replace('allowInsecure=0', 'allowInsecure=1')+"#"+"随机节点"
                else:
                    yield _encoded_config_str.replace('type=tcp====', '')+"&allowInsecure=1"+"#"+"随机节点"

            if ("vmess" in config_str):
                yield config_str.replace('allowInsecure=0', 'allowInsecure=1')




class ConfigDecoder(BaseDecoder):
    def get_json(self) -> Dict:
        if re.match(r"^{.*}$", self.decode_str):
            return json.loads(self.decode_str)
        return self._parse_ss()

    def _parse_ss(self):
        crypt, pw_at_addr, port = self.decode_str.split(":")
        pw, addr = pw_at_addr.split("@")
        return {
            "ps": self.nameinfo,
            "add": addr,
            "port": int(port),
            "method": crypt,
            "password": pw,
            "ss": True,
            "level": 0,
        }


def _get_resource_from_url(url: str) -> str:
    resource = Resource(url)
    return resource.get_encoded_data()


def _get_listencoded_cfg_from_encoded_str(encoded_str: str) -> List[EncodedCfg]:
    decoder = ListDecoder(encoded_str)
    decoder.decode()
    return [item for item in decoder.iter_encode_config()]





def decode_url_to_configs(url: str)->list:
    encoded_str = _get_resource_from_url(url)
    ##https://github.com/CareyWang/sub-web 成功用这个订阅解析解决了订阅被cf格挡问题，且可用于sspanel
    lst_encoded_cfg = _get_listencoded_cfg_from_encoded_str(encoded_str)#lst_encoded_cfg解析为节点后的列表,包含所有节点链接
    return lst_encoded_cfg




