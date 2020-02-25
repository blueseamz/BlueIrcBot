import xmlrpc.client
import pluginmanger

rpcurl = 'http://192.168.31.103:6800/rpc'

def ircariagetfun(irc_sock, nick, message):
    msgstr = message.split()[1]
    s = xmlrpc.client.ServerProxy(rpcurl)
    idstr = s.aria2.addUri([msgstr])
    irc_sock.sendall(("PRIVMSG " + nick + " :Add ok. id--%s\r\n"%idstr).encode())

pluginmanger.cmds += [('ariaget', ircariagetfun)]     


def ircariastatefun(irc_sock, nick, message):
    s = xmlrpc.client.ServerProxy(rpcurl)
    irc_sock.sendall(("PRIVMSG " + nick + " :Downloading:\r\n").encode())
    ff = s.aria2.tellActive()
    for a in ff:
        if('info' in a['bittorrent']):
            irc_sock.sendall(("PRIVMSG " + nick + " :Name:%s----Speed:%s\r\n"%(a['bittorrent']['info']['name'],a['downloadSpeed'])).encode())   

pluginmanger.cmds += [('ariastate', ircariastatefun)]     




if __name__ == "__main__":
    s = xmlrpc.client.ServerProxy('http://192.168.31.103:6800/rpc')

    t = s.aria2.getGlobalOption()

    s.aria2.addUri(['magnet:?xt=urn:btih:34E645BD66AC90B039E1B9D06814145D87FE7858'])

    s.aria2.tellActive()

    s.aria2.getGlobalStat()

    s.aria2.tellStopped(0,10)


