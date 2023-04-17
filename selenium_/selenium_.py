import json
import random
import re
import time

import requests
from requests.cookies import RequestsCookieJar
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def save(file, data_list):
    file_handle = open(file, mode='a', encoding='utf-8')
    for e in data_list:
        # [] 里面的操作是为了把list中所有的元素变成字符串，方便进行join操作
        s = ','.join([str(x) for x in e]) + '\n'
        file_handle.write(s)
    time_str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    print(time_str + ' Append {0} lines of data to {1}'.format(file, len(data_list)))
    file_handle.flush()
    file_handle.close()


class RuoYiSpider:
    def __init__(self, root_url):
        # 初试化类 传入被爬取网站的入口地址
        self.root_url = root_url

    # 登录网站
    def login(self):
        # 启动chromedriver
        self.chrome = Chrome()
        # 先打开入口地址 方便人工登录
        self.chrome.get(self.root_url)
        time.sleep(10)

    def quit(self):
        self.chrome.quit()

    # 判断是否能查到指定的节点，如果存在返回true,否则返回false
    def ifHas(self, by, xpathStr):
        # noinspection PyBroadException
        try:
            self.chrome.find_element(by, xpathStr)
            return True
        except Exception as ignored:
            pass
        return False

    # 判断是否能查到指定的节点，如果存在返回true,否则返回false
    # noinspection PyBroadException
    @staticmethod
    def ifHasNode(broswer, by, xpathStr):
        try:
            broswer.find_element(by, xpathStr)
            return True
        except Exception as ignored:
            pass
        return False

    # 保存文件，设置编码格式为utf-8

    # 爬取角色菜单数据 数据写入角色文件 role.txt
    def get_role(self):
        menu_url = 'http://127.0.0.1:9999/system/role'
        self.chrome.get(menu_url)

        data_header = []
        reccords = []
        roleId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        roleName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        roleKey = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        roleSort = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        roleStatus = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        createTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        data_header.append([roleId, roleId, roleName, roleKey, roleSort, roleStatus, createTime])
        print(data_header)

        save('role.txt', data_header)

        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr')
        for row in tbody:
            r_roleId = row.find_element(By.XPATH, 'td[2]').text
            r_roleName = row.find_element(By.XPATH, 'td[3]').text
            r_roleKey = row.find_element(By.XPATH, 'td[4]').text
            r_roleSort = row.find_element(By.XPATH, 'td[5]').text
            r_roleStatus = row.find_element(By.XPATH, 'td[6]').text
            r_createTime = row.find_element(By.XPATH, 'td[7]').text

            reccords.append([r_roleId, r_roleId, r_roleName, r_roleKey, r_roleSort, r_roleStatus, r_createTime])

        save('role.txt', reccords)

    # 爬取菜单数据 数据写入角色文件 menu.txt
    def get_menu(self):
        menu_url = 'http://127.0.0.1:9999/system/menu'
        self.chrome.get(menu_url)
        time.sleep(2)

        # 点击【展开】按钮
        self.chrome.find_element(By.ID, 'expandAllBtn').click()

        data_header = []
        reccords = []
        menuName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[2]').text
        orderNum = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[3]').text
        url = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[4]').text
        menuType = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[5]').text
        visible = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[6]').text
        perms = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[7]').text
        data_header.append([menuName, orderNum, url, menuType, visible, perms])
        print(data_header)

        save('menu.txt', data_header)

        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-tree-table"]/tbody/tr')
        for row in tbody:
            r_menuName = row.find_element(By.XPATH, 'td[2]').text
            r_orderNum = row.find_element(By.XPATH, 'td[3]').text
            r_url = row.find_element(By.XPATH, 'td[4]').text
            r_menuType = row.find_element(By.XPATH, 'td[5]').text
            r_visible = row.find_element(By.XPATH, 'td[6]').text
            r_perms = row.find_element(By.XPATH, 'td[7]').text
            reccords.append([r_menuName, r_orderNum, r_url, r_menuType, r_visible, r_perms])
            print([r_menuName, r_orderNum, r_url, r_menuType, r_visible, r_perms])

        save('menu.txt', reccords)

    # 爬取部门数据
    @DeprecationWarning
    def get_dept(self):
        menu_url = 'http://127.0.0.1:9999/system/dept'
        self.chrome.get(menu_url)
        time.sleep(2)

        data_header = []
        reccords = []
        deptName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[2]').text
        orderNum = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[3]').text
        status = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[4]').text
        createTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-tree-table"]/thead/tr/th[5]').text

        data_header.append([deptName, orderNum, status, createTime])
        save('dept.txt', data_header)

        # 查询表格里面的数据
        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-tree-table"]/tbody/tr')
        for row in tbody:
            menuId = row.find_element(By.XPATH, '.').get_attribute("data-id")
            r_deptName = row.find_element(By.XPATH, 'td[2]').text
            r_orderNum = row.find_element(By.XPATH, 'td[3]').text
            r_status = row.find_element(By.XPATH, 'td[4]').text
            r_createTime = row.find_element(By.XPATH, 'td[5]').text

            reccords.append([menuId, r_deptName, r_orderNum, r_status, r_createTime])

        save('dept.txt', reccords)

    # 爬取岗位数据
    @DeprecationWarning
    def get_post(self):
        menu_url = 'http://127.0.0.1:9999/system/post'
        self.chrome.get(menu_url)
        time.sleep(2)

        data_header = []
        records = []
        # 获得表头
        postIt = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        postCode = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        postName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        postSort = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        postStatus = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        createTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        data_header.append([postIt, postCode, postName, postSort, postStatus, createTime, ])
        save('position.txt', data_header)

        # 查询表格里面的数据
        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr')

        # 查询表格数据的总数
        positionInfo = self.chrome.find_element(By.CLASS_NAME, 'pagination-info').text

        # print(positionInfo)
        total = re.findall(r'\d+', positionInfo)
        print('岗位个数个数: ', total[2])
        print(data_header)
        # print('岗位编号:', '岗位编码', '岗位名称', ' 显示顺序', '创建时间')

        for row in tbody:
            # print(i.text)
            postId = row.find_element(By.XPATH, 'td[2]').text
            postCode = row.find_element(By.XPATH, 'td[3]').text
            postName = row.find_element(By.XPATH, 'td[4]').text
            postSort = row.find_element(By.XPATH, 'td[5]').text
            postStatus = row.find_element(By.XPATH, 'td[6]').text
            createTime_ = row.find_element(By.XPATH, 'td[7]').text
            records.append([postId, postCode, postName, postSort, postStatus, createTime_])

        save('position.txt', records)

    # 爬取字典数据
    @DeprecationWarning
    def get_dict(self):
        menu_url = 'http://127.0.0.1:9999/system/dict'
        self.chrome.get(menu_url)
        time.sleep(2)

        data_header = []
        reccords = []
        dictId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        dictName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        dictKey = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        dictStatus = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        remark = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        createTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text

        data_header.append([dictId, dictName, dictKey, dictStatus, remark, createTime])
        save('dict.txt', data_header)
        print(data_header)
        # 查询表格里面的数据
        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr')
        for row in tbody:
            r_dictId = row.find_element(By.XPATH, 'td[2]').text
            r_dictName = row.find_element(By.XPATH, 'td[3]').text
            r_dictKey = row.find_element(By.XPATH, 'td[4]').text
            r_dictStatus = row.find_element(By.XPATH, 'td[5]').text
            r_remark = row.find_element(By.XPATH, 'td[6]').text
            r_createTime = row.find_element(By.XPATH, 'td[7]').text

            reccords.append([r_dictId, r_dictName, r_dictKey, r_dictStatus, r_remark, r_createTime])
        save('dict.txt', reccords)
        print(reccords)

    # 爬取参数设置数据
    def get_config(self):
        menu_url = 'http://127.0.0.1:9999/system/config'
        self.chrome.get(menu_url)
        data_header = []
        reccords = []

        # 获得表头数据
        configId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        configName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        configKey = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        configValue = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        configType = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        remark = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        createTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[8]').text

        data_header.append([configId, configName, configKey, configValue, configType, remark, createTime])  #
        print(data_header)
        # 保存表头数据
        save('config.txt', data_header)

        # 查询表格里面的数据
        tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr')
        for row in tbody:
            r_configId = row.find_element(By.XPATH, 'td[2]').text
            r_configName = row.find_element(By.XPATH, 'td[3]').text
            # 参数键名字段有省略的情况，因此需要判断是否有input元素
            if self.ifHasNode(row, By.XPATH, 'td[4]/input'):
                r_configKey = row.find_element(By.XPATH, 'td[4]/input').get_attribute("value")
            else:
                r_configKey = row.find_element(By.XPATH, 'td[4]').text

            r_configValue = row.find_element(By.XPATH, 'td[5]').text
            r_configType = row.find_element(By.XPATH, 'td[6]').text

            # 备注字段有省略的情况，因此需要判断是否有input元素
            if self.ifHasNode(row, By.XPATH, 'td[7]/input'):
                r_remark = row.find_element(By.XPATH, 'td[7]/input').get_attribute("value")
            else:
                r_remark = row.find_element(By.XPATH, 'td[7]').text
            r_createTime = row.find_element(By.XPATH, 'td[8]').text
            print(r_configKey, r_remark)
            reccords.append(
                [r_configId, r_configName, r_configKey, r_configValue, r_configType, r_remark, r_createTime])

        save('config.txt', reccords)

    def get_opt_log(self):
        menu_url = 'http://127.0.0.1:9999/monitor/operlog'
        self.chrome.get(menu_url)
        data_header = []
        reccords = []
        # 爬取表头
        operId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        title = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        businessType = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        operName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        deptName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        operIp = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        operLocation = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[8]').text
        status = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[9]').text
        operTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[10]').text

        data_header.append([operId, title, businessType, operName, deptName, operIp, operLocation, status, operTime])
        print(data_header)
        save('opt_log.txt', data_header)

        # 把分页数调整为最大

        page = 0
        while True:
            # 如果有分页信息并且已经不是第一页，则开始分页爬取
            if self.ifHas(By.CLASS_NAME, 'pagination-info') and page > 0:
                # 找到记录号偏移数据，判断是否需要分页
                # 显示第 201 到第 250 条记录，总共 16503 条记录
                page_info_text = self.chrome.find_element(By.CLASS_NAME, 'pagination-info').text
                page_info = re.findall(r'\d+', page_info_text)

                print('当前爬取第 {0} 到第 {1} 条记录，总共{2} '.format(page_info[0], page_info[1], page_info[2]))

                # 如果还未到达最后一页
                if int(page_info[1]) < int(page_info[2]):
                    # 点击>进入下一页
                    a = self.chrome.find_element_by_link_text('›')
                    a.click()
                    # 随机休眠，模拟人工操作
                    time.sleep(random.uniform(2.1, 3))
                else:
                    print('====结束翻页爬取操作====')
                    break

            # 如果找不到明细数据则终止爬取操作
            if not self.ifHas(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr'):
                break

            tbody = self.chrome.find_elements(By.XPATH, '//*[@id="bootstrap-table"]/tbody/tr')
            for row in tbody:
                try:
                    r_operId = row.find_element(By.XPATH, 'td[2]').text
                    r_title = row.find_element(By.XPATH, 'td[3]').text
                    r_businessType = row.find_element(By.XPATH, 'td[4]').text
                    r_operName = row.find_element(By.XPATH, 'td[5]').text
                    r_deptName = row.find_element(By.XPATH, 'td[6]').text
                    r_operIp = row.find_element(By.XPATH, 'td[7]').text
                    r_operLocation = row.find_element(By.XPATH, 'td[8]').text
                    r_status = row.find_element(By.XPATH, 'td[9]').text
                    r_operTime = row.find_element(By.XPATH, 'td[10]').text
                    reccords.append(
                        [r_operId, r_title, r_businessType, r_operName, r_deptName, r_operIp, r_operLocation, r_status,
                         r_operTime])
                except StaleElementReferenceException as e:
                    print('发生了异常')
                    print('url:', self.chrome.current_url)
                    print('html:', self.chrome.page_source)
                    print(repr(e))

            page = page + 1
            if len(reccords) > 0:
                save('opt_log.txt', reccords)
                reccords.clear()

        # ========end while
        if len(reccords) > 0:
            save('opt_log.txt', reccords)

    # 把当前浏览器cookie数据持久化到文件
    @staticmethod
    def save_cookie(brower):
        cookies = brower.get_cookies()
        with open("ruoyi_cookie.json", "w") as fp:
            json.dump(cookies, fp)

    # 从本地读取cooke数据
    @staticmethod
    def load_cookie():
        fake_cookie = RequestsCookieJar()
        with open("ruoyi_cookie.json", "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                fake_cookie.set(cookie['name'], cookie['value'])

        return fake_cookie

    # 封装一个请求,用requests发送请求
    def spider_request(self, page_size, page_num, request_url, referer_url, fake_parameter):
        """
            这里封装了一个独立的请求方法，实现以下功能：
            1.从本地加载cookie
            2.组装header参数
            3.组装请求参数
            4.提交请求
            5.得到http response响应之后返回数据用utf-8解码
        """
        # 从本地加载cookie
        fake_cookies = self.load_cookie()
        fake_header = {
            'Referer': referer_url,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        }
        # 保存会话
        session_ = requests.session()
        # 组建新的请求参数、cookie
        response_data = session_.post(request_url, params=fake_parameter, headers=fake_header, cookies=fake_cookies)
        response_data.encoding = 'utf-8'
        # 数据解码
        # response_json = response_data.content.decode("utf-8")
        response_json = response_data.json()
        # with open("test_json.json", "w") as fp:
        #    json.dump(response_json, fp)
        return response_json

    # 使用request组件爬取操作日志数据
    def get_opt_log_by_request(self):
        menu_url = 'http://127.0.0.1:9999/monitor/operlog/list'
        menu_root_url = 'http://127.0.0.1:9999/monitor/operlog'
        # 模拟浏览器发起请求
        self.chrome.get(menu_root_url)
        time.sleep(3)

        # 保存cooke
        self.save_cookie(self.chrome)

        data_header = []
        reccords = []

        # 爬取表头并保存到文件
        operId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        title = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        businessType = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        operName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        deptName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        operIp = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        operLocation = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[8]').text
        status = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[9]').text
        operTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[10]').text
        data_header.append([operId, title, businessType, operName, deptName, operIp, operLocation, status, operTime])
        print(data_header)
        save('opt_log.txt', data_header)

        # 查询分页数据
        if self.ifHas(By.CLASS_NAME, 'pagination-info'):
            # 找到记录号偏移数据，判断是否需要分页
            # 显示第 201 到第 250 条记录，总共 16503 条记录
            page_info_text = self.chrome.find_element(By.CLASS_NAME, 'pagination-info').text
            page_info = re.findall(r'\d+', page_info_text)
            time_str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
            print(time_str + '当前页 {0} ，获取到记录总数:{1} '.format(page_info[0], page_info[2]))
            total = int(page_info[2])
            page_size = 50
            # 计算页数，总页数=(总数+页大小-1)/页大小
            pages = int((total + page_size - 1) / page_size) + 1
            for page_no in range(1, pages):
                time.sleep(random.uniform(1.1, 3.1))
                time_str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
                print(time_str + ' 开始爬取第{0} 页，总页数{1} '.format(page_no, pages))

                fake_parameters = {
                    'pageSize': page_size,  # 每一页的行数
                    'pageNum': page_no,  # 当前页码
                    'orderByColumn': 'operTime',
                    'isAsc': 'desc',
                    'title': '',
                    'operName': '',
                    'status': 0,
                    'businessTypes': ''
                }
                json_result = self.spider_request(page_size, page_no, menu_url, menu_root_url, fake_parameters)
                # 最后一页里面rows=null ,因此需要判断是否为空，是空时返回
                rows = json_result.get('rows')
                if not rows:
                    break

                for row in rows:
                    record = [row['operId'], row['title'], row['businessType'],
                              row['operName'], row['deptName'], row['operIp'],
                              row['operLocation'], row['status'], row['operTime']]

                    reccords.append(record)
                # 缓存中行数超过300保存到文件，然后清理缓存
                if len(reccords) > 500:
                    save('opt_log.txt', reccords)
                    reccords.clear()
            # 在循环外把缓存中的数据全部保存到文件
            if len(reccords) > 0:
                save('opt_log.txt', reccords)
                reccords.clear()

    def get_login_log_by_request(self):
        # 登录日志的分页查询url
        menu_url = 'http://127.0.0.1:9999/monitor/logininfor/list'

        # 登录日志菜单url
        menu_root_url = 'http://127.0.0.1:9999/monitor/logininfor'
        # 模拟浏览器发起请求
        self.chrome.get(menu_root_url)

        time.sleep(3)
        self.save_cookie(self.chrome)
        # 获得总的行数
        data_header = []
        reccords = []

        # 爬取表头
        infoId = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[2]').text
        loginName = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[3]').text
        ipaddr = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[4]').text
        loginLocation = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[5]').text
        browser = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[6]').text
        os = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[7]').text
        status = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[8]').text
        msg = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[9]').text
        loginTime = self.chrome.find_element(By.XPATH, '//*[@id="bootstrap-table"]/thead/tr/th[10]').text
        data_header.append([infoId, loginName, ipaddr, loginLocation, browser, os, status, msg, loginTime])
        print(data_header)
        save('login_log.txt', data_header)

        # 查询分页数据
        if self.ifHas(By.CLASS_NAME, 'pagination-info'):
            # 找到记录号偏移数据，判断是否需要分页
            # html:显示第 1 到第 50 条记录，总共 248378 条记录
            page_info_text = self.chrome.find_element(By.CLASS_NAME, 'pagination-info').text
            page_info = re.findall(r'\d+', page_info_text)
            time_str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
            print(time_str + '当前页 {0} ，获取到记录总数:{1} '.format(page_info[0], page_info[2]))
            total = int(page_info[2])
            page_size = 50
            # 计算页数，总页数=(总数+页大小-1)/页大小
            pages = int((total + page_size - 1) / page_size) + 1
            for page_no in range(1, pages):
                time.sleep(random.uniform(1.1, 3.1))
                time_str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
                print(time_str + ' 开始爬取第{0} 页，总页数{1} '.format(page_no, pages))
                fake_parameters = {
                    'pageSize': page_size,  # 每一页的行数
                    'pageNum': page_no,  # 当前页码
                    'orderByColumn': 'loginTime',
                    'isAsc': 'desc',
                    'ipaddr': '',
                    'loginName': '',
                    'status': ''
                }
                json_result = self.spider_request(page_size, page_no, menu_url, menu_root_url, fake_parameters)
                # 最后一页里面rows=null ,因此需要判断是否为空，是空时返回
                if not json_result.get('rows'):
                    break
                for row in json_result.get('rows'):
                    record = [row['infoId'], row['loginName'], row['ipaddr'],
                              row['loginLocation'], row['browser'], row['os'],
                              row['msg'], row['loginTime']]

                    reccords.append(record)
                # 缓存中行数超过300保存到文件，然后清理缓存
                if len(reccords) > 500:
                    save('login_log.txt', reccords)
                    reccords.clear()
            # 在循环外把缓存中的数据全部保存到文件
            if len(reccords) > 0:
                save('login_log.txt', reccords)
                reccords.clear()


def start_spider():
    r = RuoYiSpider('http://127.0.0.1:9999/')
    # run the following methods in order, with try catch
    r.login()
    r.get_role()
    # r.get_menu()
    # r.get_dept()
    # r.get_post()
    # r.get_dict()
    # r.get_settings()
    # r.get_opt_log()
    # r.get_opt_log_by_request()
    # r.get_login_log_by_request()
    r.quit()
    # for mtd in ['login', 'get_role', 'get_menu', 'get_dept', 'get_post', 'get_dict', 'get_settings', 'get_opt_log',
    #             'get_opt_log_by_request', 'get_login_log_by_request']:
    #     try:
    #         getattr(r, mtd)()
    #     except Exception as e:
    #         # print [ERR ] in red
    #         # print("[ERR ]: Failed to run method {0} with error {1}".format(mtd, e))
    #         print("\033[1;31m[ERR ]\033[0m: Failed to run method {0} with error {1}".format(mtd, e))
    #         continue
    #     finally:
    #         r.quit()


if __name__ == '__main__':
    start_spider()
