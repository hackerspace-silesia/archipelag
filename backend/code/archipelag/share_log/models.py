from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model

from archipelag.ngo.models import NgoUser
from archipelag.message.models import Message


class ShareLog(Model):
    owner = ForeignKey(NgoUser, null=False, blank=False)
    date_created = DateTimeField(auto_now_add=True)
    message = ForeignKey(Message, null=False, blank=False)

    def __str__(self):
        return "log type {} for id {}".format(self.message.type.service, self.message)

    def get_share_log(self):
        date_created = self.date_created.strftime("%Y-%m-%d %H:%M")
        return "Użytkownik {} udostępnił na {} dnia {}".format(self.owner, self.message.type.service, date_created)

    class Meta:
        ordering = ('date_created',)
