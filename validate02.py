import pandas as pd
import pandera as pa

df_data01 = pd.read_excel("data01.xlsx", index_col=0)
df_data02 = pd.read_excel("data02.xlsx", index_col=0)

data01_schema = pa.DataFrameSchema(
    columns = {
        "value01": pa.Column(int, checks=pa.Check.ge(0)),
        "value02": pa.Column(int, checks=pa.Check.ge(0)),
        "value03": pa.Column(int, checks=pa.Check.ge(0)),
        "value04": pa.Column(str, checks=[
            # ラムダの引数valuesはSeriesで渡される。applyで全要素にチェック処理を行う
            pa.Check(lambda values: values.apply(lambda id: not df_data02.query(f'id == ["{id}"]').empty))
        ])
    },
    strict=True,    # 定義したカラムのみしか持たないか確認
    coerce=True     # 強制型変換
)
data01_schema.validate(df_data01)