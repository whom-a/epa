# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from epa_api.models.status import Status


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def get_status(
        self,
    ) -> Status:
        ...
