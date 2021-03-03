from django.contrib import admin
from.models import OkulSınav, ExcelForm
from djangorest.admins import beskalem, iz, BeskalemAdmin, IzAdmin


class ExamAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["user", "sınıf", "şube"]
    list_display_links = ["user"]
    search_fields = ["sınıf", "şube"]
    list_filter = ["sınıf"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ExamAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ExamAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ExamAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = OkulSınav


class ExamAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["user", "sınıf", "şube"]
    list_display_links = ["user"]
    search_fields = ["sınıf", "şube"]
    list_filter = ["sınıf"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ExamAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ExamAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ExamAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = OkulSınav


class ExcelFileAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["file", "sınıf", "şube"]
    list_display_links = ["file", "sınıf"]
    # search_fields = ["file", "şube"]
    # list_filter = ["file"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ExcelFileAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ExcelFileAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ExcelFileAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = ExcelForm


beskalem.register(ExcelForm, ExcelFileAdminBeskalem)
beskalem.register(OkulSınav, ExamAdminBeskalem)
# beskalem.register(OkulSınav, BeskalemAdmin)
# iz.register(OkulSınav, IzAdmin)


class ExcelFileAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["file", "sınıf", "şube"]
    list_display_links = ["file", "sınıf"]
    # search_fields = ["file", "şube"]
    # list_filter = ["file"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ExcelFileAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(ExcelFileAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(ExcelFileAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = ExcelForm


iz.register(ExcelForm, ExcelFileAdminIz)
iz.register(OkulSınav, ExamAdminIz)
