import re

from urllib import request

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    request = request.Request(url, headers=headers)
    page = urllib3.urlopen(request)
    html = page.read()
   # html = request.urlopen(url).read()
    return html
def getImg(html):
    reg = '<src = "(.+?\.jpg)" pic_ext>'
    imgre = re.compile(reg)
    html = str(html)
    imglist = imgre.findall(html)
    x = 0
    for imgurl in imglist:
        print(imgurl)
        urllib.urlretrieve(imgurl,'C:a\\%s.jpg' % x)
        x = x + 1
html = getHtml("http://www.qiushibaike.com/imgrank/")
getImg(html)






