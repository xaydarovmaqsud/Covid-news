from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(New)
admin.site.register(Author)
admin.site.register(Person)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Category)