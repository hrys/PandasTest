import pandas as pd

df_data01 = pd.read_excel("data/data01.xlsx", index_col=0)
df_data02 = pd.read_excel("data/data02.xlsx", index_col=0)

df_data01.to_csv("data01.csv")
df_data02.to_csv("data02.csv")
# df_data01.to_csv("data01.csv", index=False)
# df_data02.to_csv("data02.csv", index=False)

df_data01.to_json("data01.json")
df_data01.to_html("data01.html")
df_data01.to_markdown("data01.md")

df_data01.to_xml("data01.xml")
