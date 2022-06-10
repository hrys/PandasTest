import re
import pandas as pd
import pandera as pa
import pandera.extensions as extensions

alnum_Regex = re.compile(r'^[a-zA-Z0-9_]+$')
@extensions.register_check_method(check_type="element_wise")
def isalnum_(pandas_obj):
    return alnum_Regex.match(pandas_obj) is not None

@extensions.register_check_method(statistics=["prefix"], check_type="element_wise")
def check_prefix(pandas_obj, *, prefix:str):
    return pandas_obj.startswith(prefix)

@extensions.register_check_method(statistics=["find_df"], check_type="element_wise")
def IDがあるか(pandas_obj, *, find_df:pd.DataFrame):
    return not find_df.query(f'id == ["{pandas_obj}"]').empty
# def value04_validate(find_id: str, find_df:pd.DataFrame) -> (pd.Series | bool):
#     return not find_df.query(f'id == ["{find_id}"]').empty

df_data01 = pd.read_excel("data/data01.xlsx", sheet_name="data", index_col=0)
df_data02 = pd.read_excel("data/data02.xlsx", index_col=0)

data01_schema = pa.DataFrameSchema(
    index = pa.Index(
        dtype=str,
        # checks=pa.Check(lambda x: x.startswith("A0") and isalnum_(x), element_wise=True),
        checks=[
            pa.Check.check_prefix("A0"),
            pa.Check.isalnum_()
        ],
        description="ID説明",
        unique=True # id の重複はエラー
    ),
    columns = {
        "value01": pa.Column(dtype=int, checks=pa.Check.ge(0)),
        "value02": pa.Column(dtype=int, checks=pa.Check.ge(0)),
        "value03": pa.Column(dtype=int, checks=pa.Check.ge(0)),
        "value04": pa.Column(dtype=str, checks=[
            pa.Check.IDがあるか(find_df=df_data02)
            # pa.Check(lambda value: value04_validate(value, df_data02), element_wise=True)
            # pa.Check(lambda value: not df_data02.query(f'id == ["{value}"]').empty, element_wise=True, raise_warning=True)
            # pa.Check(lambda value: not df_data02.query(f'id == ["{value}"]').empty, element_wise=True)
        ])
    },
    description="aaaaaaa",
    strict=True,    # 定義したカラムのみしか持たないか確認
    coerce=True     # 強制型変換
)

# with open("to_yaml.yml", "wt") as file:
#     file.write(data01_schema.to_yaml())

try:
    data01_schema.validate(df_data01, lazy=True)
except pa.errors.SchemaError as err:
    # lazy=Falseの場合はカラム毎にエラーをraiseされる
    print(err.failure_cases)
except pa.errors.SchemaErrors as err:
    # lazy=Trueの場合は全てのエラーをまとめてraiseされる
    # print(err.failure_cases.values)
    # print(err.failure_cases.values)
    # print(err.data)
    print(err.failure_cases)
else:
    print("data01 validation OK!")
finally:
    pass
