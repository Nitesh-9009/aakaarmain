from django.contrib import admin

from .models import Submission , Seismic ,BridgeIt , ConquerIt
# from .models import TaskOne
# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.




@admin.register(Seismic)
class userdetail(ImportExportModelAdmin):
    pass



admin.site.register(Submission)
#admin.site.register(Seismic)

#admin.site.register(BridgeIt)
@admin.register(BridgeIt)
class excel_bridgeit(ImportExportModelAdmin):
    pass




#admin.site.register(ConquerIt)
@admin.register(ConquerIt)
class excel_conquerit(ImportExportModelAdmin):
    pass






