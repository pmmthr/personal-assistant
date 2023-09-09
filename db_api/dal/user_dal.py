from typing import Type

from db_api.dal.base_dal import BaseDAL
from db_api.model import Users


class UserDAL(BaseDAL):

    _model: Type = Users