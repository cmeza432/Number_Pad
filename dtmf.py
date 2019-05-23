"""
Name:           Carlos Meza
Description:
 
"""

from scipy.signal import freqz
from scipy.signal import spectrogram
import numpy as np
import matplotlib.pyplot as plt

# Numeric values of added frequencies
number_pad_freq = [2277, 1906, 2033, 2174, 1979, 2106, 2247, 2061, 2188, 2329, 2150, 2418]
# String value for corresponding added frequencies
number_pad = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]
# Single values of frequencies
frequencies = [697, 770, 852, 941, 1209, 1336, 1477]

# Function returns the filter coefficients--> h[n]
def filt(bp, n):
    return (2 / L)* np.cos((2 * np.pi * bp * n) / fs)

# Populate the array with values from i to L
def populate(name, bp):
    # Populate result from filter function
    i = 0
    for i in range(L):
        name[i] = filt(bp, i)
    return name

def plot_y(var):
    return fs * var / (2 * np.pi)

def plot_frequencies(name, x):
    plt.figure(0)
    # Plot 697 frequency
    x, y = freqz(name[0], 1)
    x = plot_y(x)
    plt.plot(x, abs(y))    
    # Plot 770 frequency
    x, y = freqz(name[1], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plot 852 frequency
    x, y = freqz(name[2], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plot 941 frequency
    x, y = freqz(name[3], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plot 1209 frequency
    x, y = freqz(name[4], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plot 1336 frequency
    x, y = freqz(name[5], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plot 1477 frequency
    x, y = freqz(name[6], 1)
    x = plot_y(x)
    plt.plot(x, abs(y)) 
    # Plotting labels
    plt.title("Frequency Responses of Bandpass Filters")
    plt.xlabel("Hertz")
    plt.show()    

def processTones(name, L, fs, samplesPerTone):
    # Create empty arrays for appending
    result = []
    # X value for plotting
    x = np.arange(0, 1, 1/samplesPerTone)

    
    # Read values from csv file
    data = np.genfromtxt(name, delimiter=',')
    data = np.array(data, dtype=float)
    
    # Amount of number typed
    N = int(len(data)/samplesPerTone)
    
    # Constants
    counter = 0
    place = 0
    row_1 = np.ones(L)
    row_2 = np.ones(L)
    row_3 = np.ones(L)
    row_4 = np.ones(L)
    col_1 = np.ones(L)
    col_2 = np.ones(L)
    col_3 = np.ones(L)
    
    # Get filter coefficients
    coef = [populate(row_1, frequencies[0]),
            populate(row_2, frequencies[1]),
            populate(row_3, frequencies[2]),
            populate(row_4, frequencies[3]),
            populate(col_1, frequencies[4]),
            populate(col_2, frequencies[5]),
            populate(col_3, frequencies[6])]
    
    # Loop for each number of digits in csv file
    while(counter != N):
        # Create temp data to increment
        temp_data = data[place:(place + samplesPerTone)]
        
        # Convolve values
        y = [np.convolve(temp_data, coef[0]),
             np.convolve(temp_data, coef[1]),
             np.convolve(temp_data, coef[2]),
             np.convolve(temp_data, coef[3]),
             np.convolve(temp_data, coef[4]),
             np.convolve(temp_data, coef[5]),
             np.convolve(temp_data, coef[6])]
        
        # Store all values of mean into one array to loop
        mean_values = [np.mean(y[0]**2),
                       np.mean(y[1]**2),
                       np.mean(y[2]**2),
                       np.mean(y[3]**2),
                       np.mean(y[4]**2),
                       np.mean(y[5]**2),
                       np.mean(y[6]**2)]
        
        # Get index of max values to search in list of frequency values
        temp1 = mean_values[0:4].index(max(mean_values[0:4]))
        temp2 = mean_values[4:7].index(max(mean_values[4:7])) + 4
        total = frequencies[temp1] + frequencies[temp2]

        # Use total frequency to find find index to append string from saved array above
        position = number_pad_freq.index(total)
        result.append(number_pad[position])
        
        # Increment the while loop and place position
        place += samplesPerTone
        counter += 1

    plot_frequencies(coef, x)
    # Plot Spectogram
    plt.figure(1)
    f, t, Sxx = spectrogram(data, fs)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    return ''.join(result)

#############  main  #############
if __name__ == "__main__":
    filename = "tones-123456789star0pound.csv"  #  name of file to process, change according the excel file name
    L = 64                  #  filter length
    fs = 8000               #  sampling rate
    samplesPerTone = 4000   #  4000 samples per tone, 
                            #    NOT the total number of samples per signal

    # returns string of telephone buttons corresponding to tones
    phoneNumber = processTones(filename, L, fs, samplesPerTone)
    
    print(phoneNumber)