"""Stream type classes for tap-lucca-legacy."""

from __future__ import annotations

import sys
from typing import Any

from singer_sdk import typing as th, SchemaDirectory, StreamSchema
from singer_sdk.helpers.types import Context

from tap_lucca_legacy import schemas
from tap_lucca_legacy.client import LuccaLegacyStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

SCHEMAS_DIR = SchemaDirectory(schemas)

class EmployeesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "employees"
    path = "/api/v3/users"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    paginator_count_jsonpath = "data.count"
    stream_params={
        "orderBy": "id,asc",
        "formerEmployees": "true",
        "fields": ",".join([
            "id",
            "managerId",
            "manager",
            "departmentId",
            "legalEntityId",
            "name",
            "firstName",
            "lastName",
            "mail",
            "login",
            "employeeNumber",
            "civilTitle",
            "jobTitle",
            "dtContractStart",
            "dtContractEnd",
            "seniorityDate",
            "gender",
            "nationality",
            "externalId",
            "extendeddata",
            "attributes",
            "applicationData",

            "culture",
            "rolePrincipal",
            "habilitedRoles",
            "csp",
            "userWorkCycles",
            "userWorkCycles.id",
            "userWorkCycles.startsOn",
            "userWorkCycles.endsOn",
            "userWorkCycles.workCycle",
            "calendar",

            "userAxisValues",
            "modifiedAt",
            "collection.count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class LegalUnitsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "legal_units"
    path = "/organization/structure/api/legal-units"
    records_jsonpath = "$.items[*]"
    paginator = "page"
    paginator_count_jsonpath = "count"
    stream_params={
        "fields.root": ",".join([
            "count",
            "prev",
            "next",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class DepartmentsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "departments"
    path = "/api/v3/departments"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "code",
            "name",
            "hierarchy",
            "parentId",
            "isActive",
            "position",
            "level",
            "headID",
            "head",
            "collection.count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class WorkcyclesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "workcycles"
    path = "/api/v3/workcycles"
    records_jsonpath = "$.data.items[*]"
    paginator = None

    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "collection.count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class WorkContractsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "work_contracts"
    path = "/directory/api/4.0/work-contracts"
    records_jsonpath = "$.items[*]"
    paginator = "page"
    paginator_count_jsonpath = "count"
    stream_params={
        "fields.root": ",".join([
            "count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class EstablishmentsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "establishments"
    path = "/organization/structure/api/establishments"
    records_jsonpath = "$.items[*]"
    paginator = "page"
    paginator_count_jsonpath = "count"
    stream_params={
        "fields.root": ",".join([
            "count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class RolesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "roles"
    path = "/api/v3/roles"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    stream_params={}

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class CostCentersStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "cost_centers"
    path = "/api/v3/axes/4"
    records_jsonpath = "$.data.axisSections[*]"
    paginator = None
    stream_params={}

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class LocationsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "locations"
    path = "/api/v3/axes/7"
    records_jsonpath = "$.data.axisSections[*]"
    paginator = None
    stream_params={}

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserlogsDepartmentStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "userlogs_department"
    path = "/api/v3/userlogs"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    # paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "owner",
            "author",
            "modifiedAt",
            "modificationSource",
            "entryType",
            "value",
        ]),
        "name": "departmentid", # calendarid, legalentityid
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserlogsLegalentityStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "userlogs_legalentity"
    path = "/api/v3/userlogs"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    # paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "owner",
            "author",
            "modifiedAt",
            "modificationSource",
            "entryType",
            "value",
        ]),
        "name": "legalentityid", # calendarid, legalentityid
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserlogsCostcenterStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "userlogs_costcenter"
    path = "/api/v3/userlogs"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    # paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "owner",
            "author",
            "modifiedAt",
            "modificationSource",
            "entryType",
            "value",
        ]),
        "name": "userAxisValues_4",
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserlogsLocationStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "userlogs_location"
    path = "/api/v3/userlogs"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    # paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "owner",
            "author",
            "modifiedAt",
            "modificationSource",
            "entryType",
            "value",
        ]),
        "name": "userAxisValues_7",
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserlogsManagerStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "userlogs_manager"
    path = "/api/v3/userlogs"
    records_jsonpath = "$.data.items[*]"
    paginator = None
    # paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "name",
            "owner",
            "author",
            "modifiedAt",
            "modificationSource",
            "entryType",
            "value",
        ]),
        "name": "manager",
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class UserLocationsStream(LuccaLegacyStream):
    name = "user_locations"
    path = "/work-locations/public/api/user-locations"
    records_jsonpath = "$.items[*]"
    paginator = "page"
    default_page_size = 1000
    paginator_count_jsonpath = "count"
    stream_params={
        "fields.root": ",".join([
            "count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class WorkLocationsStream(LuccaLegacyStream):
    name = "work_locations"
    path = "/work-locations/public/api/work-locations"
    records_jsonpath = "$.items[*]"
    paginator = "page"
    paginator_count_jsonpath = "count"
    stream_params={
        "fields.root": ",".join([
            "count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class LeavesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "leaves"
    path = "/api/v3/leaves"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    default_page_size = 5000
    paginator_count_jsonpath = "data.count"
    stream_params={
        "date": "since,2000-01-01",
        "fields": ",".join([
            "id",
            "date",
            "isAM",
            "leaveAccountId",
            "leavePeriodId",
            "leaveAccount.id",
            "leaveAccount.name",
            "leavePeriod.id",
            "leavePeriod.ownerId",
            "leavePeriod.isConfirmed",
            "leavePeriod.confirmationDate",
            "leavePeriod.leaves.id",
            "leavePeriod.logs.id",
            "leavePeriod.logs.date",
            "leavePeriod.logs.status",
            "value",
            "creationDate",
            "isActive",
            "cancellationDate",
            "cancellationUserId",
            "collection.count",
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

    _legal_unit_ids: list[int] | None = None

    def _fetch_legal_unit_ids(self) -> list[int]:
        """Fetch all legal unit IDs from the legal-units endpoint."""
        if self._legal_unit_ids is None:
            legal_units_stream = LegalUnitsStream(self._tap)
            self._legal_unit_ids = [
                record["id"]
                for record in legal_units_stream.get_records(context=None)
            ]
            self.logger.info("Fetched %d legal unit IDs", len(self._legal_unit_ids))
        return self._legal_unit_ids

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        legal_unit_ids = self._fetch_legal_unit_ids()
        params["leavePeriod.owner.legalEntityId"] = ",".join(str(id) for id in legal_unit_ids)
        return params

class LeaveRequestsStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "leave_requests"
    path = "/api/v3/leaveRequests"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    default_page_size = 5000
    paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "leavePeriodId",
            "leavePeriod.id",
            "leavePeriod.ownerId",
            "leavePeriod.isConfirmed",
            "leavePeriod.confirmationDate",
            "leavePeriod.leaves.id",
            "leavePeriod.logs.id",
            "leavePeriod.logs.date",
            "leavePeriod.logs.status",
            "status",
            "creationDate",
            "nextApproverId",
            "cancellationUserId",
            "cancellationDate",
            "isActive",
            "approvals.id",
            "approvals.date",
            "approvals.approverId",
            "approvals.substitutedApproverId",
            "approvals.approved",
            "cancellationRequests.id",
            "cancellationRequests.authorId",
            "cancellationRequests.rank",
            "cancellationRequests.creationDate",
            "cancellationRequests.nextApproverId",
            "cancellationRequests.isActive",
            "collection.count"
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

class SickLeaveCertificatesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "sick_leave_certificates"
    path = "/api/v3/sickLeaveCertificates"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    default_page_size = 5000
    paginator_count_jsonpath = "data.count"
    stream_params={
        "fields": ",".join([
            "id",
            "leavePeriodId",
            "leaveAccountId",
            "authorId",
            "creationDate",
            "isActive",
            "cancellationDate",
            "cancellationUserId",
            "partTimeNature",
            "partTimeActivityRate",
            "partTimeReturnType",
            "extension",
            "originalLeavePeriodId",
            "collection.count"
        ])
    }

    primary_keys = ("id",)
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)
