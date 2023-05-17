import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd

# function that returns dy/dt
def model(y,t):
    B = 0.0015
    I = 0.0264
    TC = .04
    if y > 0:
        f = 1
    elif y == 0:
        f = 0
    elif y < 0:
        f = -1

    dydt = (-B*y-TC*f)/I
    return dydt

# initial condition
y0 = [52.3777]

# time points
t,step_size = np.linspace(0,20, retstep=True)
# print(f"t_step_size: {step_size}")
# print(f"Values of t:\n{t}")
# solve ODEs

w2 = odeint(model,y0,t)

# print(w2)
# plot results
plt.plot(t, w2,'r-',linewidth=2,label='odefunc')
plt.xlabel('time')
plt.ylabel('w(t)')
plt.legend()
plt.savefig("odefunc.svg")
# plt.show()
# (supported formats for plt.savefig: eps, jpeg, jpg, pdf, pgf, png, 
# ps, raw, rgba, svg, svgz, tif, tiff, webp)

#step one, we need to mesh the two arrays together 
t = t.transpose()
w2 = w2.flatten() #changes this 2d array to a 1d array.
data_to_export = np.stack((t,w2))
# print(data_to_export)

# alternate way to do this is to convert both the arrays to lists.
t3 = t.tolist()
w3 = w2.tolist()
data_to_export3 = {"t3":t3,"w3":w3}
# print(data_to_export3)

#now we need to convert the data to a dataframe 
#and then export it to an excel file
df = pd.DataFrame(data_to_export)
df = df.transpose()

df3 = pd.DataFrame(data_to_export3)

print(df)
print(df3)
excel_export_diffEQ = pd.ExcelWriter('new_test.xlsx', mode= 'w') #will append both dataframes to the same excel file
# df.to_excel(excel_export_diffEQ, sheet_name='Sheet 1', startrow=0, startcol=0, index=False)

df3.to_excel(excel_export_diffEQ, sheet_name="Sheet 1", startrow=0, startcol=0, index=False)
