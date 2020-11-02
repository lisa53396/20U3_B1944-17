import numpy as np
import glob 

fulldatatype=([('pulse','i8'),('frequency','i8'),('phase','i8'),('intensity','f8')])

print("Files must be in pdv format with only 1 polarisation channel (I)")
print("Enter path to directory containing files to be cleared, and name the files (using * )")
path = input()
print("Enter number of bins")
bins = input()
print("Enter pulsar period")
period = input()
print("Code is currently hardcoded for certain values for Parkes data for B1944+17. Will need to change if applying to another pulsar")

SF = int(bins)/float(period)


file_names = glob.glob(path)
print(path)
print(file_names)

for filen in file_names:
    pulse_file = np.loadtxt(fname=filen, dtype=fulldatatype)
    no_freq_bands = max(pulse_file['frequency'])+1

    f = open(filen)
    header = f.readline()
    f.close()

    for freq in range(0,no_freq_bands):
        f = pulse_file['frequency'] == freq
        x = pulse_file['phase'][f]
        y = pulse_file['intensity'][f]

        #Fourier Transform
        fft=np.fft.rfft(y)
        ffta=abs(fft)

        values=np.arange(int(len(fft)))
        values=values/int(bins)

        frequency=values*SF

        #Printing values of RFI frequency
        val = max(ffta[50:100])
        val2 = max(ffta[250:500])
        index = np.where(ffta==val)
        index2 = np.where(ffta==val2)
        fre=index[0]/1024*SF
        fre2=index2[0]/1024*SF
        print('Frequency band:',freq,'Frequencies of FRI:',fre,fre2)

        #Zeroing the problem frequencies
        fft[index[0]]=0
        fft[index2[0]]=0

        #Inverse FFT
        newy=np.fft.irfft(fft)

        pulse_file['intensity'][f]=newy

    np.savetxt(filen+'.RFIR', pulse_file, delimiter=" ", header=header[2:-1], fmt=['%d','%d','%d','%0.6f']) 
    print(filen+'.RFIR')

