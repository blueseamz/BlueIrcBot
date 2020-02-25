
import requests
import urllib
import base64
import os
import pluginmanger

def ttsbaidu(ttstext='百度语音合成', filename='tts.mp3'):
    #https://fanyi.baidu.com/#en/zh/synthesis
    r = requests.get('https://fanyi.baidu.com/gettts?lan=zh&text=%s&spd=5&source=web'%urllib.request.quote(ttstext))
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=512):
            fd.write(chunk)


def ttsaicloud(ttstext='灵云语音合成', voicetype = 0, filename='tts.mp3'):
    #https://www.aicloud.com/dev/ability/index.html?key=tts#ability-experience
    if voicetype < 0 or voicetype > 3:
        voicetype = 0
    voice =  [
        'tts.cloud.wangjing.v9',    #女声
        'tts.cloud.shenxu',         #男声
        'tts.cloud.liangjiahe',     #童声
        'tts.cloud.cartoonjing'     #卡通
    ]
    headdata = {
        'Host' : 'www.aicloud.com',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With' : 'XMLHttpRequest',
        'Origin' : 'https://www.aicloud.com',
        'Referer' : 'https://www.aicloud.com/dev/ability/index.html?key=tts'
    }
    postdata = {
        "content": ttstext,
        "capkey": voice[voicetype],
        "volume": "5",
        "speed": "5"
    }
    r = requests.post('https://www.aicloud.com/dev/Ability/tts', headers = headdata, data = postdata)
    rjson = r.json()
    if 'url' in rjson:
        rawstr = rjson['url'][rjson['url'].find(',')+1 :]
        with open(filename, 'wb') as fd:
            fd.write(base64.b64decode(rawstr))


def ttssay(msg = ' 语音合成', enginetype = 0, voicetype = 0):
    if enginetype == 0: #灵云
        ttsaicloud(msg,voicetype)
    elif enginetype == 1: #百度
        ttsbaidu(msg)
    if os.path.exists('tts.mp3'):
        os.system('play -q tts.mp3')


def ircsayfun(irc_sock, nick, message):
    msgstr = message.split()[1]
    ttssay(msgstr, 0, 2)

pluginmanger.cmds += [('say', ircsayfun)]     
    

if __name__ == "__main__":
    # ttsbaidu()
    # ttsaicloud('欢迎体验灵云语音合成技术，测试一下')
    ttssay('欢迎体验灵云语音合成技术', 0, 2)
