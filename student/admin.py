from django.contrib import admin
from .models import Öğrenci, ÖğrencidProgramı
from djangorest.admins import beskalem, iz
# Register your models here.


class ÖğrenciAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["user", "user_id", "isim", "soyisim", "no", "sınıf", "şube"]
    list_display_links = ["user", "user_id"]
    search_fields = ["isim", "soyisim"]
    list_filter = ["sınıf", "isim", "soyisim"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete()
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖğrenciAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖğrenciAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖğrenciAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Öğrenci


class ÖğrenciAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["user", "user_id", "isim", "soyisim", "no", "sınıf", "şube"]
    list_display_links = ["user", "user_id"]
    search_fields = ["isim", "soyisim"]
    list_filter = ["sınıf", "isim", "soyisim"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete()
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖğrenciAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖğrenciAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖğrenciAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Öğrenci


class ÖğrencidProgramıAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["sınıf", "date"]
    list_display_links = ["sınıf"]
    search_fields = ["sınıf"]
    list_filter = ["date"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete()
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖğrencidProgramıAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖğrencidProgramıAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖğrencidProgramıAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = ÖğrencidProgramı


class ÖğrencidProgramıAdminIz(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["sınıf", "date"]
    list_display_links = ["sınıf"]
    search_fields = ["sınıf"]
    list_filter = ["date"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete()
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ÖğrencidProgramıAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ÖğrencidProgramıAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ÖğrencidProgramıAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = ÖğrencidProgramı


beskalem.register(Öğrenci, ÖğrenciAdminBeskalem)
beskalem.register(ÖğrencidProgramı, ÖğrencidProgramıAdminBeskalem)
iz.register(Öğrenci, ÖğrenciAdminIz)
iz.register(ÖğrencidProgramı, ÖğrencidProgramıAdminIz)
