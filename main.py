# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from helpers import web_helper
import requests
from bs4 import BeautifulSoup


global driver
clinics_dict = {}
base_url = 'https://www.hfea.gov.uk'
'/choose-a-clinic/clinic-search/results/9129/'
all_clinics_url_segment = '/choose-a-clinic/clinic-search/all-clinics/?alpha='
clinic_statistics_url_segment = 'statistics/?age=35-37&treatment=ivf_icsi&year=2018&source=FSO'
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
age_groups = ['35-37', '38-39', '40-42', '43-44', 'b35', 'o44']


def build_all_clinics_url(letter):
    return base_url + all_clinics_url_segment + letter


def build_clinic_statistics_url(clinic_url_segment):
    return base_url + clinic_url_segment + clinic_statistics_url_segment


def get_website_content(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/35.0.1916.47 Safari/537.36 '
    headers = {'User-Agent': user_agent}
    web_page_content = requests.get(url, headers=headers)
    return BeautifulSoup(web_page_content.content, 'html.parser')


def get_clinics(letter):
    global clinics_dict
    clinics_with_letter_url = build_all_clinics_url(letter)
    soup = get_website_content(clinics_with_letter_url)
    asd = soup.find_all('a', href=True)
    for links in asd:
        url = links.get('href')
        if "choose-a-clinic/clinic-search/result" in url:
            clinics_dict[url] = url
    print(clinics_dict)


def get_clinic_details(clinic_url_segment):
    url = build_clinic_statistics_url(clinic_url_segment)
    print(url)
    soup = get_website_content(url)
    overview_stats = []
    stats = soup.find_all('div', {"class": "overview-stat"})
    for stat in stats:
        figure = stat.find('span', {'class': 'stat-large'})
        data = figure.text
        overview_stats.append(data)
        print(data)
    average_div = soup.find('div', {'class': 'vertical-center'})
    fig = average_div.find('span', {'class': 'stat-large'})
    overview_stats.append(fig.text)

    pie_chart_stats = soup.find_all('div', {'class': 'pieChart-legend'})
    for sta in pie_chart_stats:
        a = sta.find('span', {'class': 'value highlight'})
        overview_stats.append(a.text)

    s = soup.find('div', {'id': 'collapse-stats-subcollapseThree-1'})
    table = s.find('table')
    print(table)

    print(overview_stats)





def main():
    global driver
    # for letter in letters:
    #     get_clinics(letter)
    # get_clinics(letters[0])
    # print(len(clinics_dict))
    # for clinic in clinics_dict:
    #     get_clinic_details(clinic)
    get_clinic_details('/choose-a-clinic/clinic-search/results/19/')
    # get_clinics(letters[0])
    # Using Chrome to access web
    # op = webdriver.ChromeOptions()
    # # op.add_argument('headless')
    # s = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=s, options=op)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
