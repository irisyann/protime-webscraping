import requests
import csv
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_date():
    date_today = datetime.today().strftime('%y-%m-%d')
    date_yesterday = (datetime.today() - timedelta(1)).strftime('%y-%m-%d')
    print(date_yesterday)
    print(date_today)

    return(date_today, date_yesterday)

def scrape_table():
    URL = 'https://www.worldometers.info/coronavirus/#countries'
    page = requests.get(URL)
    data = page.text
    soup = BeautifulSoup(data, "html.parser")

    date_today, date_yesterday = get_date()

    msia_link = soup.find_all('a',string='Malaysia')[0]
    rows = msia_link.findParent('td').findParent('tr')
    columns = rows.findAll('td')
    cases = columns[3].text
    stripped_cases = re.sub('[^A-Za-z0-9]+', ' ', cases).replace(" ", "")
    if len(cases) > 0:
        with open('coviddata.csv', 'a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([date_today, stripped_cases])
            file.close()

    with open('coviddata.csv') as readfile:
        for line in csv.reader(readfile):
            if line[0] == date_yesterday:
                cases_yesterday = line[1]
            if line[0] == date_today:
                cases_today = line[1]
            else:
                cases_today = 0
    #print(cases_today)
    #print(cases_yesterday)
    return (cases_today, cases_yesterday)


def growth_factor():

    growth_today, growth_yesterday = scrape_table()
    date_today, date_yesterday = get_date()
    print("in growth def")
    print(growth_today)
    print(growth_yesterday)
    if growth_today:
        if growth_yesterday:
            Gf = round(float(growth_today)/float(growth_yesterday),2)
        else:
            Gf = 0
    else:
        Gf = 0
    print(Gf)
    return Gf

#growth_factor(cases_today, cases_yesterday)


from flask import Flask
app = Flask(__name__)

@app.route("/")
#def hello():
#    return "Hello there"

def displaymessage():
    date_today, date_yesterday = get_date()
    cases_today, cases_yesterday = scrape_table()
    Gf = growth_factor()
    if Gf == 0:
        message_body = "Number of cases on " + str(date_today) + " is not updated yet. Please check again at 1800 GMT+8 (6pm Malaysia Time)"
    else:
        message_body = "Number of cases on " + str(date_today) + " = " + str(cases_today) + "\nGrowth factor= " + str(Gf)

    return message_body


if __name__ == "__main__":
  app.run()



#  # A very simple Flask Hello World app for you to get started with...

#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'
    
#td = soup.find(lambda t: t.text.strip()=='Malaysia').parent.select('td')
#for element in zip(td, td[1:]):
#    print(element.text)

#for tr in soup.find_all(href='country/malaysia/'):
#    tds = tr.find('td')
#    print(tds.text.strip())
#for tr in soup.find_all(a="country/malaysia/"):
#    cells = tr.find_all('td')
#    new_cases = cells[0].text.strip()
#    print(new_cases.text.strip())

#results = soup.find(id='main_table_countries_today')
#rows = results.find_all('td')
#for row in rows:
#    cells = row.find_all('tr')
#    print(cells)

#content = results.find_all('td')

#element = soup.find(text='Malaysia')

#total_cases = element.next.strip()
#new_cases = total_cases.next.strip()
##case = element.parent.parent.parent.next_sibling.strip()
#print(new_cases)


#for td in content:
#    if 'Malaysia' in td.text:
#        print(content.parent)

