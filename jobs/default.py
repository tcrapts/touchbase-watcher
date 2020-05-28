import sys
import pandas as pd

file = sys.argv[1]
df = pd.read_csv(file)
print(df)