from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from archipelag.message.forms import MessageForm
from archipelag.message.models import Message
from archipelag.market.models import Market
from archipelag.event_log.models import EventLog
from archipelag.event_log.models import SHARE

#from archipelag.notification.tasks import send_notification_for_event

from archipelag.market.settings import POINTS_RULES
from archipelag.ngo.models import NgoUser


@login_required
def message_create(request, market_id):
    if request.method != 'POST':
        form = MessageForm()
        return render(request, 'registration/message.html', {'form': form})
    form = MessageForm(request.POST)
    if not form.is_valid():
        return
    msg_market = create_new_message_row(form, market_id)
    add_coins_if_rules_allow(request.user.ngouser, market_id)
    #send_notification_for_event.delay(event.id)
    statement = get_statement_for_user(msg_market)
    form = MessageForm()
    return render(request, 'registration/message.html', {'form': form, 'message': statement})


def get_statement_for_user(msg_market):
    service_name = msg_market.type.service
    return "Twoja wiadomość na {} została dodana, dodaj wiadomości na inne platformy".format(service_name)


def create_new_message_row(form, market_id):
    msg_market = form.save(commit=False)
    market = Market.objects.get(id=market_id)
    msg_market.market = market
    msg_market.save()
    return msg_market


def add_coins_if_rules_allow(ngo, market_id):
    messages = Message.objects.filter(market_id=market_id).count()
    if messages > 3:
        coins_to_add = POINTS_RULES['create_more_than_three_messages_format']
        ngo_model = NgoUser()
        ngo_model.add_coins(ngo, coins_to_add)


def add_coins_for_share(request, message_id):
    message = Message.objects.filter(id=message_id).first()
    current_ngo = request.user.ngouser
    save_log(message.id, current_ngo)
    current_ngo.add_coins(current_ngo, POINTS_RULES['for_share'])
    current_ngo.save()
    return redirect('market_details', market_id=message.market.id)


def save_log(msg_id, ngo):
    log = EventLog(type=SHARE, id_connected_object=msg_id, owner=ngo)
    log.save()
