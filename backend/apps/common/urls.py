from django.urls import include, path

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("", include("apps.tenants.urls")),
    path("", include("apps.customers.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.subscriptions.urls")),
    path("", include("apps.usage.urls")),
    path("", include("apps.invoicing.urls")),
    path("pay/", include("apps.payments.urls")),
    path("", include("apps.dunning.urls")),
    path("", include("apps.contracts.urls")),
    path("", include("apps.revenue.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.audit.urls")),
    path("", include("apps.search.urls")),
    path("", include("apps.reports.urls")),
    path("", include("apps.entitlements.urls")),
    path("", include("apps.integrations.urls")),
    path("", include("apps.forecasts.urls")),
    path("", include("apps.commissions.urls")),
]
