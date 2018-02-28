# coding = utf-8
from selenium import webdriver
import pandas as pd
class Doubangroup:
    def __init__(self):
        self.url = "https://www.douban.com/group/lovesh/discussion?start= %d"
        #options = webdriver.ChromeOptions()
        #options.add_argument('--user-data-dir=C:\Users\yangz\AppData\Local\Google\Chrome\User Data\Default')
        #options.add_argument('--proxy-server=http://ip:port')
        #options.add_argument('disable-infobars')
        #self.driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Firefox()
        self.discussion = []
        self.total_page = 0

    def get_total_page(self):
        self.driver.get(self.url %0)
        self.total_page = int(self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[3]/a[10]").text)
        print('There is %d page'% self.total_page)

    def get_discussion(self):
        self.get_total_page()
        for one_page in range(self.total_page):
            self.driver.get(self.url% one_page*25)
            self.get_onepage_discussion()


    def get_onepage_discussion(self):
        for item in range(2,27):
            temp = []
            temp.append(self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table/tbody/tr[%s]/td[1]/a"%item).text)

            temp.append(self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table/tbody/tr[%s]/td[2]/a"%item).text)
            
            temp.append(self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table/tbody/tr[%s]/td[3]"%item).text)
            temp.append(self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table/tbody/tr[%s]/td[4]"%item).text)
            self.discussion.append(temp)

    def save_to_xls(self):
        df = pd.DataFrame(self.discussion,columns = ["话题","作者","回应","最后回应"])
        df.to_excel("discussion.xls",encoding = "utf_8_sig")

if __name__=="__main__":
    doubangroup = Doubangroup()
    doubangroup.get_discussion()
    doubangroup.save_to_xls()

