import pandas as pd

df_data01 = pd.read_excel("data01.xlsx", index_col=0)
df_data02 = pd.read_excel("data02.xlsx", index_col=0)

for find_id in df_data01.loc[:, "value04"]:
    result = df_data02.query(f'id == ["{find_id}"]')
    if result.empty:
        print(f"{find_id} ない")
    else:
        print(f"{find_id} ある")
        print(result)

df_data01.to_csv("data01.csv")
df_data02.to_csv("data02.csv")