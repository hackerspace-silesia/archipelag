from json import loads

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.forms import MarketForm
from archipelag.message.models import Message



class MarketView(LoginRequiredMixin, View):
    template_name = 'market/market_list.html'

    def get(self, request):
        return render(
            request, self.template_name,
            {
                'user_messages': Market.objects.all(),
            })


@login_required
def market_create(request):
    if request.method != 'POST':
        return render(request, 'registration/event.html')

    body_data = loads(request.body.decode('utf-8'))
    if not is_fields_are_valid(body_data):
        error = dict(error="Błąd wewnętrzny. Złe pola.")
        return JsonResponse(error)
    current_ngo = request.user.ngouser
    if current_ngo.is_user_can_add_market():
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        new_market = get_new_market(current_ngo, body_data)
        message_create_url = reverse('message_create', args=[new_market.id,])
        return JsonResponse(dict(url=message_create_url))
    else:
        error = dict(error="Za mało punktów.")
        return JsonResponse(error)



def is_fields_are_valid(fields):
    forms = MarketForm(data=fields)
    return forms.is_valid()


def get_new_market(current_ngo, body_data):
    new_market = Market.objects.create(
        owner=current_ngo,
        title=body_data["title"],
        url=body_data["url"],
        date_starting=body_data["date_starting"],
        date_ending=body_data["date_ending"],
        hashtag=body_data["hashtag"]
    )
    return new_market


def get_messages(request, market_id):
    market = Market.objects.filter(id=market_id)
    template_name = 'market/message_list.html'
    return render(
            request, template_name,
            {
                'messages': Message.objects.filter(market=market).all(),
            })

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')