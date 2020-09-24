from django.contrib import admin
from djangorest.admins import beskalem, iz, BeskalemAdmin
from .models import Duyuru
# todo : model admin save_on_top = True oldu
# todo : User modelindeki emailfield charfield oldu


class DuyuruAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["oluşturan", "içerik", "tarih", "dosya"]
    list_display_links = ["oluşturan"]
    search_fields = ["oluşturan", "içerik"]
    list_filter = ["tarih"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(DuyuruAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(DuyuruAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(DuyuruAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Duyuru


class DuyuruAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["oluşturan", "içerik", "tarih", "dosya"]
    list_display_links = ["oluşturan"]
    search_fields = ["oluşturan", "içerik"]
    list_filter = ["tarih"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(DuyuruAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(DuyuruAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(DuyuruAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Duyuru


iz.register(Duyuru, DuyuruAdminIz)
beskalem.register(Duyuru, DuyuruAdminBeskalem)
