from django.contrib import admin
from .models import Eliot
from home.views import QS_AnyMeasure

class EliotAdmin(admin.ModelAdmin):
    fields = [f.name for f in Eliot._meta.get_fields()]
    list_display = ('device_model', "measurements_timestamp" ,  "device_imei" , 'val', 'metadata_measurementtype')
    readonly_fields = fields
    list_filter = (['measurements_timestamp', 'device_model', 'device_imei', 'metadata_measurementtype'])
    search_fields = (['device_imei'])
    ordering = ('-measurements_timestamp',)
    search_help_text = 'Search by IMEI (any digits)'
    empty_value_display = 'None'
    view_on_site = False
#    actions = [export_csv]

    @admin.display(description='Measured')
    def val(self, obj):
        return QS_AnyMeasure(obj).asobj() # f"{obj.measurements_systolicbloodpressure_value}/{obj.measurements_diastolicbloodpressure_value} {obj.measurements_pulse_value} ({obj.measurements_annotations_irregularheartbeat})"


admin.site.register(Eliot, EliotAdmin)
#admin.site.disable_action('delete_selected')

# to return from admin to 'view site'.
admin.site.site_url = "/"
admin.site.site_header = "M+ Admin for Staff : Trials, webhooks, roles, Pairs"
admin.site.site_title = "site_title>"
admin.site.index_title = "Selection"
