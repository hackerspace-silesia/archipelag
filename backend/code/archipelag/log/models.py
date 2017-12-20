from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveIntegerField

from archipelag.ngo.models import NgoUser

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


class Log(Model):
    owner = ForeignKey(NgoUser, null=False)
    type = CharField(max_length=2, choices=EVENT_TYPES, default=SHARE, null=False)
    date_created = DateTimeField(auto_now_add=True)
    id_connected_object = PositiveIntegerField(null=True)

    def __str__(self):
        return "log type {} for id {}".format(self.type, self.id_connected_object)

    def get_share_log(self):
        return "Użytkownik {} udostępnił to wydarzenie {}".format(self.owner.name, self.date_created)
