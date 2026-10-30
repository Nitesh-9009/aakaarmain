from django.contrib import admin

# Register your models here.


from import_export.admin import ImportExportModelAdmin
# Register your models here.


from .models import poster_class

@admin.register(poster_class)
# @admin.register(TaskOne)
class userdetail(ImportExportModelAdmin):
    pass


# Register your models here.
