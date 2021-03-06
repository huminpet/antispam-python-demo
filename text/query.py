#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""易盾文本离线检测结果获取接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python2.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python text_check_callback_demo.py
"""
__author__ = 'yidun-dev'
__date__ = '2016/3/10'
__version__ = '0.1-dev'

import hashlib
import time
import random
import urllib
import urllib2
import json

class TextQueryByTaskIdsDemo(object):
    """文本离线查询结果获取接口示例代码"""
    API_URL = "https://as.dun.163yun.com/v1/text/query/task"
    VERSION = "v3"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k)+ str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff).hexdigest()

    def query(self,params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random()*100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urllib.urlencode(params)
            request = urllib2.Request(self.API_URL, params)
            content = urllib2.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception, ex:
            print "调用API接口失败:", str(ex)

if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id" # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key" # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id" # 业务ID，易盾根据产品业务特点分配
    text_query_api = TextQueryByTaskIdsDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    
    taskIds = ['f874be29bb5743ebbeb74799b1933061', '76253c3ce34043e099419be9903eca1b'] #查询参数 taskids
    params = {
        "taskIds": taskIds
    }
    ret = text_query_api.query(params)
    if ret["code"] == 200:
        for result in ret["result"]:
            action = result["action"]
            taskId = result["taskId"]
            status = result["status"]
            callback=result["callback"]
            labelArray=json.dumps(result["labels"],ensure_ascii=False)
            if action==0:
                print "taskId=%s，status=%s，callback=%s，文本查询结果：通过" %(taskId,status,callback)
            elif action==2:
                print "taskId=%s，status=%s，callback=%s，文本查询结果：不通过，分类信息如下：%s" %(taskId,status,callback,labelArray)
    else:
        print "ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"])
