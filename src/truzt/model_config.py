"""Module for defining the BaseConfigModel class."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class BaseConfigModel(BaseModel):
    """モデル全体の設定を定義する基底クラス."""

    model_config = ConfigDict(
        # PEP8のコーディング規約に従いクラス変数はsnake_caseで記述しているが
        # json serializeでby_alias=Trueとした時にはPascalCaseで出力する
        alias_generator=to_pascal,
        populate_by_name=True,
        # 未指定のフィールドを許可しない
        extra="forbid",
    )
