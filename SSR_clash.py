#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import base64
import codecs


def getBasefile(url):  # 获取订阅链接加密文本
    try:
        html = requests.get(url)
        html.raise_for_status
        html.encoding = html.apparent_encoding
        return str(html.text)
    except:
        return "错误"


def getAllLinks(url):  # 从加密文本解析出所有ssr链接
    links = getBasefile(url)
    result = decodeInfo(links)
    alllinks = result.split('\\n')
    if len(alllinks[-1]) < 10:
        alllinks.pop()
    return alllinks


def getAllNodes(url):  # 从ssr链接汇总得到所有节点信息
    allnodes = []
    links = getAllLinks(url)
    for ss in links:
        link = ss.split('//')[1].split("'")[0]
        # node = getNode(link) if ss.split(':')[0] == "ss" else getNodeR(link)
        if ss.split(':')[0] == "ss":
            print('ss')
            node = getNode(link)
            allnodes.append(node)
        else:
            print('ssr')
            node = getNodeR(link)
            allnodes.append(node)
    return allnodes




def getNode(link):  # 从ss链接中得到节点信息
    info = decodeInfo(link)
    method = info.split(':')[0]
    pwd = info.split("@")[0].split(":")[1]
    server = info.split("@")[1].split(":")[0]
    port = info.split(':')[2]
    remark = server
    node = [remark, server, port, method, pwd]
    return node


def getNodeR(link):  # 从ssr链接中得到节点信息
    info = decodeInfo(link)
    #print (info)
    pwd = decodeInfo(info.split('/')[0].split(':')[-1]).split("'")[1]
    server = info.split(':')[0].split("'")[1]
    port = info.split(':')[1]
    protocol = info.split(':')[2]
    method = info.split(':')[3]
    obfs = info.split(':')[4]
    remark = getName(info.split('&')[2].split('=')[1])
    obfsparam = getName(info.split('&')[0].split('=')[-1])
    proparam = getName(info.split('&')[1].split('=')[1])
    node = [remark, server, port, method, pwd, protocol, obfs, proparam,obfsparam]
    print (node[0])
    return node


def getName(info):  # 得到节点名称（有待合并）
    lens = len(info)
    # lenx = lens - (lens % 4 if lens % 4 else 4)
    if lens % 4 == 1:
        info = info + "==="
    elif lens % 4 == 2:
        info = info + "=="
    elif lens % 4 == 3:
        info = info + "="
    result = base64.urlsafe_b64decode(info).decode('utf-8', errors='ignore')
    return result




def decodeInfo(info):  # 解码加密内容
    lens = len(info)
    if lens % 4 == 1:
        info = info + "==="
    elif lens % 4 == 2:
        info = info + "=="
    elif lens % 4 == 3:
        info = info + "="
    result = str(base64.urlsafe_b64decode(info))
    return result


def setNodes(nodes):  # 设置SSR节点
    proxies = []
    for node in nodes:
        name = node[0]
        server = node[1]
        port = node[2]
        cipher = node[3]
        pwd = node[4]
        protocol = node[5]
        obfs = node[6]
        proparam = node[7]
        obparam = node[8]
        proxy = "- { name: " +"\"" +str(name).strip() +"\""+ ", type: ssr, server: " +"\""+ str(server)+"\"" + ", port: " +"\""+ str(port)+"\"" +", password: " +"\""+ str(pwd)+"\""+ ", cipher: " +"\""+ str(cipher)+"\""+", protocol: "+"\""+ str(protocol)+"\""+", protocolparam: " +"\""+ str(proparam)+"\""+", obfs: "+"\"" + str(obfs)+"\""+", obfsparam: " +"\""+ str(obparam)+"\""+" }\n"
        proxies.append(proxy)
    proxies.insert(0, '\nProxy:\n')
    return proxies


def setPG(nodes):  # 设置策略组 auto,Fallback-auto,Proxy
     
    ##自定义
    proxy_namesHK = []
    proxy_namesUSA = []
    proxy_namesSHen = []
    proxy_namesHu = []
    proxy_namesHang = []
    proxy_namesJing = []
    proxy_names = []
    for node in nodes: 
        if  '香港 'in str(node[0]):
            proxy_namesHK.append(node[0])
        elif '美国 ' in str(node[0]) or '狮城 ' in str(node[0]):
            proxy_namesUSA.append(node[0])
        elif '深'in str(node[0]):
            proxy_namesSHen.append(node[0])
        elif '沪'in str(node[0]):
            proxy_namesHu.append(node[0])
        elif '杭'in str(node[0]):
            proxy_namesHang.append(node[0])
        elif '京'in str(node[0]):
            proxy_namesJing.append(node[0])
        else:
            proxy_names.append(node[0])
      ##自定义

    #auto = "- { name: \'auto\', type: url-test, proxies: " + str( proxy_names) + ", url: 'http://www.gstatic.com/generate_204', interval: 300 }\n"
    #Fallback = "- { name: 'Fallback-auto', type: fallback, proxies: " + str(proxy_names) + ", url: 'http://www.gstatic.com/generate_204', interval: 300 }\n"

    
    
    
    ##自定义
    HK = "- { name: '香港直连', type: select, proxies: " + str(proxy_namesHK) + " }\n"
    USA = "- { name: '美国直连', type: select, proxies: " + str(proxy_namesUSA) + " }\n"
    Shen = "- { name: '深圳中转', type: select, proxies: " + str(proxy_namesSHen) + " }\n"
    Shang = "- { name: '上海中转', type: select, proxies: " + str(proxy_namesHu) + " }\n"
    Hang = "- { name: '杭州中转', type: select, proxies: " + str(proxy_namesHang) + " }\n"
    BeiJing = "- { name: '北京中转', type: select, proxies: " + str(proxy_namesJing) + " }\n"
    Others = "- { name: '其他', type: select, proxies: " + str(proxy_names) + " }\n"       
    Proxy = "- { name: 'PROXY', type: select, proxies: " + " [\"香港直连\",\"美国直连\",\"深圳中转\",\"上海中转\",\"杭州中转\",\"北京中转\",\"其他\",\"DIRECT\"] }" + "\n"
    ##自定义
    
    
    Apple = "- { name: 'Apple', type: select, proxies: "+" [\"PROXY\",\"DIRECT\"] }" +"\n"
    GlobalMedia = "- { name: 'ForeignMedia', type: select, proxies: "+" [\"PROXY\"] }" +"\n"
    MainlandMedia = "- { name: 'DomesticMedia', type: select, proxies: "+" [\"DIRECT\"] }" +"\n"
    RejectWeb =  "- { name: 'Hijacking', type: select, proxies: "+" [\"REJECT\",\"DIRECT\"] }" +"\n"+"\n"+"\n"+"\n"+"\n"
    Rule = "#规则"+"\n"+"Rule:"+"\n"
    ProxyGroup = ['\nProxy Group:\n',HK,USA,Shen,Shang,Hang,BeiJing,Others,Proxy,Apple,GlobalMedia,MainlandMedia,RejectWeb,Rule]
    return ProxyGroup


def getClash(nodes):  #写文件

    rules = getBasefile(
        'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/Pro.yaml')
    gener = rules.split('# 代理节点')[0]
    with codecs.open("./clash.yaml", "w",encoding = 'utf-8') as f:
        f.writelines(gener)

    info = setNodes(nodes) + setPG(nodes)
    with codecs.open("./clash.yaml", "a",encoding = 'utf-8') as f:
        f.writelines(info)

    rule = rules.split('Rule:\n')[1].split('- MATCH,Final')[0]
    with codecs.open("./clash.yaml", "a",encoding = 'utf-8') as f:
        f.writelines(rule)
        f.writelines('- MATCH,PROXY')


if __name__ == "__main__":
    url = ""         #替换订阅，在自定义下替换自己机场的节点标识
    nodes = getAllNodes(url)
    getClash(nodes)
