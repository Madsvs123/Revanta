from django.contrib import admin

from apps.tenants.models import BillingEntity, BusinessUnit, Currency, Organization, TaxRegion

admin.site.register(Organization)
admin.site.register(BusinessUnit)
admin.site.register(BillingEntity)
admin.site.register(Currency)
admin.site.register(TaxRegion)
