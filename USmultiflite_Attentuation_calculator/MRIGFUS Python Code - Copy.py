#You need to copy and paste ths into the command line and hit enter: python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

#Notes
#Automate the file type and the full path into one function
# Could you window using the period and moving back a quarter period, and find ways to break it. Output the final signals used for the automated code.
#Two different codes
#Start with replicating the data
#Analyze the code for the frequency
#Useginput to have the user select input on figure

#Notes round two
#make the file uploading more flexible
#We want the speed of sound as a function of the frequency at 0.6, 1, 1.8, 3.0 MHz
#At the beginning: What frequencies do you plan to input?
#Think about 6 fat samples and 4 frequencies with water only and 8 water temps
#Inputs: Frequencies vector text file, path to files in a folder, water bath temp text file



import tkinter as tk, math as m, matplotlib.pyplot as plt, matplotlib.axes as ax, tkinter.filedialog as fd, numpy.fft as fft, numpy as np, os #various functions from all of these libraries will be used throughout the program.
from datetime import datetime

#def fileTypeMenu(): #User selectes file input type
#	valid = 1
#	while valid:
#		print("[1] .txt \n[2] .isf \n[3] .xls") #Displays file type options
#		try:#Recieves user input for the file type they will select and tries to convert the string input into an integer
#			fileTypeMenu.fileType = int(input("Type the number next to your file type and press enter: ")) 
#		except: #If the in input cannot be made an integer then the loop will repromt the user for an integer
#			print("Invalid selection.")
#			print()
#			continue		
#		if fileTypeMenu.fileType == 1 or fileTypeMenu.fileType == 2 or fileTypeMenu.fileType == 3: #Checks to make sure the integer was on the menu as an option
#			valid = 0
#		else:
#			print("Invalid selection.")
#			print()


def filePathRetreval(): #Sets the file paths to the selected files depending on the file type 
	print("The code can only take .txt, .isf, and .csv file types.")

	#if fileTypeMenu.fileType == 1: #TXT files
	print("Select your SHORTER LENGTH or WATER-ONLY file when the file window opens.")
	root = tk.Tk()
	root.withdraw()
	filePathRetreval.filePath1 = fd.askopenfilename(title = "Open file for SHORTER LENGTH (L2) or WATER-ONLY") #Extracts file name from the selected file
	print("Select your LONGER LENGTH file when the file window opens.")
	filePathRetreval.filePath2 = fd.askopenfilename(title = "Open file for LONGER LENGTH (L1)")

	#elif fileTypeMenu.fileType == 2: #ISF files
	#	print("Select your SHORTER LENGTH or WATER-ONLY .isf file when the file window opens.")
	#	root = tk.Tk()
	#	root.withdraw()
	#	filePathRetreval.filePath1 = fd.askopenfilename(title = "Open .isf file for SHORTER LENGTH (L2) or WATER-ONLY")
	#	print("Select your LONGER LENGTH .isf file when the file window opens.")
	#	filePathRetreval.filePath2 = fd.askopenfilename(title = "Open .isf file for LONGER LENGTH (L1)")

	#elif fileTypeMenu.fileType == 3: #CSV files
	#	print("Select your SHORTER LENGTH or WATER-ONLY .csv file when the file window opens.")
	#	root = tk.Tk()
	#	root.withdraw()
	#	filePathRetreval.filePath1 = fd.askopenfilename(title = "Open your first file.")
	#	print("Select your LONGER LENGTH .csv file when the file window opens.")
	#	filePathRetreval.filePath2 = fd.askopenfilename(title = "Open your second file.")


def dataExtraction(): #You cannot have extra white space at the end of the file. The last line of your file needs to be your last points of data.
	dataExtraction.finalDataShort = [] #Initializes the list where the data will be placed
	file_TXT = open(filePathRetreval.filePath1, "r") #Opens the file you selected and pulls out the data
	lines = file_TXT.readlines()
	for x in lines:
		if x: #Skips empty lines because empty lines are boolean false
			tempData = (x.split(',')) #Splits each line of data into a list with two points in the list
		for i in range(0, len(tempData)):
			try:
				tempData[i] = float(tempData[i]) #Converts the data list to a list of two floats
			except:
				continue
		if type(tempData[0]) == float and type(tempData[1]) == float: #Only lets lists with two float entries get added to the list of data
			dataExtraction.finalDataShort.append(tempData) #Makes a list of lists that are floats as values
		else:
			continue
	file_TXT.close()

	dataExtraction.finalDataLong = [] #This does the some thing as the code above but for the second file selected
	file_TXT = open(filePathRetreval.filePath2, "r")
	lines = file_TXT.readlines()
	for x in lines:
		if x: #Skips empty lines because empty lines are boolean false
			tempData = (x.split(',')) #Splits each line of data into a list with two points in the list
		for i in range(0, len(tempData)):
			try:
				tempData[i] = float(tempData[i]) #Converts the data list to a list of two floats
			except:
				continue
		if type(tempData[0]) == float and type(tempData[1]) == float: #Only lets lists with two float entries get added to the list of data
			dataExtraction.finalDataLong.append(tempData) #Makes a list of lists that are floats as values
		else:
			continue
	file_TXT.close()

	if len(dataExtraction.finalDataShort) != len(dataExtraction.finalDataLong): #Checks to amkes sure the number of data points is the same for each file bewfore windowing
		print ("The lengths of the two files must be the same.")
	

def windowSelection():
	print()
	print("Do you wish to window the time-domain data (to exclude multiple refletions for example)? [y/n]")
	windowSelection.windowSelect = input("If yes, mouse click on the desired lower bound, then select the desire upper bound, in the following two plots. ") #Accepts a string user input
	repeat = 1
	while repeat: #This is used to confirm is the input above is a 'y' for yes or an 'n' for no
		if windowSelection.windowSelect == 'y': #'y' was selected and we are going to window the data
			repeat = 0 #There was a valid input to the windowing question

			rewindow = "y"
			while rewindow == "y": #This is will be used to allow the user to rewindow the data set if the show plot is not what they wanted
				windowSelection.timeValuesShort = []
				windowSelection.magnitudeValuesShort = []
				for i in range(0, len(dataExtraction.finalDataShort)):
					windowSelection.timeValuesShort.append(dataExtraction.finalDataShort[i][0] - dataExtraction.finalDataShort[0][0]) #Fills in a list for the time values and normalizes the data so the first point is 0 seconds and counts up from there
					windowSelection.magnitudeValuesShort.append(dataExtraction.finalDataShort[i][1]) #Fills in a list of the amplitudes that will correspond to the time normalized time values by index
				plt.plot(windowSelection.timeValuesShort, windowSelection.magnitudeValuesShort) #Plots the data from the two lists
				plt.title("Select the lower limit of your window and then the upper limit.\nClose the window when you are done.") #Adds a title to the window
				plt.xlabel("Time (s)")
				plt.ylabel("Voltage (mV)")
				while 1: #Loops infinitely until the break command is reached
					limitSelections = plt.ginput(2) #Asks user for the lower and upper limits of the window they want to add to the data set
					lowerLimitShort = limitSelections[0][0]
					upperLimitShort = limitSelections[1][0]
					if lowerLimitShort >= upperLimitShort: #Ensures the lower limit is lower than the upper limit
						print("The lower limit must be selected first and then the upper limit is selected second!") #Prints the problem
						continue #Loops to ask for lower and upper limit inputs again
					else:
						plt.close()
						break
				offset = 0
				for i in range(0, len(dataExtraction.finalDataShort)):
					if windowSelection.timeValuesShort[0] < lowerLimitShort: #removes all points below the lower limit
						windowSelection.timeValuesShort.pop(0)
						windowSelection.magnitudeValuesShort.pop(0)
						offset = offset + 1
					elif windowSelection.timeValuesShort[i - offset] > upperLimitShort: #removes all points above the upper limit
						windowSelection.timeValuesShort.pop(i - offset)
						windowSelection.magnitudeValuesShort.pop(i - offset)
						offset = offset + 1
					else: #skips removing the value from the data if it is between the selected lower and upper limits
						continue
				plt.plot(windowSelection.timeValuesShort, windowSelection.magnitudeValuesShort)
				plt.title("Preview of the Windowed Data for Shorter Sample")
				plt.xlabel("Time (s)")
				plt.ylabel("Voltage (mV)")
				plt.show() #Shows the plot of the windowed data
				plt.close()
				rewindow = input("Do you want to rewindow the shorter sample or water data? [y/n] ") #Prompts the user if they want to reselect the window boundaries
				if rewindow == 'y':
					continue
				elif rewindow == 'n':
					break
				else:
					rewindow = input("Please enter 'y' for yes or 'n' for no and then press enter: ") #asks again if anything beside 'y' or 'n' is input



			rewindow = "y"
			while rewindow == "y": #Does the same thing as above but looks at the longer sample data
				windowSelection.timeValuesLong = []
				windowSelection.magnitudeValuesLong = []
				for i in range(0, len(dataExtraction.finalDataLong)):
					windowSelection.timeValuesLong.append(dataExtraction.finalDataLong[i][0] - dataExtraction.finalDataLong[0][0])
					windowSelection.magnitudeValuesLong.append(dataExtraction.finalDataLong[i][1])
				plt.plot(windowSelection.timeValuesLong, windowSelection.magnitudeValuesLong)
				plt.title("Select the lower limit of your window and then the upper limit.\nClose the window when you are done.")
				plt.xlabel("Time (s)")
				plt.ylabel("Voltage (mV)")
				limitSelections = plt.ginput(2)
				lowerLimitLong = limitSelections[0][0]
				upperLimitLong = limitSelections[1][0]
				while 1:
					if lowerLimitLong >= upperLimitLong:
						print("The lower limit must be selected first and then the upper limit is selected second!")
						continue
					else:
						plt.close()
						break
				offset = 0
				for i in range(0, len(dataExtraction.finalDataShort)):
					if windowSelection.timeValuesLong[0] < lowerLimitLong: #removes all points below the lower limit
						windowSelection.timeValuesLong.pop(0)
						windowSelection.magnitudeValuesLong.pop(0)
						offset = offset + 1
					elif windowSelection.timeValuesLong[i - offset] > upperLimitLong: #removes all points above the upper limit
						windowSelection.timeValuesLong.pop(i - offset)
						windowSelection.magnitudeValuesLong.pop(i - offset)
						offset = offset + 1
					else: #skips removing the value from the data if it is between the click limits
						continue
				plt.plot(windowSelection.timeValuesLong, windowSelection.magnitudeValuesLong)
				plt.title("Preview of the Windowed Data for Longer Sample")
				plt.xlabel("Time (s)")
				plt.ylabel("Voltage (mV)")
				plt.show()
				plt.close()
				rewindow = input("Do you want to rewindow the longer sample data? [y/n] ")
				if rewindow == 'y':
					continue
				elif rewindow == 'n':
					break
				else:
					rewindow = input("Please enter 'y' for yes or 'n' for no and then press enter: ")

			runningTotal = 0
			for i in range(0, len(dataExtraction.finalDataShort)):
				runningTotal = runningTotal + dataExtraction.finalDataShort[i][1] #Gets the sum of all the magnitudes of the windowed data set for the shorter or water only sample
			windowSelection.wmean = runningTotal / len(dataExtraction.finalDataShort) #Calculates the average amplitude for water
			
			runningTotal = 0
			for i in range(0, len(dataExtraction.finalDataLong)):
				runningTotal = runningTotal + dataExtraction.finalDataLong[i][1] #Does the same thing as the for loop above but for the longer sample windowed data
			windowSelection.smean = runningTotal / len(dataExtraction.finalDataLong)

		elif windowSelection.windowSelect == 'n': #Does not window the data but still looks for the mean amplitude of the original data set
			runningTotal = 0
			for i in range(0, len(dataExtraction.finalDataShort)):
				runningTotal = runningTotal + dataExtraction.finalDataShort[i][1]
			windowSelection.wmean = runningTotal / len(dataExtraction.finalDataShort)
			
			runningTotal = 0
			for i in range(0, len(dataExtraction.finalDataLong)):
				runningTotal = runningTotal + dataExtraction.finalDataLong[i][1]
			windowSelection.smean = runningTotal / len(dataExtraction.finalDataLong)
			repeat = 0

		else: #Loops the window prompt until 'y' or 'n' is selected
			windowSelection.windowSelect = input("Please press 'y' for yes or 'n' for no and then press enter: ")


def userInputValues():
	print()
	userInputValues.sampleRate = 1 / ((dataExtraction.finalDataShort[1][0] - dataExtraction.finalDataShort[0][0])/1000000) #Divide by 1000000 to convert the time data of microseconds into seconds
	#userInputValues.sampleRate = input("Enter the sampling rate of your files in Hz: ") #Recieves the sampling rate from the user
	#while userInputValues.sampleRate != float:
	#	try:									#evaluates if the input string can be converted to a float
	#		userInputValues.sampleRate = float(userInputValues.sampleRate)		#reassigns sample rate to be a float if it can be converted from a string to a float, if not then the try block ends here and except is run
	#		break								#ends the while loop
	#	except:									#if the user input cannot be converted to a float the except block is run
	#		userInputValues.sampleRate = input("The sampling rate needs to be a number. Please enter the sampling rate of your files in Hz: ")
	#		continue							#repeats the while loop

	userInputValues.shortLength = input("Enter the SHORTER sample's thickness in millimeters (if water enter 0): ") #Recieves the length of the shorter sample
	while userInputValues.shortLength != float:
		try:
			userInputValues.shortLength = float(userInputValues.shortLength)
			break
		except:
			userInputValues.shortLength = input("The length needs to be a number. Please enter the SHORTER sample's thickness in millimeters (if water enter 0): ")
			continue
			
	userInputValues.longLength = input("Enter the LONGER sample's thickness in millimeters: ") #Recieves the length of the longer sample
	while userInputValues.longLength != float:
		try:
			userInputValues.longLength = float(userInputValues.longLength)
			break
		except:
			userInputValues.longLength = input("The length needs to be a number. Please enter the LONGER sample's thickness in millimeters: ")
			continue
			
	userInputValues.densitySample = input("If water was used in the shorter length, then type 0 for the density. Otherwise, enter the sample density in kg/m^3: ") #Recieves the density of the smaples
	while userInputValues.densitySample != float:
		try:
			userInputValues.densitySample = float(userInputValues.densitySample)
			if userInputValues.densitySample == 0:
				userInputValues.densitySample = 1000
			break
		except:
			userInputValues.densitySample = input("The density needs to be a number. If water was used in the shorter length, then type 0 for the density. Otherwise, enter the sample density in g/cm^3: ")
			continue

	userInputValues.velocitySample = input("Enter acoustic velocity of sample in m/s. If you want this to be calculated type 0: ") #Recieves the acoustic velocity of the sample if it is known
	while userInputValues.velocitySample != float:
		try:
			userInputValues.velocitySample = float(userInputValues.velocitySample)
			break
		except:
			userInputValues.velocitySample = input("The acostic velocity needs to be a number. Enter acoustic velocity in m/s. If you want this to be calculated type 0: ")
			continue

def inputCalculations():
	inputCalculations.waterTemperature = input("Enter the water temperature of the bath in degrees C: ") #Recieves the temperature of the bath
	while inputCalculations.waterTemperature != float:
		try:
			inputCalculations.waterTemperature = float(inputCalculations.waterTemperature)
			break
		except:
			inputCalculations.waterTemperature = input("The water temperature needs to be a number. Enter water temperature in degrees C: ")
			continue
	if windowSelection.windowSelect == 'y':
		inputCalculations.estDt = (windowSelection.timeValuesShort[10] - windowSelection.timeValuesShort[0])/10 #Calculated sampling rate from the data in Hz
		savedt = inputCalculations.estDt
		inputCalculations.velocityWater = 1402.38744 + 5.03835027 * inputCalculations.waterTemperature - 0.0581142290 * inputCalculations.waterTemperature ** 2 + 0.000334558776 * inputCalculations.waterTemperature ** 3 - 0.00000148150040 * inputCalculations.waterTemperature **4 + 0.00000000316081885 * inputCalculations.waterTemperature ** 5 #Calculated velocity of ultrasound in water in m/s based on Nykolai paper data
		deltaT = 1 / userInputValues.sampleRate #Time between data points in seconds
		totalTShort = deltaT * len(windowSelection.magnitudeValuesShort) #Duration of one trial in seconds
		totalTLong = deltaT * len(windowSelection.magnitudeValuesLong) #Duration of one trial in seconds
		inputCalculations.deltaFShort = 1 / totalTShort #Number of trials per second
		inputCalculations.deltaFLong = 1 / totalTLong #Number of trials per second
		tPlot = []
		inputCalculations.fPlot1 = []
		inputCalculations.fPlot2 = []
		for i in range(0, len(windowSelection.magnitudeValuesShort)): 
			tPlot.append(i * deltaT) #This makes a list of the time points 
			if i % 2 != 0: #Only adds to the frequency plot if the number is even to get half the frequency range
				inputCalculations.fPlot1.append((inputCalculations.deltaFShort * ((i-1)/2))/1000000) #This makes a list of the frequency range for the Hermitian spectrum in MHz	
		for i in range(0, len(windowSelection.magnitudeValuesLong)): 
			tPlot.append(i * deltaT) #This makes a list of the time points 
			if i % 2 != 0: #Only adds to the frequency plot if the number is even to get half the frequency range
				inputCalculations.fPlot2.append((inputCalculations.deltaFLong * ((i-1)/2))/1000000) #This makes a list of the frequency range for the Hermitian spectrum in MHz	

	else:
		inputCalculations.estDt = (dataExtraction.finalDataLong[10][0] - dataExtraction.finalDataLong[0][0])/10 #Calculated sampling rate from the data in Hz
		savedt = inputCalculations.estDt
		inputCalculations.velocityWater = 1402.38744 + 5.03835027 * inputCalculations.waterTemperature - 0.0581142290 * inputCalculations.waterTemperature ** 2 + 0.000334558776 * inputCalculations.waterTemperature ** 3 - 0.00000148150040 * inputCalculations.waterTemperature **4 + 0.00000000316081885 * inputCalculations.waterTemperature ** 5 #Calculated velocity of ultrasound in water in m/s based on Nykolai paper data
		deltaT = 1 / userInputValues.sampleRate #Time between data points in seconds
		totalT = deltaT * len(dataExtraction.finalDataShort) #Duration of one trial in seconds
		inputCalculations.deltaF = 1 / totalT #Number of trials per second
		tPlot = []
		inputCalculations.fPlot = []
		for i in range(0, len(dataExtraction.finalDataShort)): 
			tPlot.append(i * deltaT) #This makes a list of the time points 
			if i % 2 != 0: #Only adds to the frequency plot if the number is even to get half the frequency range
				inputCalculations.fPlot.append((inputCalculations.deltaF * ((i-1)/2))/1000000) #This makes a list of the frequency range for the Hermitian spectrum in MHz	


def calcFFT():
	if windowSelection.windowSelect == 'y': #Checks to see if the data was truncated by windowing
		calcFFT.frequencyValuesShort = []
		calcFFT.F1 = []
		for i in range (0, len(windowSelection.magnitudeValuesShort)): #May not be needed
			calcFFT.frequencyValuesShort.append(windowSelection.magnitudeValuesShort[i])
		calcFFT.FF1 = fft.fft(calcFFT.frequencyValuesShort) #Runs the FFT function
		for i in range(0, m.floor(len(calcFFT.FF1)/2)): #What is the point of this?
			calcFFT.F1.append(2 * abs(calcFFT.FF1[i]) / len(calcFFT.FF1))
		calcFFT.F1[0] = abs(calcFFT.FF1[0]) / len(calcFFT.FF1)

		calcFFT.frequencyValuesLong = []
		calcFFT.F2 = []
		for i in range (0, len(windowSelection.magnitudeValuesLong)):
			calcFFT.frequencyValuesLong.append(windowSelection.magnitudeValuesLong[i])
		calcFFT.FF2 = fft.fft(calcFFT.frequencyValuesLong)
		for i in range(0, m.floor(len(calcFFT.FF2)/2)):
			calcFFT.F2.append(2 * abs(calcFFT.FF2[i]) / len(calcFFT.FF2))
		calcFFT.F2[0] = abs(calcFFT.FF2[0]) / len(calcFFT.FF2)

		f1Threshhold = []
		for i in range(0, len(calcFFT.F1)):
			if calcFFT.F1[i] <= max(calcFFT.F1)/20:
				f1Threshhold.append(0) #Anything less than the maximum of the FFT divided by 20 is set to zero
			else:
				f1Threshhold.append(calcFFT.F1[i]) #Otherwise the value is placed into the threshold list
		spectrumSum = sum(f1Threshhold)
		spectrumCumSum = np.cumsum(f1Threshhold)
		centerIndex = calcFFT.F1.index(max(calcFFT.F1))
		calcFFT.centerFrequency = centerIndex * inputCalculations.deltaFShort / 1000000

	else:
		calcFFT.frequencyValuesShort = []
		calcFFT.F1 = []
		for i in range (0, len(dataExtraction.finalDataShort)):
			calcFFT.frequencyValuesShort.append(dataExtraction.finalDataShort[i][1])
		calcFFT.FF1 = fft.fft(calcFFT.frequencyValuesShort)
		for i in range(0, m.floor(len(calcFFT.FF1)/2)):
			calcFFT.F1.append(2 * abs(calcFFT.FF1[i]) / len(calcFFT.FF1))
		calcFFT.F1[0] = abs(calcFFT.FF1[0]) / len(calcFFT.FF1)

		calcFFT.frequencyValuesLong = []
		calcFFT.F2 = []
		for i in range (0, len(dataExtraction.finalDataLong)):
			calcFFT.frequencyValuesLong.append(dataExtraction.finalDataLong[i][1])
		calcFFT.FF2 = fft.fft(calcFFT.frequencyValuesLong)
		for i in range(0, m.floor(len(calcFFT.FF2)/2)):
			calcFFT.F2.append(2 * abs(calcFFT.FF2[i]) / len(calcFFT.FF2))
		calcFFT.F2[0] = abs(calcFFT.FF2[0]) / len(calcFFT.FF2)

		f1Threshhold = []
		for i in range(0, len(calcFFT.F1)):
			if calcFFT.F1[i] < max(calcFFT.F1)/20:
				f1Threshhold.append(0)
			else:
				f1Threshhold.append(calcFFT.F1[i])
		#print("Langth of the orginal fourier transform: ", len(calcFFT.F1))
		spectrumSum = sum(f1Threshhold)
		spectrumCumSum = np.cumsum(f1Threshhold)
		#print(f1Threshhold)
		#print(len(f1Threshhold))
		#print("Total Half Sum: ", spectrumSum)
		#print("Cum Sum: ", spectrumCumSum)
		#print(len(spectrumCumSum))
		#print()
		for i in range(0, len(spectrumCumSum)):
			if spectrumCumSum[i] > spectrumSum / 2:
				centerIndex = i + 1
				break
			else:
				continue
		#print(centerIndex)
		#print(spectrumSum/2)
		#print(spectrumCumSum[centerIndex])
		#print(calcFFT.F1)
		#print("Maximum: ", max(calcFFT.F1))
		#tempList = calcFFT.F1
		#tempList[0] = 0
		#maxVal = 0
		#for i in range(1, len(calcFFT.F1)):
		#	if calcFFT.F1[i] > maxVal:
		#		maxVal = calcFFT.F1[i]
		#	else:
		#		continue
		#print("Ranged Maximum: ", max(calcFFT.F1))
		#print(len(calcFFT.F1))
		#centerIndex = calcFFT.F1.index(max(calcFFT.F1))
		#print("Should match the maximum: ", calcFFT.F1[centerIndex])
		#print("Old center index: ", centerIndex)
		#print("Value @ center Frequency: ", calcFFT.F1[centerIndex])
		calcFFT.centerFrequency = centerIndex * inputCalculations.deltaF / 1000000
		#print("Old center frequency: ", calcFFT.centerFrequency)
		#print(spectrumSum)
		#print(spectrumCumSum)
		#centerIndex = calcFFT.F1.index(max(calcFFT.F1)) + 3
		#print("Adjusted center index: ", centerIndex)
		#print("Value @ center Frequency: ", calcFFT.F1[centerIndex])
		#calcFFT.centerFrequency = centerIndex * inputCalculations.deltaF / 1000000
		#print("Adjusted center frequency: ", calcFFT.centerFrequency)
		#print("Delta F: ", inputCalculations.deltaF)




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


def faceReflectionLoss():
	densityWater = 1000 #Density of water in kg/m^3
	impedanceWater = densityWater * inputCalculations.velocityWater #Impedance of water

	if userInputValues.velocitySample == 0:
		velocitySample = calcFlightTime.velocitySample
	else:
		velocitySample = userInputValues.velocitySample
	impedanceSample = userInputValues.densitySample * velocitySample

	R = (impedanceSample - impedanceWater) / (impedanceSample + impedanceWater) #Pressure relfection coefficient
	T = 1 - R * R #Power Transmission Coefficient
	TT = -1 * 10 * m.log10(T) #Estimate of attenuation due to both face reflections

	if calcFlightTime.shortLengthM == 0:	#Water only
		faceReflectionLoss.attenuationFace = TT				#Accounts for estimated face attenuation
		waterOnlyFlag = 1					#Denotes the shorter sample was a water phantom
	else:									#Shorter sample
		faceReflectionLoss.attenuationFace = 0
		waterOnlyFlag = 0


def calcAttenuation():
	sampleShortSquared = []
	sampleLongSquared = []
	for i in range(0, len(calcFFT.frequencyValuesShort)):
		sampleShortSquared.append((calcFFT.frequencyValuesShort[i] - windowSelection.wmean) * (calcFFT.frequencyValuesShort[i] - windowSelection.wmean))
	for i in range(0, len(calcFFT.frequencyValuesLong)):
		sampleLongSquared.append((calcFFT.frequencyValuesLong[i] - windowSelection.smean) * (calcFFT.frequencyValuesLong[i] - windowSelection.smean))
	calcAttenuation.attcmd = (10 * m.log10(sum(sampleShortSquared) / sum(sampleLongSquared)) - faceReflectionLoss.attenuationFace) / (calcFlightTime.diffLengthM * 100) #Calculation of attenuationin the time domain in dB per cm.
	if calcFlightTime.shortLengthM == 0:
		totalAttenuation = 10 * m.log10(sum(sampleShortSquared) / sum(sampleLongSquared))
	else:
		totalAttenuation = "NaN"


def printPlots():
	print()

	valid = 1
	while valid:
		printPlots.show = input("Do you want to see the signal and spectra plots? [y/n]: ")
		if printPlots.show == 'y':
			printPlots.show = 1
			valid = 0
		elif printPlots.show == 'n':
			printPlots.show = 0
			valid = 0
		else:
			print("Invalid selection. Please select 'y' for yes or 'n' for no.")
			print()

	if printPlots.show and printPlots.firstTimeThrough:
		valid = 1
		while valid:
			partial = input("Do you want to see only the first 1/40 of frequency range of the frequency spectra plot? [y/n]: ")
			if partial == 'y':
				printPlots.partial = 1
				valid = 0
			elif partial == 'n':
				printPlots.partial = 0
				valid = 0
			else:
				print("Invalid selection. Please select 'y' for yes or 'n' for no.")
				print()
		printPlots.firstTimeThrough = 0

	if printPlots.show:
		if windowSelection.windowSelect == 'y': #If the data has a window applied we use the selected window boundaries for the plots
			fig, [signal, pressure, FFT] = plt.subplots(nrows = 3, ncols = 1)
			fig.suptitle("Shorter or Water Only Sample", fontsize=16)

			signal.plot(windowSelection.timeValuesShort, windowSelection.magnitudeValuesShort)
			signal.set_xlabel("Time (microseconds)")
			signal.set_ylabel("Voltage (mV)")
			signal.set_title("Transmission Signal")
			pressure.plot(windowSelection.timeValuesShort, calcFlightTime.pressureEnv1)
			pressure.set_xlabel("Time (microseconds)")
			pressure.set_ylabel("Voltage (mV)")
			pressure.set_title("Envelope of Analytic Signal")
			if printPlots.partial:
				newFPlot1 = []
				newFFTPlot1 = []
				for i in range(0, len(inputCalculations.fPlot1)//40):
					newFPlot1.append(inputCalculations.fPlot1[i])
					newFFTPlot1.append(calcFFT.F1[i])
				FFT.plot(newFPlot1, newFFTPlot1)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			else:
				FFT.plot(inputCalculations.fPlot1, calcFFT.F1)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			plt.tight_layout()

			fig, [signal, pressure, FFT] = plt.subplots(nrows = 3, ncols = 1)
			fig.suptitle("Longer Sample", fontsize=16)

			signal.plot(windowSelection.timeValuesLong, windowSelection.magnitudeValuesLong)
			signal.set_xlabel("Time (microseconds)")
			signal.set_ylabel("Voltage (mV)")
			signal.set_title("Transmission Signal")
			pressure.plot(windowSelection.timeValuesLong, calcFlightTime.pressureEnv2)
			pressure.set_xlabel("Time (microseconds)")
			pressure.set_ylabel("Voltage (mV)")
			pressure.set_title("Envelope of Analytic Signal")
			if printPlots.partial:
				newFPlot2 = []
				newFFTPlot2 = []
				for i in range(0, len(inputCalculations.fPlot2)//40):
					newFPlot2.append(inputCalculations.fPlot2[i])
					newFFTPlot2.append(calcFFT.F2[i])
				FFT.plot(newFPlot2, newFFTPlot2)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			else:
				FFT.plot(inputCalculations.fPlot2, calcFFT.F2)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			plt.tight_layout()
			plt.show()


		else: #If the data was not windowed then we can simply plot the entire data set
			fig, [signal, pressure, FFT] = plt.subplots(nrows = 3, ncols = 1)
			fig.suptitle('Shorter or Water Only Sample', fontsize=16)

			timeValues = []
			voltageValues = []
			for i in range(0, len(dataExtraction.finalDataShort)):
				timeValues.append(dataExtraction.finalDataShort[i][0] - dataExtraction.finalDataShort[0][0])
				voltageValues.append(dataExtraction.finalDataShort[i][1])
			signal.plot(timeValues, voltageValues)
			signal.set_xlabel("Time (microseconds)")
			signal.set_ylabel("Voltage (mV)")
			signal.set_title("Transmission Signal")
			pressure.plot(timeValues, calcFlightTime.pressureEnv1)
			pressure.set_xlabel("Time (microseconds)")
			pressure.set_ylabel("Voltage (mV)")
			pressure.set_title("Envelope of Analytic Signal")
			if printPlots.partial:
				newFPlot = []
				newFFTPlot = []
				for i in range(1, len(inputCalculations.fPlot)//40):
					newFPlot.append(inputCalculations.fPlot[i])
					newFFTPlot.append(calcFFT.F1[i])
				FFT.plot(newFPlot, newFFTPlot)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			else:
				FFT.plot(inputCalculations.fPlot, calcFFT.F2)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			plt.tight_layout()

			fig, [signal, pressure, FFT] = plt.subplots(nrows = 3, ncols = 1)
			fig.suptitle("Longer Sample", fontsize=16)

			timeValues = []
			voltageValues = []
			for i in range(0, len(dataExtraction.finalDataLong)):
				timeValues.append(dataExtraction.finalDataLong[i][0] - dataExtraction.finalDataLong[0][0])
				voltageValues.append(dataExtraction.finalDataLong[i][1])
			signal.plot(timeValues, voltageValues)
			signal.set_xlabel("Time (microseconds)")
			signal.set_ylabel("Voltage (mV)")
			signal.set_title("Transmission Signal")
			pressure.plot(timeValues, calcFlightTime.pressureEnv2)
			pressure.set_xlabel("Time (microseconds)")
			pressure.set_ylabel("Voltage (mV)")
			pressure.set_title("Envelope of Analytic Signal")
			if printPlots.partial:
				newFPlot = []
				newFFTPlot = []
				for i in range(1, len(inputCalculations.fPlot)//40):
					newFPlot.append(inputCalculations.fPlot[i])
					newFFTPlot.append(calcFFT.F2[i])
				FFT.plot(newFPlot, newFFTPlot)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			else:
				FFT.plot(inputCalculations.fPlot, calcFFT.F2)
				FFT.set_xlabel("Frequency (MHz)")
				FFT.set_ylabel("Voltage (mV)")
				FFT.set_title("Frequency Spectrum")
			plt.tight_layout()
			plt.show()


def printResults():
	print()
	print("Results:")
	print("Calculated time of flight velocity (m/s): ", calcFlightTime.velocitySample)
	print("Attenuation from time domain (dB/cm) at center frequency of", calcFFT.centerFrequency, "MHz: ", calcAttenuation.attcmd)


def saveResults(firstFlag):  #This will save in the folder that the code is saved to.
	valid = 1
	while valid:
		saveInput = input("Do you want to save the results for the final set of plots? [y/n] ")	
		if saveInput == 'y':
			#root = tk.Tk()
			#root.withdraw()
			#savePath = fd.asksaveasfilename(title = "Select a folder where you want the file to be saved")

			#name = "_Results_" + str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")) + ".txt"
			#file = open(savePath + name, 'w')
			#file.write("Results for " + os.path.basename(filePathRetreval.filePath2) + "\n")
			#file.write("Calculated time of flight velocity (m/s): " + str(calcFlightTime.velocitySample) + "\n")
			#file.write("Attenuation from time domain (dB/cm): " + str(calcAttenuation.attcmd) + "\n")
			#file.write("Center frequency: " + str(calcFFT.centerFrequency))
			#file.close()
			valid = 0
			if firstFlag:
				saveResults.allVelocities = []
				saveResults.allAttenuation = []
				saveResults.allFrequencies = []
				saveResults.fileNames = []
			saveResults.allVelocities.append(calcFlightTime.velocitySample)
			saveResults.allAttenuation.append(calcAttenuation.attcmd)
			saveResults.allFrequencies.append(calcFFT.centerFrequency)
			saveResults.fileNames.append(os.path.basename(filePathRetreval.filePath2))

		elif saveInput == 'n': 
			valid = 0
		else:
			print("Invalid selection.")
			print()

		
def finalPlots():
	plt.figure()
	maxVelocity = max(saveResults.allVelocities)
	minVelocity = min(saveResults.allVelocities)
	meanVelocity = np.mean(saveResults.allVelocities)
	minFrequency = min(saveResults.allFrequencies)
	maxFrequency = max(saveResults.allFrequencies)
	for i in range(0, len(saveResults.allFrequencies)):
		plt.plot(saveResults.allFrequencies[i], saveResults.allVelocities[i], '*')
		plt.text(saveResults.allFrequencies[i]+0.05, saveResults.allVelocities[i]-0.01, saveResults.fileNames[i])
	plt.title("Frequency vs Velocity of Sound")
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Velocity (m/s)")
	#plt.text(minFrequency, maxVelocity, "The average velocity is " + str(round(meanVelocity, 2)) + " m/s")
	print()
	print("Mean Velocity: ", meanVelocity)


	plt.figure()
	coefficients = [0, 0]
	for i in range(0, len(saveResults.allFrequencies)):
		plt.plot(saveResults.allFrequencies[i], saveResults.allAttenuation[i], '*')
		plt.text(saveResults.allFrequencies[i]+0.05, saveResults.allAttenuation[i]-0.01, saveResults.fileNames[i])
	if len(saveResults.allFrequencies) > 1:
		coefficients = np.polyfit(saveResults.allFrequencies, saveResults.allAttenuation, 1) #Generates coefficients
		#print(coefficients)
		linearFunction = np.polyval(coefficients, saveResults.allFrequencies) #Generates linear fit
		#print(linearFunction)
		plt.plot(saveResults.allFrequencies, linearFunction) #Plots linear fit
	plt.title("Linear Frequecy vs Attenuation")
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Attenuation (dB/cm)")
	#plt.text(minFrequency, maxVelocity, "The average velocity is " + str(round(meanVelocity, 2)) + " m/s \nSlope = " + str(p[0]) + " dB/cm/MHz		Intercept = " + str(p[1]) + " dB/cm")
	#plt.text(minFrequency, maxVelocity, "Attenuation fit at 1 MHz = " + str(round((coefficients[0] + coefficients[1]), 2)) + " dB/cm		Attenuation fit at 1 MHz = " + str(round((coefficients[0] + coefficients[1])/8.686, 2)) + " np/cm")
	print()
	print("Linear Fit Information")
	print("Slope: ", coefficients[0], "dB/cm/MHz")
	print("Intercept: ", coefficients[1], "dB/cm")
	print("Attenuation at 1 MHz according to the linear fit: ", np.polyval(coefficients, 1), "dB/cm")
	print("Attenuation at 1 MHz according to the linear fit: ", np.polyval(coefficients, 1) * 0.1151277918, "np/cm")
	
	
	plt.figure()
	coefficients = [0, 0]
	logAttenuation = np.log(saveResults.allAttenuation)
	for i in range(0, len(logAttenuation)):
		plt.plot(saveResults.allFrequencies[i], logAttenuation[i], '*')
		plt.text(saveResults.allFrequencies[i] + 0.05, logAttenuation[i] - 0.01, saveResults.fileNames[i])
	if len(saveResults.allFrequencies) > 1:
		#logFrequencies = np.log(saveResults.allFrequencies)
		#print(saveResults.allAttenuation)
		#print(logAttenuation)
		coefficients = np.polyfit(saveResults.allFrequencies, logAttenuation, 1) #Generates coefficients
		#print(coefficients)
		logFunction = np.polyval(coefficients, saveResults.allFrequencies) #Generates log fit
		#print(logFunction)
		plt.plot(saveResults.allFrequencies, logFunction) #Plots linear fit
	plt.title("Logarithmic Frequency vs Attenuation")
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Attenuation (dB/cm)")
	print()
	print("Log Fit Information")
	print("Exponent: ", coefficients[0], "dB/cm/MHz")
	print("Attenuation at 1 MHz according to the linear fit: ", np.polyval(coefficients, 1), "dB/cm")
	print("Attenuation at 1 MHz according to the linear fit: ", np.polyval(coefficients, 1) * 0.1151277918, "np/cm")
	plt.show()


repeat = 1
firstFlag = 1
ii = 0 #Number of samples counter
savedt = 0

while repeat:
	#if firstFlag:
	#	fileTypeMenu()
	filePathRetreval()
	dataExtraction()
	windowSelection()
	if firstFlag:
		userInputValues()
	inputCalculations()
	calcFFT()
	calcFlightTime()
	faceReflectionLoss()
	calcAttenuation()
	printResults()
	if firstFlag:
		printPlots.firstTimeThrough = 1
	printPlots()
	saveResults(firstFlag)


	firstFlag = 0

	valid = 1
	while valid:
		additionalSample = input("Do you have another sample you want to run? [y/n]: ")
		if additionalSample == 'y':
			repeat = 1
			valid = 0
			print()
		elif additionalSample == 'n':
			repeat = 0
			valid = 0
			print()
		else:
			print("Invalid selection. Please select 'y' for yes or 'n' for no.")
			print()
try:
	finalPlots()
except:
	print("Nothing was saved to the final results plot.")