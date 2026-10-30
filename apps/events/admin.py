from django.contrib import admin

from .models import Cenex,ceohour, StaadPro, Fusion,LabVisit,Primavera,Staad_payment,Primavera_payment,Fusion_payment,Fusionplusstaad_payment,Primaveraplusstaad_payment,Fusionplusstaad_reg,labpayment_modal
# from .models import TaskOne
# Register your models here.
# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.




@admin.register(Cenex)
class userdetail(ImportExportModelAdmin):
    pass
@admin.register(StaadPro)
class staadpro_excel(ImportExportModelAdmin):
    pass
@admin.register(Fusion)
class fusion_excel(ImportExportModelAdmin):
    pass

@admin.register(LabVisit)
class fusion_excel(ImportExportModelAdmin):
    pass
@admin.register(Primavera)
class primavera_excel(ImportExportModelAdmin):
    pass


@admin.register(Fusionplusstaad_payment)
class fusionpayment_excel(ImportExportModelAdmin):
    pass
@admin.register(Primaveraplusstaad_payment)
class primaveraplusstaad_excel(ImportExportModelAdmin):
    pass
@admin.register(Staad_payment)
class staad_payment(ImportExportModelAdmin):
    pass
@admin.register(Fusion_payment)
class fusion_payment(ImportExportModelAdmin):
    pass
@admin.register(Primavera_payment)
class primavera_payment(ImportExportModelAdmin):
    pass

@admin.register(Fusionplusstaad_reg)
class fusionplusstaad_excel(ImportExportModelAdmin):
    pass

@admin.register(labpayment_modal)
class fusionplusstaad_excel(ImportExportModelAdmin):
    pass

@admin.register(ceohour)
class ceohour(ImportExportModelAdmin):
    pass


#admin.site.register(Cenex)




