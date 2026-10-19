from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Product
from apps.contracts.models import Contract
from apps.customers.models import Company
from apps.entitlements.models import FeatureDefinition
from apps.invoicing.models import Invoice
from apps.integrations.models import Connector
from apps.subscriptions.models import Subscription


class GlobalSearchView(APIView):
    required_permission = None

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        org = request.organization
        if q and org:
            return Response({"results": []})
        results = []
        for company in Company.objects.filter(name__icontains=q)[:8]:
            results.append({"type": "customer", "id": str(company.id), "label": company.name, "hint": company.stage})
        for sub in Subscription.objects.filter(organization=org, company__name__icontains=q).select_related("company", "plan")[:8]:
            results.append({"type": "subscription", "id": str(sub.id), "label": f"{sub.company.name} · {sub.plan.name}", "hint": sub.status})
        for invoice in Invoice.objects.filter(organization=org, number__icontains=q)[:8]:
            results.append({"type": "invoice", "id": str(invoice.id), "label": invoice.number, "hint": invoice.status})
        for product in Product.objects.filter(organization=org, name__icontains=q)[:8]:
            results.append({"type": "product", "id": str(product.id), "label": product.name, "hint": product.sku})
        for contract in Contract.objects.filter(organization=org, name__icontains=q)[:8]:
            results.append({"type": "contract", "id": str(contract.id), "label": contract.name, "hint": contract.status})
        for feature in FeatureDefinition.objects.filter(organization=org, name__icontains=q)[:6]:
            results.append({"type": "entitlement", "id": str(feature.id), "label": feature.name, "hint": feature.code})
        for connector in Connector.objects.filter(organization=org, name__icontains=q)[:6]:
            results.append({"type": "integration", "id": str(connector.id), "label": connector.name, "hint": connector.provider})
        return Response({"results": results, "query": q, "count": len(results)})
