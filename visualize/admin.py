from django.contrib import admin
from .models import County, GuardianCounted, Geo, Item, Station


admin.site.register(County)
admin.site.register(GuardianCounted)
admin.site.register(Geo)
admin.site.register(Item)
admin.site.register(Station)
