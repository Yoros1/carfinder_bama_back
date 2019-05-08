''' import doc string '''
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    ''' function docstring'''
    template_name = 'index.html'
#     def get(self, request):
#         '''docstring'''
#         form = CarSearchForm()
#         return render(request, self.template_name, {'myform' : form})

def inspect(detail):
    '''func Docstring'''
    ins_amo = ins_num = pre_pay = 0
    description = ''
    car_detail = 'https://bama.ir' + detail  #########
    car_data = requests.get(car_detail)
    soup = BeautifulSoup(car_data.text, 'html.parser')
    release_date = soup.find('span', itemprop='releaseDate', datetime=True)['datetime'] ########
    brand = soup.find('span', itemprop='brand').text  #############
    model_temp = soup.find('span', itemprop='model')
    model = re.sub(r'\s+', ' ', soup.find('span', itemprop='model').text).strip() ##########
    style_temp = model_temp.find_next_sibling('span')
    style = re.sub(r'\s+', ' ', style_temp.find_next_sibling('span').text)
    style = re.sub(r'، ', '', style).strip() ############
    odo_label = soup.find('span', attrs={'class' : 'label'}, string='كاركرد   ')
    odo_meter = re.sub(r',', '', odo_label.find_next_sibling('span').text).strip()
    price = 0
    if odo_meter == 'کارتکس':
        odo_meter = 0
        description += '//کارتکس//'
    elif re.search(r'\d', odo_meter):
        odo_meter = int(re.findall(r'\d+', odo_meter)[0]) #############

    if bool(soup.find('span', attrs={'class':'label'}, string='پیش پرداخت ')):
        description += '//اقساطی//'
        pre_pay = int(soup.find('span', itemprop='price')['content'])   #######
        ins_num_label = soup.find('span', attrs={'class':'label'}, string='تعداد اقساط ')
        ins_num = int(re.findall(r'\d+', ins_num_label.find_next_sibling('span').text)[0])  #######
        ins_amo_label = soup.find('span', attrs={'class':'label'}, string='مبلغ هر قسط  ')
        ins_amo = re.sub(r',', '', ins_amo_label.find_next_sibling('span').text)
        ins_amo = int(re.findall(r'\d+', ins_amo)[0].strip())
        price = 0

    elif bool(soup.find('span', attrs={'class':'label'}, string='قیمت   ')):
        price_desc = soup.find('span', itemprop='price', content=True)['content'].strip()
        if price_desc != '0':
            price = int(re.sub(r',', '', price_desc))

        elif soup.find('span', itemprop='price', content='0').text.strip() == 'در توضیحات':
            price_desc = soup.find('span', style='font-weight:bold;').text
            price = int(re.findall(r'\d+', re.sub(r',', '', price_desc))[0])

        elif soup.find('span', itemprop='price', content='0').text.strip() == 'حواله':
            return 0

        elif soup.find('span', itemprop='price', content='0').text.strip() == 'تماس بگيريد':
            return 0

    car_data = (brand, model, style, release_date, odo_meter,
                price, pre_pay, ins_amo, ins_num, description,)
    return car_data

def fetch(last_page, link):
    ''' fetch doc string'''
    main_list = []
    car_count = 0
    for i in range(1, last_page):
        page_number = '?page=' + str(i)
        mylink = link + page_number
        mypage = requests.get(mylink).text
        soup = BeautifulSoup(mypage, 'html.parser')
        details = soup.find_all('a', attrs={'class':'cartitle cartitle-desktop'}, href=True)
        for j in range(0, 12):
            detail = re.sub(r'\s+', ' ', details[j]['href']).strip()
            data = inspect(detail) # detail link preparing for process
            if data != 0:
                car_count += 1
                main_list.append(data)
            if car_count > 19:
                break
        if car_count > 19:
            break
    return main_list

def search_result(request):
    ''' method docstring'''
    temp = loader.get_template('./SearchResult.html')
    if request.method == 'POST':
        term = request.POST.get('term', None)
        term += ' باما'
        link = search(term, tld='com', num=1,)
        link = next(link)
        first_page = requests.get(link).text
        soup1 = BeautifulSoup(first_page, 'html.parser')
        nav = soup1.find_all('h4')[1].text
        car_per_page = int(re.findall(r'\[\s+\d+\s+تا\s+(\d+)\s+از\s+\d+', nav)[0])
        total_car_num = int(re.findall(r'\[\s+\d+\s+تا\s+\d+\s+از\s+(\d+)', nav)[0])
        last_page = total_car_num // car_per_page
        main_list = fetch(last_page, link)
        return HttpResponse(temp.render({'main_list' : main_list}, request))
            