import requests
from bs4 import BeautifulSoup
import time
import random
import csv

global driver
clinics_dict = {}
base_url = 'https://www.hfea.gov.uk'
'/choose-a-clinic/clinic-search/results/9129/'
all_clinics_url_segment = '/choose-a-clinic/clinic-search/all-clinics/?alpha='
clinic_statistics_url_segment = 'statistics/?age=o44&treatment=ivf_icsi&year=2018&source=FSO'
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
age_groups = ['b35', '35-37', '38-39', '40-42', '43-44', 'o44']


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
            clinics_dict[url] = links.text
    # print(clinics_dict)


def get_clinic_details(clinic_url_segment):
    url = build_clinic_statistics_url(clinic_url_segment)

    soup = get_website_content(url)
    dsa = soup.find_all('span', {'class': 'stat-large'})
    if len(dsa) == 0 or dsa[0].text == '**':
        print(url)
        return 0

    overview_stats = [clinics_dict[clinic_url_segment]]
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
    table = s.find('table', {'class': 'waiting-times-table'})
    rows = table.find_all('tr')
    for row in rows:
        dat = row.find_all('td')
        a = dat[1].text
        overview_stats.append(a)


    s = soup.find('div', {'id': 'collapse-stats-subcollapseThree-2'})
    table = s.find('table', {'class': 'waiting-times-table'})
    rows = table.find_all('tr')
    for row in rows:
        dat = row.find_all('td')
        a = dat[1].text
        overview_stats.append(a)


    s = soup.find('div', {'id': 'collapse-stats-subcollapseThree-3'})
    table = s.find('table', {'class': 'waiting-times-table'})
    rows = table.find_all('tr')
    for row in rows:
        dat = row.find_all('td')
        a = dat[1].text
        overview_stats.append(a)
    print(table)
    points_of_intrest = [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16]
    pregnancies_and_births = soup.find_all('div', {'class' : 'detailedStats-comparisionContent'})
    for pregnancies_and_birth in pregnancies_and_births:
        data_points = pregnancies_and_birth.find_all('div', {'class': 'col-sm-12 col-md-4 col ps-30'})
        for position in points_of_intrest:
            if position >= len(data_points):
                break
            point = data_points[position]
            d = point.find('span', {'class': 'h3'})
            if d is not None:
                overview_stats.append(d.text)
            else:
                e = point.find('span', {'class': 'stat-large clinic-rate mb-20'})
                overview_stats.append(e.text)
    f = open('o44.csv', 'a')
    writer = csv.writer(f)
    writer.writerow(overview_stats)
    f.close()

    print(overview_stats)


def main():
    global driver
    for letter in letters:
        print(letter)
        get_clinics(letter)
    # get_clinics(phase__letters[0])
    # print(len(clinics_dict))
    count = 0
    for clinic in clinics_dict:
        count = count + 1
        # count = count + get_clinic_details(clinic)
        get_clinic_details(clinic)
        time.sleep(5)
        # if count >= 10:
        #     time.sleep(120)
    # print('total clinics is: ')
    # print(count)
    # get_clinic_details('/choose-a-clinic/clinic-search/results/15/')
    # get_clinics(letters[0])


if __name__ == '__main__':
    main()
