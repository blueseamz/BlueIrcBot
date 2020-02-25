
import socket
import time
import sys
import xmlrpc.client
import pluginmanger as pm

 

irc_host = "irc.freenode.net"
irc_port = 6667
irc_chan = "#yourchan"

bot_name = "bluebot"
usr_name = "bluebot"
ral_name = "bluebot"

ctrlusr = ['yourname1', 'yourname2']    #允许执行命令的用户

print(pm.cmds)

def connectServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(150)    #设置超时，防止网络断掉后死等
    while True:
        try:
            if(sock.connect_ex((irc_host, irc_port)) != 0):
                print("conect error!!!!")
                time.sleep(60)  #网络不通，等待后再试
            else:
                sock.sendall(("NICK " + bot_name + "\r\n").encode())
                sock.sendall(("USER " + bot_name + " " + bot_name + " " + usr_name + " :" + ral_name + "\r\n").encode())
                sock.sendall(("JOIN " + irc_chan + "\r\n").encode())
                sock.sendall(("PRIVMSG " + irc_chan + " :Hello.\r\n").encode())
                break
        except:
            print(sys.exc_info())
    return sock

irc_sock = connectServer()

while True:
    try:
        databyte = irc_sock.recv(4096)
        data = databyte.decode()
        if len(data) == 0:      #检测服务器关闭
            print('socket error -------',time.ctime())
            raise ConnectionResetError
        if(data.startswith("PING")):
            print(data,'-------',time.ctime())
            irc_sock.sendall(data.replace("PING", "PONG").encode())
        elif('PRIVMSG' in data):
            print(data)
            nick = data.split('!')[0].replace(':','')
            message = ':'.join(data.split(':')[2:])
            destination = data.split()[2]
            print(nick,'--',destination,'--',message)
            if(nick in ctrlusr and destination == bot_name):    #只响应特定用户的私信
                for cmd in pm.cmds:
                    if(message.startswith(cmd[0])):
                        cmd[1](irc_sock, nick, message)
        else:
            print("ELSE------",data)
    except KeyboardInterrupt:
        exit()  #ctrl+c中断退出
    except:
        irc_sock = connectServer()
    


