from django.contrib import admin

from .models import Cafe, Comment, Profile

class CafeAdmin(admin.ModelAdmin):
	class Meta:
		model=Cafe

admin.site.register(Cafe, CafeAdmin)	

class CommentAdmin(admin.ModelAdmin):
	class Meta:
		model=Comment

admin.site.register(Comment, CommentAdmin)	

class profileAdmin(admin.ModelAdmin):
	class Meta:
		model=Profile

admin.site.register(Profile, profileAdmin)	


