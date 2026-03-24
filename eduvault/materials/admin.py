from django.contrib import admin
from .models import Material, CycleAssignment

admin.site.register(Material)
admin.site.register(CycleAssignment)  # ✅ NEW