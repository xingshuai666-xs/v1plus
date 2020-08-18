from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from lxml import etree
import random
import redis

a = []

# 基于浏览器的驱动程序实例化一个浏览器对象
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
bro = webdriver.Chrome(executable_path='..\异步爬虫\chrome\chromedriver.exe',chrome_options=chrome_options)
bro.get('https://www.jd.com')


#时间
def time(x):
    if x == 0:
        return sleep(random.randint(1, 3))
    else:
        return sleep(x)


# 数据库存储
def redis_sql(title, rate):
    # 连接数据库
    re1 = redis.ConnectionPool(host='localhost', port=6379, password=111111, decode_responses=True)
    # 设置对象
    r1 = redis.Redis(connection_pool=re1)
    # 添加数值
    r1.hset(query_puts, title, rate)



# 首页操作
def auto():
    global query_num
    global query_puts
    query_puts = input('请输出查询数据>>>')
    query_num = int(input('请输入查询页码>>>'))

    ##定位到搜索对象并录入数据
    search_text = bro.find_element_by_xpath('//*[@id="key"]')
    search_text.send_keys(query_puts)

    ##找到搜索按钮对象并双击搜索按钮
    btn = bro.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
    btn.click()

    deta()


# 商品页爬取
def deta():
    bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time(3)
    text = bro.page_source
    tree = etree.HTML(text)

    # 获取商品数据
    number = int(tree.xpath('//*[@id="J_topPage"]/span/b/text()')[0])
    if number <= query_num:
        title = tree.xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/em/text()[1]')
        rate = tree.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i/text()')
        for i in range(len(title)):
            redis_sql(title[i], rate[i])
        print(number, '页完成')


        # 点击下一页
        Next_page = bro.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]')
        Next_page.click()

        deta()
    else:
        return '完'


auto()
bro.quit()

