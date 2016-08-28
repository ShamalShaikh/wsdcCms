from django.contrib import admin

# Register your models here.
from .models import User, Conference, Page, Paper, Profile

from django.db.models import Q




class ConferenceAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(ConferenceAdmin, self).get_queryset(request)

        #queryset.filter(Q(pages__userdept=request.user)|Q(department=None)|Q(department__isnull=True)|Q(department=request.user.deptuser.department)).distinct()

        #user.groups.filter(name__in=['group1', 'group2']).exists()
        if request.user.groups.filter(name='admin').exists():
            return queryset
        elif request.user.groups.filter(name='manager').exists():
            #return queryset.filter(Q(cid=request.user.profile.conferenceId))
            return queryset.filter(Q(mid=request.user.id))
        else:
            return Conference.objects.none()

    def save_model(self, request, obj, form, change):
        if(request.user.groups.filter(name = 'admin').exists()):
            obj.save()
        elif request.user.groups.filter(name='manager').exists():
            #todo if user cid and confidmatches
            obj.save()



class PageAdmin(admin.ModelAdmin):

    def get_queryset(self, request):


        queryset = super(PageAdmin, self).get_queryset(request)

        if request.user.groups.filter(name='admin').exists():
            return queryset
        elif request.user.groups.filter(name__in = ['manager','editor']).exists():
            #todo match page cid and user cid
            cids = []

            confs = Conference.objects.filter(mid=request.user.id)

            for conf in confs:
                cids.append(conf.cid)

            return queryset.filter(Q(cid__in = cids ))
        else:
            return Page.objects.none()

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['admin','manager','editor']):
            obj.save()




class PaperAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(PaperAdmin, self).get_queryset(request)
        if request.user.groups.filter(name = 'admin').exists():
            return queryset
        elif request.user.groups.filter(name = 'manager').exists():
            #todo match papercid and usercid
            return queryset.filter(Q(cid=request.user.profile.conferenceId))

        elif request.user.groups.filter(name = 'attendee').exists():
            return queryset
        else:
            return Paper.objects.none()

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['admin','manager','attendee']):
            obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if  request.user.groups.filter(name__in=['admin','manager']).exists():
            self.exclude = []
        elif  request.user.groups.filter(name='attendee').exists():
            self.exclude = ('approved','uid', )
        else:
            pass
        return super(PaperAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Profile)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Paper, PaperAdmin)
