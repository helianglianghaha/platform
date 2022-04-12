from django.contrib import admin
# from .models import PostList,Project,Version,Version_Bug,Version_Bug_Analysis,Version_Code,Version_delay,Version_engineer,Version_release

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','pub_date')
# admin.site.register(PostList,PostAdmin)
# admin.site.register(NewTable)
# admin.site.register(Product)
# admin.site.register(Hfs_Bug)
# admin.site.register(Zsk_Bug)
# admin.site.register(Slw_Bug)
# admin.site.register(Project)
# admin.site.register(Version)
# admin.site.register(Version_Bug)
# admin.site.register(Version_Bug_Analysis)
# admin.site.register(Version_Code)
# admin.site.register(Version_delay)
# admin.site.register(Version_engineer)
# admin.site.register(Version_release)