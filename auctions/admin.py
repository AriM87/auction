from django.contrib import admin

from .models import *
admin.site.register(Auction)
# admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)


