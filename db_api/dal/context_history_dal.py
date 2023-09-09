from typing import Type

from db_api.dal.base_dal import BaseDAL
from db_api.model import Context


class ContextDAL(BaseDAL):

    _model: Type = Context