''' import doc string '''
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView
from .tasks import fetch

class HomePageView(TemplateView):
    ''' function docstring'''
    template_name = 'index.html'
#     def get(self, request):
#         '''docstring'''
#         form = CarSearchForm()
#         return render(request, self.template_name, {'myform' : form})

def search_result(request):
    ''' method docstring'''
    initial_list = [0]
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
        initial_list = fetch.delay(last_page, link).get()
        return HttpResponse(temp.render({'initial_list' : initial_list}, request))
        
