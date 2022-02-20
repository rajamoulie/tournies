from django.contrib import admin

from .models import Sport, Tourney, Message

# Register your models here.

admin.site.register(Sport)
admin.site.register(Tourney)
admin.site.register(Message)