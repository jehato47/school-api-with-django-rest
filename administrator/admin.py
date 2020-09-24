from django.contrib import admin
from .models import Yönetici
from djangorest.admins import beskalem, iz
# Register your models here.


@admin.register(Yönetici)
class YöneticiAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["isim", "soyisim", "mevki", "email"]
    list_display_links = ["isim"]
    search_fields = ["isim"]
    list_filter = ["mevki"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(YöneticiAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(YöneticiAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(YöneticiAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Yönetici


class YöneticiAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["isim", "soyisim", "mevki", "email"]
    list_display_links = ["isim"]
    search_fields = ["isim"]
    list_filter = ["mevki"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(YöneticiAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(YöneticiAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(YöneticiAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Yönetici


beskalem.register(Yönetici, YöneticiAdminBeskalem)
iz.register(Yönetici, YöneticiAdminIz)
