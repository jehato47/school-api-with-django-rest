from django.contrib import admin
# from django.contrib.auth.models import User
# from accountancy.models import Muhasebe
# from administrator.models import Yönetici
# from general.models import Duyuru
# from management.models import Etüt, Yoklama, Ödev
# from teacher.models import Öğretmen
# from student.models import Öğrenci

# --- To get all models  ---
from django.apps import apps
models = apps.get_models()
liste = models

# To add specific models
# liste = [User, Muhasebe, Yönetici, Duyuru, Etüt, Yoklama, Öğretmen, Ödev, Öğrenci]


# ---- Admin panel for beskalem database ----
class BeskalemAdmin(admin.ModelAdmin):
    using = 'beskalem'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(BeskalemAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(BeskalemAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(BeskalemAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


beskalem = admin.AdminSite('beskalem')
for i in liste:
    beskalem.register(i, BeskalemAdmin)


# ---- Admin panel for iz database ----
class IzAdmin(admin.ModelAdmin):
    using = 'iz'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(IzAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(IzAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(IzAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


iz = admin.AdminSite('iz')
for i in liste:
    iz.register(i, IzAdmin)
