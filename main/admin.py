from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(activity)
admin.site.register(Reservation)
admin.site.register(PreReservation)
admin.site.register(Visitor)
admin.site.register(Feedback)
