# -*- coding: utf-8 -*-

import re
import os
import requests
import pluginmanger

# https://m.weibo.cn/detail/4452635194980369
# https://m.weibo.cn/detail/4453120718978560


try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


def requests_with_retry(url,max_retry=0,stream=False):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    retry = 0
    while retry <= max_retry:
        try:
            return requests.request("GET",url,headers=headers,timeout=5,stream=stream,verify=False)
        except:
            retry = retry + 1

def download(url,file_path,overwrite):
    if os.path.exists(file_path) and not overwrite:
        return True
    response = requests_with_retry(url=url,max_retry=0,stream=True)
    if not response:
        return False
    else:
        try:
            with open(file_path,'wb') as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
        except:
            if os.path.exists(file_path): os.remove(file_path)
            return False
        else:
            return True

def getpicurls(urlstr):
    htmlstr = requests_with_retry(urlstr)
    contentstr = htmlstr.content.decode('utf-8')
    recomp = re.compile(r'"size": "large".*?(https.*?jpg)',re.DOTALL)
    return recomp.findall(contentstr)

def downloadpic(url,dirpath):
    file_name = re.sub(r"^\S+/","",url)
    file_name = re.sub(r"\?\S+$","",file_name)
    file_path = os.path.join(dirpath,file_name)
    if not os.path.exists(dirpath): 
        os.makedirs(dirpath)
    download(url, file_path, True)

def ircweibopicfun(irc_sock, nick, message):
    msgstr = message.split()[1]
    urls = getpicurls(msgstr)
    print(len(urls))
    irc_sock.sendall(("PRIVMSG " + nick + " :" + "There are %d pictures."%len(urls) + "\r\n").encode())
    for url in urls:
        irc_sock.sendall(("PRIVMSG " + nick + " :" + "Downloading %s"%url + "\r\n").encode())
        downloadpic(url, 'pic')
    irc_sock.sendall(("PRIVMSG " + nick + " :" + "Download finish." + "\r\n").encode())

pluginmanger.cmds += [('weibo', ircweibopicfun)]

if __name__ == "__main__":
    urls = getpicurls('https://m.weibo.cn/detail/4453120718978560')
    print(len(urls))
    print('\n'.join(urls))
    for url in urls:
        downloadpic(url, 'pic')