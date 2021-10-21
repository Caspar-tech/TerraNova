from django.contrib import admin

from .models import (
    Square,
    Main,
    Highscore
)

admin.site.register(Square)
admin.site.register(Main)
admin.site.register(Highscore)