# ----------------------------------------------------------------------------------------------
# Headers Referers for DOS - HTTP Unbearable Load King
#
# author :  David Rengifo , version 1.0
# ----------------------------------------------------------------------------------------------

# global params
headers_referers = []


# Generate a referers array (include http and https protocols)
# Top search engines: Google, Yahoo, Bing
# Alternatives search engines: Duck Duck Go, Yandex, Usa Today
def get_referer_list():
    global headers_referers
    headers_referers.append('http://www.google.com/?q=')
    headers_referers.append('http://www.usatoday.com/search/results?q=')
    headers_referers.append('http://search.aol.com/aol/search?q=')
    headers_referers.append('http://www.bing.com/search?q=')
    headers_referers.append('http://search.yahoo.com/search?p=')
    headers_referers.append('http://duckduckgo.com/?q=')
    headers_referers.append('http://yandex.com/search/?text=')
    headers_referers.append('https://www.google.com/?q=')
    headers_referers.append('https://www.usatoday.com/search/results?q=')
    headers_referers.append('https://search.aol.com/aol/search?q=')
    headers_referers.append('https://www.bing.com/search?q=')
    headers_referers.append('https://search.yahoo.com/search?p=')
    headers_referers.append('https://duckduckgo.com/?q=')
    headers_referers.append('https://yandex.com/search/?text=')
    return headers_referers
