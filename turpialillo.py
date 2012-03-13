#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import socket
import random

# Posibles comandos:
# !define <palabra>: devuelve el significado de la palabra
# !status: devuelve el estado de los servicios
# !botella: gira la botella y apunta a un nombre aleatorio
# !regaño [nick]: lanza un regaño aleatorio a nick
# !google
# !wiki

p_join = re.compile('^:(.+)!(.+) JOIN :#turpial')
p_message = re.compile('^:(.+)!(.+) PRIVMSG #turpial :(.*)')

network = 'irc.freenode.net'
port = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))
print irc.recv( 4096 )
irc.send ('NICK turpialillo\r\n' )
irc.send ('USER turpialillo turpialillo turpialillo :Turpial Bot\r\n' )
irc.send ('JOIN #turpial\r\n' )

REJECTS = [
    'Verga %s, eres una ladilla andante',
    '%s, marico te dije y marico te quedaste',
    '¿%s, no tienes algo mejor que hacer? Anda a ver si la puerca puso',
    '%s, ¿qué es de la vida de tu mamá? Yo siempre la recuerdo',
    '¿Alguien por aquí tiene periódico? Es para ver si envolvemos a %s y lo ponemos a que madure',
    '%s, pronto satanas me dará permisos para patear, y te patearé el trasero',
    '%s, a parte de saludar, qué otro truco sabes hacer?',
    '¿%s no te da pena ser así?',
    '¿Qué tanto saludas %s? Te salude al entrar',
]

def custom_rejects(nick):
    reject = REJECTS[random.randint(0, len(REJECTS)-1)] % nick
    return 'PRIVMSG #turpial :' + reject + '\r\n'

def process_command(nick, cmd):
    if cmd == '!hola':
        irc.send(custom_rejects(nick))
    elif cmd == '!ping':
        irc.send('PRIVMSG #turpial :%s, ¿se supone que debo responderte "pong" para que sepas que estoy aquí?\r\n' % nick)

while True:
    data = irc.recv(4096)

    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')

    # Saludos
    rtn = p_join.search(data)
    if rtn:
        nick, _ = rtn.groups()
        if nick == 'satanas':
            irc.send('PRIVMSG #turpial :Saludos satanas, amo y señor del inframundo. Bienvenido a tu reino\r\n')
        #elif nick != 'turpialillo':
        #    irc.send('PRIVMSG #turpial :Saludos ' + nick + '. Bienvenid@ al infierno...\r\n')
        continue

    # Mensajes
    rtn = p_message.search(data)
    if rtn:
        nick, _, msg = rtn.groups()
        # Procesar comandos
        if msg[0] == '!':
            process_command(nick, msg.strip())
        elif nick.lower().find('tr0n') >= 0 and msg.find('turpialillo') >= 0:
            irc.send(custom_rejects(nick))


    print data


