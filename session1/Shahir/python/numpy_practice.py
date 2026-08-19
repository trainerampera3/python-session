import numpy as np
import numpy as np
import pandas 
import matplotlib.pyplot as plt
array=np.array([1,2,4])
ones=np.ones((2,2))
zeros=np.zeros((2,2))
empty=np.empty((2,2))
aranged=np.arange(0,5,3)
linspce=np.linspace(1,10,10)
new_reshaped_array=linspce.reshape((2,5))
linspce.resize((2,5))
new_=new_reshaped_array.flatten()
#print(new_reshaped_array)
ind=np.where(new_reshaped_array<5)
array_1=np.linspace(10,20,4)
r_array_1=array_1.reshape((2,2))
array_2=np.linspace(0,10,4)
r_array_2=array_2.reshape((2,2))
#now we stack the elements together
result=np.hstack((r_array_1,r_array_2))
aftet_split=np.hsplit(result,2)

print(aftet_split)