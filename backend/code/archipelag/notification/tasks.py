# -*- coding: utf-8 -*-
from logging import getLogger

from django.core.mail import send_mail
from django.conf import settings

from archipelag.app.celery import capp
from archipelag.Market.models import Market
from archipelag.ngo.models import NgoUser
from archipelag.notification.models import Notification

logger = getLogger(__name__)


@capp.task(ignore_result=True)
def send_notification_for_event(event_id):
    logger.info('Dispatching notification for event {}'.format(event_id))
    try:
        event = Market.objects.get(id=event_id)
        for user in NgoUser.objects.exclude(id=event.owner.id):
            notification = Notification(
                event=event,
                owner=user)
            notification.save()
            send_notification.delay(notification.id)
        logger.info('Dispatching notification for event {} finished'.format(event_id))
    except Event.DoesNotExist:
        logger.error('Event object with id {} not found'.format(event_id))


@capp.task(ignore_result=True)
def send_notification(notification_id):
    logger.info('Sending notification id {}'.format(notification_id))
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.error('Notification object with id {} not found'.format(notification_id))
        return

    event = notification.event
    user = notification.owner.user
    if not user.email:
        logger.error('Notification object with id {} can not be sent, because user has no email'.format(
            notification_id))
        return

    send_mail(
        '[Nowe wydarzenie] {}'.format(event.title),
        event.text,
        settings.NOTIFICATION_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    notification.sent = True
    notification.save()

    logger.info('Notification id {} sent'.format(notification_id))
