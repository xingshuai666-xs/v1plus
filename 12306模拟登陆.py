import requests
from hashlib import md5
import random

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }

        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def tranformImgCode(imgPath, imgType):
    chaojiying = Chaojiying_Client('nibaba', '111111', '907600')
    im = open(imgPath, 'rb').read()
    return chaojiying.PostPic(im, imgType)['pic_str']

def ccc(distance):
    # 初速度
    v = 0
    # 单位时间为0.3s来统计轨迹，轨迹即0.3s内的位移
    t = 0.3
    # 位移/轨迹列表
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 4 / 5
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间内的位移越小，模拟的轨迹就越多越详细
            a = 2
        else:
            a = -3
        # 初速度
        v0 = v
        # 0.3s时间内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经达到V，该速度作为下次的初速度
        v = v0 + a * t
    return tracks
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains

from time import sleep
from PIL import Image

# https://kyfw.12306.cn/otn/login/init#
##找到驱动打开网站
bro = webdriver.Chrome('chrome\chromedriver.exe')
bro.get('https://kyfw.12306.cn/otn/resources/login.html')


def jt(img_name, img_x):
    bro.save_screenshot('12306.png')
    print('截图ok')
    img_tag = bro.find_element_by_xpath(f'{img_x}')
    location = img_tag.location
    size = img_tag.size
    rengle = (
        int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
    i = Image.open('12306.png')
    frame = i.crop(rengle)
    frame.save(f'{img_name}.png')
    print(f'{img_name}裁剪ok')
    return img_tag


# 登陆界面
sleep(1)
dl = bro.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
sleep(1)
xp = '//*[@id="J-loginImg"]'
bro.find_element_by_xpath('//*[@id="J-userName"]').send_keys('13520111584')
sleep(1)
bro.find_element_by_xpath('//*[@id="J-password"]').send_keys('hbsihbsi1')
sleep(3)
img_tag = jt('yzm', xp)
# 识别
rangle = tranformImgCode('yzm.png', 9004)
print(rangle)
all_list = []
if '|' in rangle:
    list_1 = rangle.split('|')
    count_1 = len(list_1)
    print(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)

else:
    x = int(rangle.split(',')[0])
    y = int(rangle.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
ran = random.randint(1,10)
for i in all_list:
    x = i[0]
    y = i[1]
    ActionChains(bro).move_to_element_with_offset(img_tag, x, y).click().perform()
    sleep(1.5)
bro.find_element_by_xpath('//*[@id="J-login"]').click()
sleep(2)
div_tag = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
track_list = [i for i in ccc(150)]
track_list.insert(0, 150)
print(track_list)
sleep(1)
for track in track_list:
    ActionChains(bro).click_and_hold(div_tag).move_by_offset(track, 0).perform()
print('拖动完成')
sleep(0.5)
ActionChains(bro).release(div_tag).perform()
sleep(5)
#
bro.quit()
