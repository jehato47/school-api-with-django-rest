from django.contrib import admin
from .models import Muhasebe
from djangorest.admins import beskalem, iz

# Register your models here.


class MuhasebeAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["user", "taksit_adedi"]
    list_display_links = ["user"]
    search_fields = ["user"]
    list_filter = ["user"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MuhasebeAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MuhasebeAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MuhasebeAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Muhasebe


class MuhasebeAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["user", "taksit_adedi"]
    list_display_links = ["user"]
    search_fields = ["user"]
    list_filter = ["user"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MuhasebeAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MuhasebeAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MuhasebeAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = Muhasebe


beskalem.register(Muhasebe, MuhasebeAdminBeskalem)
iz.register(Muhasebe, MuhasebeAdminIz)
