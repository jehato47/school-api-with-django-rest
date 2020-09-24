from django.contrib import admin
from djangorest.admins import beskalem, iz

# Register your models here.
from django.contrib.auth.models import User


class UserAdminBeskalem(admin.ModelAdmin):
    using = "beskalem"
    list_display = ["username", "first_name", "last_name", "id"]
    list_display_links = ["username"]
    list_filter = ["is_superuser", "is_staff", "is_active"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.set_password(obj.password)
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        User.objects.filter(id=obj.id).delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.using(self.using).delete()
        queryset.using("default").delete()

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(UserAdminBeskalem, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(UserAdminBeskalem, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(UserAdminBeskalem, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = User


class UserAdminIz(admin.ModelAdmin):
    using = "iz"
    list_display = ["username", "first_name", "last_name", "id"]
    list_display_links = ["username"]
    list_filter = ["is_superuser", "is_staff", "is_active"]

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.set_password(obj.password)
        obj.save()
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        User.objects.filter(id=obj.id).delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.using(self.using).delete()
        queryset.using("default").delete()

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(UserAdminIz, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(UserAdminIz, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(UserAdminIz, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    class Meta:
        model = User


beskalem.register(User, UserAdminBeskalem)
iz.register(User, UserAdminIz)
