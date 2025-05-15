from django.contrib import admin
from .models import EmergencyCondition, AssessmentStep, AssessmentChoice, CPRTimer, PatientStatus, EmergencyProtocol, CyrillicTag, EmergencyMedia

class AssessmentChoiceInline(admin.TabularInline):
    model = AssessmentChoice
    extra = 1
    fk_name = 'step'

class AssessmentStepInline(admin.TabularInline):
    model = AssessmentStep
    extra = 1
    show_change_link = True

class EmergencyMediaInline(admin.TabularInline):
    model = EmergencyMedia
    extra = 1
    fields = ('image', 'description', 'order')
    ordering = ('order',)

@admin.register(EmergencyCondition)
class EmergencyConditionAdmin(admin.ModelAdmin):
    inlines = [EmergencyMediaInline]
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [AssessmentStepInline]
    search_fields = ('title', 'description')

@admin.register(AssessmentStep)
class AssessmentStepAdmin(admin.ModelAdmin):
    list_display = ('question', 'emergency', 'order')
    list_filter = ('emergency',)
    inlines = [AssessmentChoiceInline]
    ordering = ('emergency', 'order')

@admin.register(CPRTimer)
class CPRTimerAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'is_active')
    
    def has_add_permission(self, request):
        return not CPRTimer.objects.exists()

@admin.register(PatientStatus)
class PatientStatusAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'emergency', 'consciousness', 'breathing', 'heartbeat', 'created_at')
    list_filter = ('emergency', 'consciousness', 'breathing', 'heartbeat')

@admin.register(EmergencyProtocol)
class EmergencyProtocolAdmin(admin.ModelAdmin):
    list_display = ('emergency', 'step', 'order')
    ordering = ['order']

@admin.register(CyrillicTag)
class CyrillicTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'slug']
