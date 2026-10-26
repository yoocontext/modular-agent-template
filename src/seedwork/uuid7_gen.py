from uuid import UUID

from uuid_utils import uuid7


def uuid7_factory() -> UUID:
    return UUID(str(uuid7()))
