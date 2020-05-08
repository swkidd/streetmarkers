from django.contrib import admin

from .models import MarkerType, PathType, Palace, Path, BasicMarker, PalaceOwner

admin.site.register(MarkerType)
admin.site.register(PathType)
admin.site.register(BasicMarker)
admin.site.register(Path)
admin.site.register(Palace)
admin.site.register(PalaceOwner)
