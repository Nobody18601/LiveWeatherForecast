from django.shortcuts import render
import requests
import datetime

# NEWS API
api_key="06a56f6093cb4656a2e1c488c9ccb2f3" #you can take it from https://newsapi.org 

# WEATHER API
whe_api="f2be27edff0dc8e2cb74dc9a085e7f65" #you can take it from https://api.openweathermap.org



# Create your views here.
def home(request):
    main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+api_key
    news=requests.get(main_url).json()
    articles=news["articles"]
    stock=requests.get("https://newsapi.org/v2/everything?q=nse&apiKey="+api_key).json()['articles'][0]
    sports=requests.get("https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey="+api_key).json()['articles'][0]
    corona=requests.get("https://newsapi.org/v2/everything?q=corona&apiKey="+api_key).json()['articles'][0]
    print(stock)
    print(sports)
    print(corona)
    top_articles=[]
    for i in range(6):
        top_articles.append(articles[i])
    rangex=range(3)
    return render(request,'home.html',{'articles':top_articles,'stock':stock,'corona':corona,'sports':sports})



#from newsapi import NewsApiClient



def news(request,slug):
    #main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+api_key
    main_url="https://newsapi.org/v2/top-headlines?country=in&category="+slug+"&apiKey="+api_key
    if slug == "stock-news":
        main_url="https://newsapi.org/v2/everything?q=nse&apiKey="+api_key
    elif slug == "corona":
        main_url="https://newsapi.org/v2/everything?q=corona&apiKey="+api_key
    news=requests.get(main_url).json()
    article=news["articles"]
    
    top_articles=[]
    for i in range(3):
        top_articles.append(article[i])
    context=article
    return render(request,'news.html',{'articles':article,'category':slug,'top_articles':top_articles})



def sing_news(request,slug,slug2):
    print(slug)
    print(slug2)
    main_url="https://newsapi.org/v2/top-headlines?country=in&category="+slug+"&apiKey="+api_key
    if slug == "all":
        main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+api_key
    elif slug == "stock-news":
        main_url="https://newsapi.org/v2/everything?q=nse&apiKey="+api_key
    elif slug == "corona":
        main_url="https://newsapi.org/v2/everything?q=corona&apiKey="+api_key
    
    news=requests.get(main_url).json()
    article=news["articles"]
    #print(news)
    print(type(article))
    
    new=[]
    for i in article:
        if i['title']==slug2:
            new.append(i)
            continue
        print(i)
        print(new)
        #print(dict(new))
    return render(request,'single_news.html',{'snews':new[0]})


def weather(request):
    if request.method=="GET":
        
        base_url="https://api.openweathermap.org/data/2.5/weather?q="
        city=request.GET['city']
        complete_url=base_url+city+"&appid="+whe_api
        api_link=requests.get(complete_url)
        #api_link.raise_for_status()
        #if api_link.status_code != 20:
        api_data = api_link.json()
        if api_data['cod'] == '404':
            return render(request,'error.html')
        else:
            temp_city=((api_data['main']['temp'])-273.15)
            wheather_disc=api_data['weather'][0]['description']
            hmdt=api_data['main']['humidity']
            wind_spd=api_data['wind']['speed']
            date_time=datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    return render(request,'weather.html',{'tc':temp_city,'wd':wheather_disc,'ht':hmdt,'ws':wind_spd,'dt':date_time,'city':city})
