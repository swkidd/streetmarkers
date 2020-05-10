from django.contrib import admin

from .models import PegSystem, BasicPeg, PAOPeg, POPeg, PegType

admin.site.register(POPeg)
admin.site.register(PAOPeg)
admin.site.register(PegType)
admin.site.register(BasicPeg)
admin.site.register(PegSystem)