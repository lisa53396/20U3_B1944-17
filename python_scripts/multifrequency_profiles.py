import numpy as np
import matplotlib.pyplot as plt
import sys

#Import frequency information
print("What is the minimum frequency of the observation? (MHz)")
minf=int(input())
print("What is the maximum frequency of the observation? (MHz)")
maxf=int(input())

print("What minimum phase do you want on the plot?")
minp=float(input())
print("What maximum phase do you want on the plot?")
maxp=float(input())

print("Graph title")
title=input()

print("Do you want to save the figure? Y/N")
save=input()

plt.figure(figsize=(3,10))

#Command line argument as file name
obsname=sys.argv[1]

#Data type and importing data
obs_dt=([('pulse','i8'),('frequency','i8'),('phase','i8'),('intensity','f8')])
profiles=np.loadtxt(fname=obsname, dtype=obs_dt)

#Defining frequency
no_freq=max(profiles['frequency'])+1
size_freq=(maxf-minf)/no_freq
halfsize_freq=size_freq/2

#Repeating for each profile
offset=0
for freq in range(0, no_freq):
    #Selecting only one frequency profile
    f=profiles['frequency'] == freq
    x=profiles['phase'][f]
    xconv=max(x)
    x=x/xconv
    y=profiles['intensity'][f]

    #Defining centre frequency
    cf=int((freq*size_freq)+minf+halfsize_freq)
    print(cf)

    if len(x)!=0 and len(y)!=0:
        #Normalising y
        y=y/max(y)
        #creating offset
        y=y+offset
        offset=offset+1
        labels=str(cf)+'MHz'
        
        plt.plot(x[int(minp*xconv):int(maxp*xconv)],y[int(minp*xconv):int(maxp*xconv)],label=labels,color='black',lw=0.75)
        plt.text(minp+0.025,offset-0.75,labels,fontsize=6)


plt.yticks([])
plt.title(title)
plt.xlabel('Phase')
plt.ylabel('Intensity')

if save == "Y":
    plt.savefig(title)
plt.show()
