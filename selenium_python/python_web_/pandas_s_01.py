import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
s = pd.Series([1,3,5,np,6,8])
print(s)
dates = pd.date_range('20130101',periods=6)
print(dates)
df = pd.DataFrame(np.random.random(6,4),index=dates,columns=('ABCD'))
print(df)