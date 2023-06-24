%% calculating flight time code for TT:

clc
clear all

lengthphantom=0.0796;  %in m
temp=20.7;           %in C

%get water data waveform
pathwater='C:\Users\chloe\Documents\school grad\lab files\20220929 data RO water and cyclic\20220929-1w_600.csv';
%get phantom data waveform
pathphantom='C:\Users\chloe\Documents\school grad\lab files\20220929 data RO water and cyclic\20220929-2p1_600.csv';


Pw=readtable(pathwater); %getting the pressure waveforms
Pp=readtable(pathphantom);

cwater = 1402.38744 + 5.03835027 * temp - 0.0581142290 * temp^2 + 0.000334558776 * temp^3 - 0.00000148150040 * temp^4 + 0.00000000316081885 * temp^5; %Calculated velocity of ultrasound in water in m/s based on Nykolai paper data

[zerow,zeroindexw]=min(abs((Pw.Time)-0)); %finding the 0 point of the time waveform
[zerop,zeroindexp]=min(abs((Pp.Time)-0)); %finding the 0 point of the time waveform

point5000w=zeroindexw+5000; %cropping out the first sent signal, so we're just comparing the received ones
point5000p=zeroindexp+5000;


% fs=1/(time(2)-time(1))*10^6; %getting the sampling frequency in Hz, just because I'm curious about it

lastpoint=length(Pw.Average_B_)-2;
time=Pw.Time([point5000w:lastpoint]); %making a time vector that starts at zero+5000points and is the right length
Pw=Pw.Average_B_([point5000w:lastpoint]); %clipping the pressure waveforms so they start at the time=0 spot, where the signal is sent from transducer
Pp=Pp.Average_B_([point5000w:lastpoint]);


xcorrwp=xcorr(Pp,Pw,'normalized'); %taking a correlation between the two
corrN=length(xcorrwp); %how long is that correlation vector?
seconds = time(end)-time(1); %How many microseconds is the time vector? (I'm not 100% sure on the units here)
timecorr=linspace(-seconds ,seconds ,corrN); %making a time vector to go with the xcorrwp, where the center is time=0

[xcorrmax,xcorrindexw]=max(abs(xcorrwp)); %finding the peak of the correlation, which corresponds to the time delay where the pressure waves best match each other

delay=timecorr(xcorrindexw)/(10^6); %Finding the time delay in seconds from that peak

cphantom = lengthphantom / ((lengthphantom / cwater) + delay) %calculating the speed of sound of the phantom from that delay and the speed of sound in water

% figure(1)
% plot(timecorr,xcorrwp)
% grid on
% xlim([-10,10])
% 
% figure(2)
% plot(time,Pw)
% hold on
% plot(time,Pp)
% hold off

%{ 
THIS IS THE PYTHON CODE I USED AS A TOUCHSTONE 

inputCalculations.velocityWater = 1402.38744 + 5.03835027 * inputCalculations.waterTemperature - 0.0581142290 * inputCalculations.waterTemperature ** 2 + 0.000334558776 * inputCalculations.waterTemperature ** 3 - 0.00000148150040 * inputCalculations.waterTemperature **4 + 0.00000000316081885 * inputCalculations.waterTemperature ** 5 #Calculated velocity of ultrasound in water in m/s based on Nykolai paper data

def calcFlightTime():
	P1 = 2 * calcFFT.FF1 #Pulls the Fourier Transform from the data and multiplies it by to in order to .......???????????????????????????????????????????
	P1[len(calcFFT.FF1)//2 + 2: len(calcFFT.FF1)] = 0 #Fabricates Fourier transform of anlytic signal for Length 1
	pressure1 = fft.ifft(P1) #Brings the pressure back into the time domain instead of the frequency domain
	calcFlightTime.pressureEnv1 = np.sqrt(pressure1 * np.conj(pressure1)) #Removes the imaginary part to give you only the real part of the pressure

	P2 = 2 * calcFFT.FF2
	P2[len(calcFFT.FF2)//2 + 2: len(calcFFT.FF2)] = 0  
	pressure2 = fft.ifft(P2)
	calcFlightTime.pressureEnv2 = np.sqrt(pressure2 * np.conj(pressure2))

	xCorrelation = np.correlate(calcFlightTime.pressureEnv2, calcFlightTime.pressureEnv1, "full") #Cross correlates the two pressure arrays
	peakIndXC = np.argmax(xCorrelation) #Returns the index of the max value of the cross correlation
	peakIndShift = peakIndXC - len(calcFlightTime.pressureEnv2) #Finds the difference in the indices when the largest signal arrives at the hydrophone for the two samples 

	timeDiff = peakIndShift * (1 / userInputValues.sampleRate) #Calculates how much time passes between the arrival of the two max signals
	calcFlightTime.shortLengthM = userInputValues.shortLength / 1000
	calcFlightTime.longLengthM = userInputValues.longLength / 1000
	calcFlightTime.diffLengthM = calcFlightTime.longLengthM - calcFlightTime.shortLengthM
	calcFlightTime.velocitySample = calcFlightTime.diffLengthM / ((calcFlightTime.diffLengthM / inputCalculations.velocityWater) + timeDiff)
%}