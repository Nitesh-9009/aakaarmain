from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Submission
# from .models import TaskOne
# Register your models here.
class sympo_excel(ImportExportModelAdmin):
    pass
admin.site.register(Submission,sympo_excel)

from .models import iitb
@admin.register(iitb)
class iitb_import(ImportExportModelAdmin):
    pass

from .models import non_iitb
@admin.register(non_iitb)
class noniitb_import(ImportExportModelAdmin):
    pass






