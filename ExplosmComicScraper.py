from bs4 import BeautifulSoup
import requests
import pathlib

def month_number(month):    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    return months.index(month) + 1

def month_name(month_number) :  
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    return months[month_number-1]

#Reading the input text file
with open('input.txt', 'r') as input:
    start = input.readline().split(' ')
    end = input.readline().split(' ')
    authors = input.readline().split(' ')

#Random Comic downloader
if start[0] == 'Random' :
    soup = BeautifulSoup(requests.get('http://explosm.net/rcg').text, 'lxml')
    comic_panel = soup.find('div', class_='rcg-panels')
    number = 1
    for img in comic_panel.findAll('img') :
        image_url = img.get('src')
        pathlib.Path('./random/').mkdir(parents=True, exist_ok=True)
        with open(f'./random/frame{number}.png', 'wb') as image :
            image.write(requests.get(image_url).content)
        print(f'./random/frame{number}.png')
        number += 1
#Latest Comic Downloader
elif start[0] == 'latest' :
    url = requests.get('http://explosm.net/comics/archive').text
    soup = BeautifulSoup(url, 'lxml')
    for url in soup.findAll('div', class_='small-3 medium-3 large-3 columns', limit=int(start[1])):
        comic_url = 'http://explosm.net' + url.a.get('href')
        comic_soup = BeautifulSoup(requests.get(comic_url).text, 'lxml')
        imageid = 'http:'+comic_soup.find('img', id='main-comic')['src']
        filename = comic_soup.find('div', id='comic-author').text.split('\n')[1] #Extracting the date of comic upload
        author = comic_soup.find('div', id='comic-author').text.split('\n')[2].split(' ')[1] #Extracting Author's first name
        pathlib.Path(f'./latest').mkdir(parents=True, exist_ok=True)   #Directory Creation for the comic
        
        image_url = requests.get(imageid)
        with open(f'./latest/{filename}-{author}.png', 'wb') as image:  #Downloading and saving the comic
            image.write(image_url.content)
        print(f'./latest/{filename}-{author}.png')
#Input based downloader (Takes start month, year and end month, year, authors as inputs and downloads the specified comics)
else :
    i=0
    #Code snippet to make sure that the authors are in lowercase
    for author in authors :
        authors[i] = author.lower()
        i+=1

    start_month = month_number(start[0])
    end_month = month_number(end[0])
    start_year = int(start[1])
    end_year = int(end[1])

    for year in range(start_year, end_year+1, 1) :
        start = 1
        end = 13
        if year == end_year :
            end = end_month+1
        if year == start_year :
            start = start_month
        for month in range(start, end, 1) :
            Month = month_name(month) #Getting the name of the month
            for author in authors :
                url = requests.get(f'http://explosm.net/comics/archive/{year}/{month}/{author}').text
                soup = BeautifulSoup(url, 'lxml')
                for url in soup.findAll('div', class_='small-3 medium-3 large-3 columns'):
                    comic_url = 'http://explosm.net' + url.a.get('href')
                    comic_soup = BeautifulSoup(requests.get(comic_url).text, 'lxml')
                    imageid = 'http:'+comic_soup.find('img', id='main-comic')['src']
                    filename = comic_soup.find('div', id='comic-author').text.split('\n')[1] #Extracting the date of comic upload
                    pathlib.Path(f'./{year}/{Month}').mkdir(parents=True, exist_ok=True)   #Directory Creation for the comic
                    
                    image_url = requests.get(imageid)
                    with open(f'./{year}/{Month}/{filename}-{author}.png', 'wb') as image:  #Downloading and saving the comic
                        image.write(image_url.content)
                    print(f'./{year}/{Month}/{filename}-{author}.png') 
        
        

