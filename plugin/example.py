'''
扩展示例，通过引用pluginmanger，将对应的命令和处理函数提供给主进程
'''
import pluginmanger
import time

'''
发送私信，以time开头，返回当前时间
'''
def showtime(irc_sock, nick, message):
    irc_sock.sendall(("PRIVMSG " + nick + " :" + time.ctime() + "\r\n").encode())

'''
把命令提供给主进程调用
'''
pluginmanger.cmds += [('time', showtime)]     #声明需要识别的字符串及对应命令