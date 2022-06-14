import re
from typing import Any, Dict
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
import yaml
from pydoc import locate

alnum_regex = re.compile(r"^[a-zA-Z0-9_]+$")


@extensions.register_check_method(check_type="element_wise")
def isalnum_(pandas_obj):
    """文字列が英数字アンダースコアのみで構成されているか"""
    return alnum_regex.match(pandas_obj) is not None


@extensions.register_check_method(check_type="element_wise")
def check_prefix(pandas_obj, *, prefix: str):
    """文字列のプレフィックスが指定文字列と一致するか"""
    return pandas_obj.startswith(prefix)


@extensions.register_check_method(check_type="element_wise")
def IDがあるか(pandas_obj, *, find_df: pd.DataFrame, column_name: str):
    """指定要素が特定のデータフレームのデータに存在するか"""
    return not find_df.query(f'{column_name} == ["{pandas_obj}"]').empty


def create_check(param_str: str) -> pa.Check | None:
    """文字列からCheck処理を生成"""
    if param_str.startswith(">="):
        return pa.Check.ge(int(param_str[2:]))
    if param_str.startswith(">"):
        return pa.Check.gt(int(param_str[1:]))
    if param_str.startswith("<="):
        return pa.Check.le(int(param_str[2:]))
    if param_str.startswith("<"):
        return pa.Check.lt(int(param_str[1:]))

    params = param_str.split(",")
    match params[0]:
        case "ref":
            return pa.Check.IDがあるか(find_df=ref_data[params[1]], column_name=params[2])
        case "startswith":
            return pa.Check.check_prefix(prefix=params[1])
        case "isalnum_":
            return pa.Check.isalnum_()
        case _:
            return None


def create_check_list(param_str_list: list[str]) -> list[pa.Check]:
    """文字列配列からChecksへ渡す配列を生成"""
    ret_checks = []
    for param_str in param_str_list:
        ret_checks.append(create_check(param_str))
    return ret_checks


def create_index_checks(data: Dict[str, Any]) -> pa.Index:
    """IndexのCheck設定を生成"""
    return pa.Index(
        dtype=locate(data["type"]),  # 文字列から型に変換
        checks=create_check_list(data["checks"]),
        unique=data["unique"] if "unique" in data else False,
    )


def create_column_checks(data: Dict[str, Any]) -> Dict[str, pa.Column]:
    """ColumnのCheck設定を生成"""
    columns = {}
    for name, column in data.items():
        columns[name] = pa.Column(
            dtype=locate(column["type"]),
            checks=create_check_list(column["checks"]),
            unique=data["unique"] if "unique" in data else False,
        )
    return columns


df_data01 = pd.read_excel("data/data01.xlsx", sheet_name="data", index_col=0)
df_data02 = pd.read_excel("data/data02.xlsx", index_col=0)

ref_data = {"data01": df_data01, "data02": df_data02}

with open("data/data01_check.yml") as file:
    data01_check = yaml.safe_load(file)

data01_schema = pa.DataFrameSchema(
    index=create_index_checks(data01_check["index"]),
    columns=create_column_checks(data01_check["columns"]),
    strict=True,  # 定義したカラムのみしか持たないか確認
    coerce=True,  # 強制型変換
)

try:
    data01_schema.validate(df_data01, lazy=True)
except pa.errors.SchemaError as err:
    # lazy=Falseの場合はカラム毎にエラーをraiseされる
    print(err.failure_cases)
except pa.errors.SchemaErrors as err:
    # lazy=Trueの場合は全てのエラーをまとめてraiseされる
    print(err.failure_cases)
else:
    print("data01 validation OK!")
finally:
    pass
