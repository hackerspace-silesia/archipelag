from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveIntegerField

from archipelag.ngo.models import NgoUser
from archipelag.message.models import Message

SHARE = "SH"
ADMIN_PROMOTE = "AP"
REGISTER_FROM_INV = "RI"
REGISTER = "R"
EVENT_TYPES = (
    (SHARE, 'SHARE'),
    (ADMIN_PROMOTE, 'ADMIN PROMOTE'),
    (REGISTER_FROM_INV, 'REGISTER FROM INVITATION'),
    (REGISTER, 'REGISTER'),
)


class EventLog(Model):
    owner = ForeignKey(NgoUser, null=False, blank=False)
    type = CharField(max_length=2, choices=EVENT_TYPES, default=SHARE, null=False, blank=False)
    date_created = DateTimeField(auto_now_add=True)
    id_connected_object = PositiveIntegerField(null=False,)

    def __str__(self):
        return "log type {} for id {}".format(self.type, self.id_connected_object)

    def get_share_log(self):
        date_created = self.date_created.strftime("%Y-%m-%d %H:%M")
        shared_message = Message.objects.filter(id=self.id_connected_object).first()
        return "Użytkownik {} udostępnił na {} dnia {}".format(self.owner, shared_message.type, date_created)

    class Meta:
        ordering = ('date_created',)
