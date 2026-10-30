from django.contrib import admin

# Register your models here.
#from .models import threemtt
#admin.site.register(threemtt)

from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import threemtt
#from .models import taskSeven
@admin.register(threemtt)
class threemtt_import(ImportExportModelAdmin):
    pass

