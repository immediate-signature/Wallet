from bs4 import BeautifulSoup as BS
import urllib.request
def get_rate():
   with urllib.request.urlopen('https://www.google.com/finance/quote/BTC-usd') as response:
      html = response.read()

   soup = BS(html)
   data_tag = soup.find('div', 'YMlKec fxKbKc')
   rate = data_tag.contents[0]
   num =''
   for i in range(0,len(rate)):
      if rate[i] != ',':
         num = num + rate[i]
   return num