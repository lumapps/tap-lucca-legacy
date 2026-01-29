"""Stream type classes for tap-lucca-legacy."""

from __future__ import annotations

from singer_sdk import typing as th, SchemaDirectory, StreamSchema

from tap_lucca_legacy import schemas
from tap_lucca_legacy.client import LuccaLegacyStream

SCHEMAS_DIR = SchemaDirectory(schemas)

class EmployeesStream(LuccaLegacyStream):
    """Define custom stream."""

    name = "employees"
    path = "/api/v3/users"
    records_jsonpath = "$.data.items[*]"
    paginator = "offset"
    paginator_count_jsonpath = "data.count"
    stream_params={
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
