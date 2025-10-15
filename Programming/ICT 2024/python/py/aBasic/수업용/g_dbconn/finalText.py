import pandas as pd

# 엑셀 파일 경로
excel_file = './files/ev_list.xlsx'

# 엑셀 파일 읽기
df = pd.read_excel(excel_file)

# 데이터 확인
print(df.head())  # 처음 몇 줄 출력