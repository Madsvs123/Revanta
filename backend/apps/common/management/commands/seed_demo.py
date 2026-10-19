from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import InvestigatorProfile, Membership, Role, StudyAccess, User
from apps.documents.models import Document
from apps.finance.models import Expense, Grant, Invoice, Payment, StudyBudget
from apps.issues.models import CorrectiveAction, Issue, ProtocolDeviation
from apps.monitoring.models import ActionItem, Finding, MonitoringVisit, RiskIndicator, TripReport
from apps.notifications.models import Notification
from apps.participants.models import Participant, RandomizationRecord, ScreeningRecord, Withdrawal
from apps.qualifications.models import StaffCredential, TrainingRecord
from apps.sites.models import FeasibilityAssessment, Site, SiteContact, SiteContract, SiteMetric, StudySite
from apps.studies.models import (
    CustomField,
    Protocol,
    StatusWorkflow,
    Study,
    StudyCountry,
    StudyMilestone,
    StudyObjective,
    StudyTeamMember,
    StudyTemplate,
)
from apps.tenants.models import Country, Department, Organization, OrganizationSetting, Sponsor
from apps.visits.models import Visit, VisitAssessment, VisitDefinition, VisitFollowUp
from apps.workitems.models import Task, TaskComment


class Command(BaseCommand):
    help = "Seed a complete Trialora demonstration workspace"

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            slug="northwind-research",
            defaults={
                "name": "Northwind Research Network",
                "org_type": Organization.OrgType.CRO,
                "legal_name": "Northwind Research Network, LLC",
                "country": "United States",
                "timezone": "America/New_York",
                "website": "https://northwind.example",
            },
        )
        OrganizationSetting.objects.get_or_create(organization=org)
        Role.ensure_defaults(org)
        owner_role = Role.objects.get(organization=org, slug="owner")
        inv_role = Role.objects.get(organization=org, slug="investigator")
        coord_role = Role.objects.get(organization=org, slug="coordinator")
        monitor_role = Role.objects.get(organization=org, slug="monitor")

        admin, created = User.objects.get_or_create(
            email="admin@northwind.research",
            defaults={
                "username": "admin@northwind.research",
                "display_name": "Amelia Hart",
                "first_name": "Amelia",
                "last_name": "Hart",
                "title": "Head of Clinical Operations",
                "last_organization": org,
            },
        )
        if created:
            admin.set_password("Trialora!2026")
            admin.save()
        Membership.objects.get_or_create(organization=org, user=admin, defaults={"role": owner_role, "title": "Operations lead"})

        investigator, icreated = User.objects.get_or_create(
            email="pi@northwind.research",
            defaults={
                "username": "pi@northwind.research",
                "display_name": "Dr. Elias Voss",
                "first_name": "Elias",
                "last_name": "Voss",
                "is_investigator": True,
                "title": "Principal Investigator",
                "last_organization": org,
            },
        )
        if icreated:
            investigator.set_password("Trialora!2026")
            investigator.save()
        Membership.objects.get_or_create(organization=org, user=investigator, defaults={"role": inv_role, "title": "PI"})
        InvestigatorProfile.objects.get_or_create(
            organization=org,
            user=investigator,
            defaults={
                "specialty": "Oncology",
                "institution": "Harborview Academic Medical Center",
                "gcp_certified": True,
                "years_experience": 14,
                "medical_license": "MD-44821",
            },
        )

        coordinator, ccreated = User.objects.get_or_create(
            email="crc@northwind.research",
            defaults={
                "username": "crc@northwind.research",
                "display_name": "Priya Raman",
                "first_name": "Priya",
                "last_name": "Raman",
                "title": "Study Coordinator",
                "last_organization": org,
            },
        )
        if ccreated:
            coordinator.set_password("Trialora!2026")
            coordinator.save()
        Membership.objects.get_or_create(organization=org, user=coordinator, defaults={"role": coord_role, "title": "CRC"})

        monitor, mcreated = User.objects.get_or_create(
            email="cra@northwind.research",
            defaults={
                "username": "cra@northwind.research",
                "display_name": "Jonah Hale",
                "first_name": "Jonah",
                "last_name": "Hale",
                "title": "Clinical Research Associate",
                "last_organization": org,
            },
        )
        if mcreated:
            monitor.set_password("Trialora!2026")
            monitor.save()
        Membership.objects.get_or_create(organization=org, user=monitor, defaults={"role": monitor_role, "title": "CRA"})

        countries = [
            ("US", "United States", "North America"),
            ("GB", "United Kingdom", "Europe"),
            ("DE", "Germany", "Europe"),
            ("JP", "Japan", "Asia"),
            ("CA", "Canada", "North America"),
        ]
        country_map = {}
        for code, name, region in countries:
            country_map[code], _ = Country.objects.get_or_create(code=code, defaults={"name": name, "region": region})

        oncology, _ = Department.objects.get_or_create(organization=org, name="Oncology", defaults={"code": "ONC"})
        cardio, _ = Department.objects.get_or_create(organization=org, name="Cardiology", defaults={"code": "CRD"})
        sponsor, _ = Sponsor.objects.get_or_create(
            organization=org,
            name="Lumen Therapeutics",
            defaults={"code": "LUM", "country": "United States", "contact_email": "trials@lumen.example"},
        )

        template, _ = StudyTemplate.objects.get_or_create(
            organization=org,
            name="Oncology Phase II starter",
            defaults={
                "phase": "II",
                "therapeutic_area": "Oncology",
                "default_milestones": [{"name": "Protocol approved"}, {"name": "FPI"}, {"name": "LPI"}, {"name": "Database lock"}],
                "default_visits": [
                    {"code": "SCR", "name": "Screening", "window_start_days": -14, "window_end_days": 0},
                    {"code": "C1D1", "name": "Cycle 1 Day 1", "window_start_days": 0, "window_end_days": 3},
                    {"code": "EOT", "name": "End of treatment"},
                ],
                "default_objectives": [{"kind": "primary", "text": "Overall response rate"}],
            },
        )
        CustomField.objects.get_or_create(
            organization=org,
            entity_type="study",
            field_key="biomarker",
            defaults={"name": "Biomarker strategy", "field_type": "text"},
        )
        StatusWorkflow.objects.get_or_create(
            organization=org,
            entity_type="study",
            name="Study lifecycle",
            defaults={
                "states": ["draft", "startup", "enrolling", "active", "follow_up", "closed"],
                "transitions": [["draft", "startup"], ["startup", "enrolling"], ["enrolling", "active"]],
                "is_default": True,
            },
        )

        study, _ = Study.objects.get_or_create(
            organization=org,
            code="LUM-ONC-204",
            defaults={
                "title": "A randomized study of lumetinib in previously treated NSCLC",
                "protocol_number": "LUM-204-01",
                "acronym": "LUMEN-NSCLC",
                "phase": Study.Phase.II,
                "therapeutic_area": "Oncology",
                "indication": "Non-small cell lung cancer",
                "status": Study.Status.ENROLLING,
                "sponsor": sponsor,
                "department": oncology,
                "enrollment_target": 180,
                "screening_target": 260,
                "start_date": date(2025, 9, 1),
                "first_patient_in": date(2025, 11, 12),
                "nct_id": "NCT05912044",
                "description": "Multicenter Phase II study evaluating lumetinib plus standard of care versus standard of care alone.",
            },
        )
        cardio_study, _ = Study.objects.get_or_create(
            organization=org,
            code="LUM-CRD-118",
            defaults={
                "title": "Heart-sparing imaging biomarker study in HFpEF",
                "protocol_number": "LUM-118-02",
                "phase": Study.Phase.I_II,
                "therapeutic_area": "Cardiology",
                "indication": "HFpEF",
                "status": Study.Status.STARTUP,
                "sponsor": sponsor,
                "department": cardio,
                "enrollment_target": 60,
                "start_date": date(2026, 4, 1),
            },
        )

        Protocol.objects.get_or_create(
            organization=org,
            study=study,
            version="3.0",
            defaults={"title": "Lumetinib NSCLC protocol", "is_current": True, "effective_date": date(2026, 1, 15)},
        )
        for seq, name, status in [
            (1, "Protocol approved", "complete"),
            (2, "First site activated", "complete"),
            (3, "First patient in", "complete"),
            (4, "50% enrollment", "in_progress"),
            (5, "Last patient in", "planned"),
        ]:
            StudyMilestone.objects.get_or_create(organization=org, study=study, name=name, defaults={"sequence": seq, "status": status, "due_date": date(2026, 3, 1) + timedelta(days=seq * 40)})
        StudyObjective.objects.get_or_create(organization=org, study=study, text="Confirm overall response rate versus control", defaults={"kind": "primary"})
        StudyObjective.objects.get_or_create(organization=org, study=study, text="Evaluate progression-free survival", defaults={"kind": "secondary"})
        StudyCountry.objects.get_or_create(organization=org, study=study, country=country_map["US"], defaults={"enrollment_target": 110})
        StudyCountry.objects.get_or_create(organization=org, study=study, country=country_map["GB"], defaults={"enrollment_target": 40})
        StudyTeamMember.objects.get_or_create(organization=org, study=study, user=admin, role_label="Study manager", defaults={"is_lead": True})
        StudyTeamMember.objects.get_or_create(organization=org, study=study, user=monitor, role_label="Lead CRA")

        harbor, _ = Site.objects.get_or_create(
            organization=org,
            name="Harborview Academic Medical Center",
            defaults={"institution": "Harborview", "city": "Boston", "country": country_map["US"], "principal_investigator": investigator, "email": "trials@harborview.example"},
        )
        riverside, _ = Site.objects.get_or_create(
            organization=org,
            name="Riverside Cancer Institute",
            defaults={"institution": "Riverside", "city": "Chicago", "country": country_map["US"]},
        )
        SiteContact.objects.get_or_create(organization=org, site=harbor, name="Priya Raman", defaults={"role": "CRC", "email": "crc@northwind.research", "is_primary": True})

        ss1, _ = StudySite.objects.get_or_create(
            organization=org,
            study=study,
            site=harbor,
            defaults={"status": StudySite.Status.ENROLLING, "activation_date": date(2025, 10, 20), "enrollment_target": 40, "investigator": investigator, "monitoring_status": "elevated"},
        )
        ss2, _ = StudySite.objects.get_or_create(
            organization=org,
            study=study,
            site=riverside,
            defaults={"status": StudySite.Status.ACTIVATING, "enrollment_target": 28, "contract_status": "executed"},
        )
        FeasibilityAssessment.objects.get_or_create(organization=org, study=study, study_site=ss1, defaults={"status": "complete", "score": 8.6, "population_fit": 9, "staff_readiness": 8, "completed_at": date(2025, 8, 12)})
        SiteContract.objects.get_or_create(organization=org, study=study, study_site=ss1, title="Harborview CTA", defaults={"status": "executed", "value": 420000, "executed_at": date(2025, 9, 30)})
        SiteMetric.objects.get_or_create(organization=org, study=study, study_site=ss1, defaults={"screened": 38, "enrolled": 22, "screen_failed": 9, "withdrawn": 2, "completed": 4, "open_findings": 3, "enrollment_pace": 55})

        StudyAccess.objects.get_or_create(organization=org, user=investigator, study=study, defaults={"role": inv_role, "can_view_pii": True})
        StudyAccess.objects.get_or_create(organization=org, user=coordinator, study=study, defaults={"role": coord_role, "can_view_pii": True})
        StudyAccess.objects.get_or_create(organization=org, user=monitor, study=study, defaults={"role": monitor_role, "can_view_pii": False})
        StudyAccess.objects.get_or_create(organization=org, user=admin, study=study, defaults={"role": owner_role, "can_view_pii": True})
        StudyAccess.objects.get_or_create(organization=org, user=admin, study=cardio_study, defaults={"role": owner_role, "can_view_pii": True})

        defs = []
        for seq, code, name, start, end in [
            (1, "SCR", "Screening", -14, 0),
            (2, "C1D1", "Cycle 1 Day 1", 0, 3),
            (3, "C2D1", "Cycle 2 Day 1", 18, 24),
            (4, "EOT", "End of treatment", 0, 7),
        ]:
            item, _ = VisitDefinition.objects.get_or_create(organization=org, study=study, code=code, defaults={"name": name, "sequence": seq, "window_start_days": start, "window_end_days": end})
            defs.append(item)

        statuses = ["screening", "screen_failed", "enrolled", "randomized", "active", "withdrawn", "completed"]
        for i in range(1, 25):
            status = statuses[i % len(statuses)]
            subject = f"204-{i:03d}"
            participant, _ = Participant.objects.get_or_create(
                organization=org,
                study=study,
                subject_id=subject,
                defaults={
                    "study_site": ss1 if i % 3 else ss2,
                    "screening_number": f"S{i:03d}",
                    "status": status,
                    "eligibility_status": "eligible" if status not in ("screen_failed", "prescreen") else "ineligible",
                    "screened_on": date(2026, 1, 2) + timedelta(days=i),
                    "enrolled_on": date(2026, 1, 10) + timedelta(days=i) if status not in ("screening", "screen_failed") else None,
                    "first_name": f"Subject{i}",
                    "last_name": "Rivera",
                    "date_of_birth": date(1968, 4, min(28, i)),
                    "sex": "F" if i % 2 else "M",
                    "email": f"subject{i}@example.com",
                },
            )
            ScreeningRecord.objects.get_or_create(
                organization=org,
                study=study,
                participant=participant,
                screened_on=participant.screened_on or date(2026, 1, 2),
                defaults={"result": "failed" if status == "screen_failed" else "passed", "inclusion_met": status != "screen_failed"},
            )
            if status in ("randomized", "active", "completed"):
                RandomizationRecord.objects.get_or_create(
                    organization=org,
                    study=study,
                    participant=participant,
                    defaults={"arm": "lumetinib" if i % 2 else "control", "randomized_on": date(2026, 1, 12), "kit_number": f"KIT-{i:04d}"},
                )
            if status == "withdrawn":
                Withdrawal.objects.get_or_create(organization=org, study=study, participant=participant, defaults={"withdrawn_on": date(2026, 3, 1), "reason": "Consent withdrawn"})
            visit, _ = Visit.objects.get_or_create(
                organization=org,
                study=study,
                participant=participant,
                name="Cycle 1 Day 1",
                defaults={
                    "definition": defs[1],
                    "study_site": participant.study_site,
                    "scheduled_date": date(2026, 2, 1) + timedelta(days=i),
                    "window_start": date(2026, 1, 29) + timedelta(days=i),
                    "window_end": date(2026, 2, 4) + timedelta(days=i),
                    "status": "completed" if i < 10 else ("overdue" if i > 20 else "scheduled"),
                    "actual_date": date(2026, 2, 1) + timedelta(days=i) if i < 10 else None,
                },
            )
            VisitAssessment.objects.get_or_create(organization=org, study=study, visit=visit, name="ECOG", defaults={"status": "complete" if i < 10 else "pending", "form_code": "ECOG"})
            if i > 20:
                VisitFollowUp.objects.get_or_create(organization=org, study=study, visit=visit, due_date=date(2026, 4, 1), defaults={"reason": "Reschedule missed cycle visit", "status": "open"})

        mv, _ = MonitoringVisit.objects.get_or_create(
            organization=org,
            study=study,
            study_site=ss1,
            scheduled_date=date(2026, 3, 18),
            defaults={"monitor": monitor, "kind": MonitoringVisit.Kind.IMV, "status": "completed", "actual_date": date(2026, 3, 18)},
        )
        TripReport.objects.get_or_create(organization=org, study=study, monitoring_visit=mv, defaults={"summary": "Source data review complete. Two consent version findings.", "status": "submitted", "submitted_at": timezone.now()})
        finding, _ = Finding.objects.get_or_create(organization=org, study=study, monitoring_visit=mv, title="Consent version lag", defaults={"severity": "major", "status": "open", "category": "ICF", "due_date": date(2026, 4, 15), "owner": coordinator})
        ActionItem.objects.get_or_create(organization=org, study=study, finding=finding, title="Reconsent remaining subjects", defaults={"status": "open", "due_date": date(2026, 4, 10), "owner": coordinator})
        RiskIndicator.objects.get_or_create(organization=org, study=study, study_site=ss1, name="Consent process", defaults={"score": 7.2, "trend": "up"})

        issue, _ = Issue.objects.get_or_create(
            organization=org,
            study=study,
            title="Visit window deviation on C2D1",
            defaults={"kind": "deviation", "severity": "medium", "status": "open", "category": "visit_window", "study_site": ss1, "owner": coordinator, "due_date": date(2026, 4, 20), "root_cause": "Holiday clinic closure"},
        )
        ProtocolDeviation.objects.get_or_create(organization=org, study=study, issue=issue, defaults={"is_important": False, "protocol_section": "6.2"})
        CorrectiveAction.objects.get_or_create(organization=org, study=study, issue=issue, defaults={"description": "Add holiday coverage calendar to visit planning", "status": "open", "due_date": date(2026, 4, 25)})

        Document.objects.get_or_create(organization=org, study=study, title="Protocol v3.0", defaults={"category": "protocol", "status": "current"})
        Document.objects.get_or_create(organization=org, site=harbor, title="Harborview IRB approval", defaults={"category": "approval", "expires_at": date(2026, 11, 1)})
        Document.objects.get_or_create(organization=org, study=study, title="ICF version 5", defaults={"category": "consent", "status": "current"})

        StaffCredential.objects.get_or_create(organization=org, user=investigator, name="Medical license", defaults={"kind": "license", "expires_on": date(2027, 6, 1), "status": "valid"})
        StaffCredential.objects.get_or_create(organization=org, user=coordinator, name="GCP certificate", defaults={"kind": "gcp", "expires_on": date(2026, 5, 20), "status": "valid"})
        TrainingRecord.objects.get_or_create(organization=org, user=coordinator, study=study, course="Protocol 3.0 amendment training", defaults={"status": "assigned", "due_date": date(2026, 4, 8), "required": True})

        task, _ = Task.objects.get_or_create(organization=org, study=study, title="Activate Riverside pharmacy", defaults={"priority": "high", "status": "open", "assignee": admin, "due_date": date(2026, 4, 12), "study_site": ss2})
        TaskComment.objects.get_or_create(organization=org, task=task, author=admin, defaults={"body": "Awaiting controlled-substance license scan."})

        StudyBudget.objects.get_or_create(organization=org, study=study, category="Site payments", defaults={"planned": 1200000, "actual": 410000})
        StudyBudget.objects.get_or_create(organization=org, study=study, category="Monitoring", defaults={"planned": 280000, "actual": 96000})
        Payment.objects.get_or_create(organization=org, study=study, title="Harborview startup", defaults={"kind": "site", "amount": 35000, "status": "paid", "study_site": ss1, "paid_on": date(2025, 11, 1)})
        Payment.objects.get_or_create(organization=org, study=study, title="Investigator Q1", defaults={"kind": "investigator", "amount": 12500, "status": "scheduled", "due_date": date(2026, 4, 30), "investigator": investigator})
        Invoice.objects.get_or_create(organization=org, study=study, number="INV-204-018", defaults={"amount": 12500, "status": "issued", "issued_on": date(2026, 3, 15)})
        Expense.objects.get_or_create(organization=org, study=study, category="Travel", defaults={"amount": 1840, "incurred_on": date(2026, 3, 18), "vendor": "Northline Air"})
        Grant.objects.get_or_create(organization=org, study=study, source="Lumen Therapeutics", defaults={"amount": 4800000, "status": "active", "awarded_on": date(2025, 6, 1)})

        Notification.objects.get_or_create(organization=org, user=admin, title="Harborview reached 50% enrollment", defaults={"kind": "enrollment", "body": "22 of 40 subjects enrolled.", "link": "/app/enrollment"})
        Notification.objects.get_or_create(organization=org, user=admin, title="GCP certificate expiring", defaults={"kind": "training", "body": "Priya Raman GCP expires 20 May 2026.", "link": "/app/staff"})

        self.stdout.write(self.style.SUCCESS("Seeded Northwind Research Network. Login admin@northwind.research / Trialora!2026"))
