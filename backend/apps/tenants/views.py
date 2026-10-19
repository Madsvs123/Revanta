from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Membership
from apps.common.mixins import TenantQuerysetMixin
from apps.tenants.models import (
    BillingEntity,
    BusinessUnit,
    Currency,
    FinancialControl,
    Organization,
    OrganizationSetting,
    TaxRegion,
)
from apps.tenants.serializers import (
    BillingEntitySerializer,
    BusinessUnitSerializer,
    CurrencySerializer,
    FinancialControlSerializer,
    OrganizationSerializer,
    OrganizationSettingSerializer,
    TaxRegionSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    allow_unscoped = True
    required_permission = "org.manage"

    def get_queryset(self):
        return Organization.objects.all()

    def get_permissions(self):
        if self.action in ("list", "retrieve", "switch"):
            self.required_permission = None
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def switch(self, request, pk=None):
        organization = self.get_object()
        membership = Membership.objects.filter(user=request.user, organization=organization, is_active=True).first()
        if membership:
            return Response({"detail": "Not a member."}, status=403)
        request.user.last_organization = organization
        request.user.save(update_fields=["last_organization"])
        return Response(OrganizationSerializer(organization).data)


class BusinessUnitViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    resource_name = "settings"


class BillingEntityViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = BillingEntity.objects.all()
    serializer_class = BillingEntitySerializer
    resource_name = "settings"


class CurrencyViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    resource_name = "settings"


class TaxRegionViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = TaxRegion.objects.all()
    serializer_class = TaxRegionSerializer
    resource_name = "settings"


class SettingsView(APIView):
    resource_name = "settings"

    def get(self, request):
        controls, _ = FinancialControl.objects.get_or_create(organization=request.organization)
        settings, _ = OrganizationSetting.objects.get_or_create(organization=request.organization)
        return Response(
            {
                "organization": OrganizationSerializer(request.organization).data,
                "controls": FinancialControlSerializer(controls).data,
                "settings": OrganizationSettingSerializer(settings).data,
                "currencies": CurrencySerializer(Currency.objects.filter(organization=request.organization), many=True).data,
                "tax_regions": TaxRegionSerializer(TaxRegion.objects.filter(organization=request.organization), many=True).data,
                "business_units": BusinessUnitSerializer(
                    BusinessUnit.objects.filter(organization=request.organization), many=True
                ).data,
                "billing_entities": BillingEntitySerializer(
                    BillingEntity.objects.filter(organization=request.organization), many=True
                ).data,
            }
        )

    def patch(self, request):
        if "organization" in request.data:
            org = OrganizationSerializer(request.organization, data=request.data["organization"], partial=True)
            org.is_valid(raise_exception=True)
            org.save()
        if "controls" in request.data:
            controls, _ = FinancialControl.objects.get_or_create(organization=request.organization)
            ser = FinancialControlSerializer(controls, data=request.data["controls"], partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
        if "settings" in request.data:
            settings, _ = OrganizationSetting.objects.get_or_create(organization=request.organization)
            ser = OrganizationSettingSerializer(settings, data=request.data["settings"], partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
        return self.get(request)
