import pandas as pd
import pandera as pa

df_data01 = pd.read_excel("data/data01.xlsx", index_col=0)
df_data02 = pd.read_excel("data/data02.xlsx", index_col=0)

def value04_validate(values: pd.Series, find_df:pd.DataFrame) -> (pd.Series | bool):
    return values.apply(lambda id: not find_df.query(f'id == ["{id}"]').empty)

data01_schema = pa.DataFrameSchema(
    index = pa.Index(
        str,
        pa.Check(lambda x: x.str.startswith("A0")),
        unique=True # id の重複はエラー
    ),
    columns = {
        "value01": pa.Column(int, checks=pa.Check.ge(0)),
        "value02": pa.Column(int, checks=pa.Check.ge(0)),
        "value03": pa.Column(int, checks=pa.Check.ge(0)),
        "value04": pa.Column(str, checks=[
            pa.Check(lambda values: value04_validate(values, df_data02))
        ])
    },
    strict=True,    # 定義したカラムのみしか持たないか確認
    coerce=True     # 強制型変換
)
data01_schema.validate(df_data01)
