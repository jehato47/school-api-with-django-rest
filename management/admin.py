from django.contrib import admin
from .models import Ödev, Etüt, Yoklama
from djangorest.admins import beskalem, iz
# Register your models here.


# >----- Beskalem Management Admin Models -----<
class EtütAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["öğretmen", "ders"]
    list_display_links = ["öğretmen"]
    list_filter = ["ders"]
    search_fields = ["öğretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(EtütAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(EtütAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(EtütAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Etüt


class ÖdevAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["baslik", "ogretmen", "sinif", "baslangic_tarihi"]
    list_display_links = ["baslik"]
    list_filter = ["sinif", "ogretmen"]
    search_fields = ["icerik", "ogretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖdevAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖdevAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖdevAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Ödev


class YoklamaAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["öğretmen", "ders", "derssaati", "date", "sınıf", "gelenler", "gelmeyenler", "izinliler", "geç_gelenler"]
    list_display_links = ["öğretmen", "derssaati"]
    list_filter = ["ders", "date"]
    search_fields = ["ders", "öğretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(YoklamaAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(YoklamaAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(YoklamaAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Yoklama


# >----- Registiration of models to beskalem admin -----<
beskalem.register(Etüt, EtütAdminBeskalem)
beskalem.register(Ödev, ÖdevAdminBeskalem)
beskalem.register(Yoklama, YoklamaAdminBeskalem)


# >----- Iz Admin Management Models -----<
class EtütAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["öğretmen", "ders"]
    list_display_links = ["öğretmen"]
    list_filter = ["ders"]
    search_fields = ["öğretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(EtütAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(EtütAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(EtütAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Etüt


class ÖdevAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["baslik", "ogretmen", "sinif", "baslangic_tarihi"]
    list_display_links = ["baslik"]
    list_filter = ["sinif", "ogretmen"]
    search_fields = ["icerik", "ogretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖdevAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖdevAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖdevAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Ödev


class YoklamaAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["öğretmen", "ders", "derssaati", "date", "sınıf", "gelenler", "gelmeyenler", "izinliler", "geç_gelenler"]
    list_display_links = ["öğretmen", "derssaati"]
    list_filter = ["ders", "date"]
    search_fields = ["ders", "öğretmen"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(YoklamaAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(YoklamaAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(YoklamaAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Yoklama


# >----- Registiration of models to iz admin -----<
iz.register(Etüt, EtütAdminIz)
iz.register(Ödev, ÖdevAdminIz)
iz.register(Yoklama, YoklamaAdminIz)
