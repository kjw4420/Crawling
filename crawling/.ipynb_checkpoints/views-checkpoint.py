from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
# import requests
import time

# 크롤링 모듈 import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#By import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#event
from selenium.webdriver import ActionChains


#데이터 분석
# 시각화에 쓰이는 라이브러리
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 횟수를 기반으로 딕셔너리 생성
from collections import Counter

# 문장에서 명사를 추출하는 형태소 분석 라이브러리
from konlpy.tag import Hannanum

# figure, xlabel, ylabel, title 설정 및 데이터 시각화
import matplotlib.pyplot as plt
# import seaborn as sns



class CrawlingRouter(APIView):
    def get(self, request):
        return Response({'success':True})
    
    #데이터 분석
    def WordParsing(self,news_data):
        hannanum = Hannanum()
        nouns_list =[]
        for i in range(len(news_data)):
            #무의미한 문자 없애기
            data = news_data[i]
            replace_list = ["‘","’","”","“",'"',"'","[포토]","[사설]","[CarTalk]","...","…","[단독]"]
            for j in replace_list:
                data = data.replace(j, "")
                
            nouns = hannanum.nouns(data)
            nouns_list += nouns
            
            #개수 확인
            
            # print(i, nouns_list)
            # print(i,data)
        # return news_data
        counter = Counter(nouns_list)
        x = [elem[0] for elem in counter.most_common(10)]
        y = [elem[1] for elem in counter.most_common(10)]
        
        # # print(x)
        # plt.figure(figsize=(20,10))
        # plt.title("Frequency of question in Hashcode")
        # plt.xlabel("Tag")
        # plt.ylabel("Frequency")

        # sns.barplot(x=x,y=y) #막대 그래프 그리기

        # plt.show()

    #크롤링(데이터 가져오기)
    def post(self, request):

        #크롬 실행
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            
            #언론사 뉴스 홈-> 경향신문(첫번째)
            driver.get("https://news.naver.com/main/officeList.naver")
            button = driver.find_element(By.XPATH, '//*[@id="groupOfficeList"]/table/tbody/tr[1]/td/ul/li[1]/a')
            ActionChains(driver).click(button).perform()
            driver.implicitly_wait(5)
            
            news_data=[]
            #버튼으로 언론사 페이지 네이션
            for i in range(2,11): 
                button = driver.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div/div/ul/li[{}]/a'.format(i))
                ActionChains(driver).click(button).perform()
                driver.implicitly_wait(10)
                
                #요약기사(첫 페이지기사만)
                #ul[1]
                for i in range(1, 11): #첫 페이지 10개까지있음
                    # element = driver.find_element(By.XPATH,'//*[@id="main_content"]/div[2]/ul[1]/li[{}]/dl/dt[2]/a'.format(i))
                    element = driver.find_element(By.XPATH,'//*[@id="main_content"]/div[2]/ul[1]/li[{}]/dl/dt[last()]/a'.format(i))
                    # element = driver.find_element('By.XPATH','//*[@id="main_content"]/div[2]/ul[1]/li[{}]/dl//'.format(i))
                    # print(element.text)
                    
                    news_data.append(element.text)
                    # //*[@id="main_content"]/div[2]/ul[1]/li[5]/dl/dt/a
                #ul[2]
                for i in range(1, 11): #첫 페이지 10개까지있음
                    element = driver.find_element(By.XPATH,'//*[@id="main_content"]/div[2]/ul[2]/li[{}]/dl/dt[last()]/a'.format(i))    
                    # print(element.text)
                    news_data.append(element.text)

                
            # print(news_data)
            self.WordParsing(news_data)
            title = driver.title
            url = driver.current_url

            # 형태소 분석
            

            return Response({'title': title, 'url': url})
            # return redirect('WordParsing', news_data)
        
# def WordParsing(news_data):
#     # news_data= get_object_or_404(news_data) #해당 pk값에 맞는 객체 가져오기
#     # news_data = news_data.objects.all(news_data)
#     print(news_data)
#     return news_data




