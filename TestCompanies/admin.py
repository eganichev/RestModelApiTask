from django.contrib import admin

# Register your models here.
from TestCompanies.models import Company, Office

admin.site.register(Company)
admin.site.register(Office)
