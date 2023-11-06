from django.contrib import admin
from .models import State, LGA, PollingUnit, ElectionResult, Ward

# Register your models here.


admin.site.register(State)
admin.site.register(LGA)
admin.site.register(PollingUnit)
admin.site.register(ElectionResult)
admin.site.register(Ward)
