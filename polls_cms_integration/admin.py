from django.contrib import admin

# Register your models here.
from .models import  * 


# Workshops table
class WorkshopAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['user_name','workshop_id', 'workshop_name', 'workshop_date'],
        }),
    ]
    list_display = ('user_name','workshop_id', 'workshop_name', 'workshop_date')
    search_fields = ['user_name','workshop_id', 'workshop_name', 'workshop_date']

# Langzeitstationär table 
class LangPollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Langzeitstationär Mouse over effect table 
class LangMouseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Langzeitstationär answers table
class LangPoll_AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id'],
        }),
    ]
    list_display = ('ques_id', 'question', 'choice', 'comment', 'comment_unless', 'skipped', 'category','workshop_id')
    search_fields = ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id']

# Akutstationär table
class AkuPollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Akutstationär Mouse over effect table 
class AkuMouseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Akutstationär answers table
class AkuPoll_AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id'],
        }),
    ]
    list_display = ('ques_id', 'question', 'choice', 'comment', 'comment_unless', 'skipped', 'category','workshop_id')
    search_fields = ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id']

# Ambulant table 
class AmbuPollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Ambulant Mouse over effect table 
class AmbuMouseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics'],
        }),
    ]
    list_display = ('ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics')
    search_fields = ['ques_id','economy', 'care', 'technology', 'embedding', 'law', 'ethics']

# Ambulant answers table 
class AmbuPoll_AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id'],
        }),
    ]
    list_display = ('ques_id', 'question', 'choice', 'comment', 'comment_unless', 'skipped', 'category','workshop_id')
    search_fields = ['question', 'choice', 'comment', 'comment_unless', 'skipped', 'ques_id', 'category','workshop_id']

# Setting table
class SettingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['workshop_id', 'setting', 'company_name', 'robot_name'],
        }),
    ]
    list_display = ('workshop_id', 'setting', 'company_name', 'robot_name')
    search_fields = ['workshop_id', 'setting', 'company_name', 'robot_name']

# Roles table 
class RolesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['workshop_id', 'role_id', 'role', 'names'],
        }),
    ]
    list_display = ('workshop_id', 'role_id', 'role', 'names')
    search_fields = ['workshop_id', 'role_id', 'role', 'names']
    
# Langzeitstationär roles table
class RolesLangAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['role_id', 'role_name', 'mandatory'],
        }),
    ]
    list_display = ('role_id', 'role_name', 'mandatory')
    search_fields = ['role_id', 'role_name', 'mandatory']

# Akutstationär roles table
class RolesAkuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['role_id', 'role_name', 'mandatory'],
        }),
    ]
    list_display = ('role_id', 'role_name', 'mandatory')
    search_fields = ['role_id', 'role_name', 'mandatory']

# Ambulant roles table
class RolesAmbuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['role_id', 'role_name', 'mandatory'],
        }),
    ]
    list_display = ('role_id', 'role_name', 'mandatory')
    search_fields = ['role_id', 'role_name', 'mandatory']


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(LangPoll, LangPollAdmin)
admin.site.register(LangMouse, LangMouseAdmin)
admin.site.register(LangPoll_Answer, LangPoll_AnswerAdmin)
admin.site.register(AkuPoll, AkuPollAdmin)
admin.site.register(AkuMouse, AkuMouseAdmin)
admin.site.register(AkuPoll_Answer, AkuPoll_AnswerAdmin)
admin.site.register(AmbuPoll, AmbuPollAdmin)
admin.site.register(AmbuMouse, AmbuMouseAdmin)
admin.site.register(AmbuPoll_Answer, AmbuPoll_AnswerAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(RolesLang, RolesLangAdmin)
admin.site.register(RolesAku, RolesAkuAdmin)
admin.site.register(RolesAmbu, RolesAmbuAdmin)