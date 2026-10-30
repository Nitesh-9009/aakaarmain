from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import cityplan_reg
# from .models import TaskOne
# Register your models here.

#admin.site.register(cityplan_reg)
#from .models import taskSeven
@admin.register(cityplan_reg)
class cityplanreg_import(ImportExportModelAdmin):
    pass
