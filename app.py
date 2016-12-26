from flask import Flask, render_template
import os

app = Flask(__name__)

def getProcessInfo():
    response = os.popen('top -b -n1').readlines()
    return response[1].split()

#function that returns IP Address
def getIpAddress():
    response = os.popen('hostname -I').readline()
    return response.split()

# function that returns username
#def getUserName():
#    response = os.popen('users').readline()
#    return response

# function that returns memory usage in MBs
def getMemoryUsage(lineNumber):
    response = os.popen('free -m').readlines()
    return response[lineNumber].split()

# function that returns how long the raspberry pi has been running
def getUptime():
    response = os.popen('cat /proc/uptime').readline().split() # reads the response as an array of strings for each line
    minutes = int(float(response[0])/60)
    time = [0, 0, 0]
    time[0] = int(minutes / 24 / 60) # get days
    time[1] = int(minutes /60 % 24) # get hours
    time[2] = minutes % 60 # get minutes
    return time

# function that returns disk usage
def getDiskUsage(lineNumber):
	response = os.popen('df -h').readlines() # reads the response as an array of strings for each line
	return response[lineNumber].split() # splits a specific line into an array of words based on lineNumber

# function that returns cpu temperature in fahrenheit
def getFahrenheit():
	response = os.popen('vcgencmd measure_temp').readline() # get the response from running the command 'vcgencmd measure_temp'
	celsius = float(response.replace("temp=","").replace("'C\n","")) # get rid of 'temp=' and ''C'
	fahrenheit = round(((celsius * (9/5)) + 32),1) # convert from fahrenheit to celsius rounded to one decimal place
	return fahrenheit

# function that returns cpu temperature in celsius
def getCelsius():
	response = os.popen('vcgencmd measure_temp').readline() # get the response from running the command 'vcgencmd measure_temp'
	celsius = float(response.replace("temp=","").replace("'C\n","")) # get rid of 'temp=' and ''C'
	celsius = round(celsius,1) # celsius rounded to one decimal place
	return celsius

@app.route('/')
def index():
	return render_template('index.html', 
                           fahrenheit=getFahrenheit(),
                           celsius=getCelsius(),
                           diskUsageHeader=getDiskUsage(0), # array for Disk Usage <th>
                           diskUsageInfo=getDiskUsage(1), # array for Disk Usage <td>
                           upTime=getUptime(), # how long the raspberry pi has been running
                           memoryUsageHeader=getMemoryUsage(0), # array for Memory Usage <th>
                           memoryUsageInfo=getMemoryUsage(1), # array for Memory Usage <td>
                           memoryUsePercentage=round(float(getMemoryUsage(1)[2]) / float(getMemoryUsage(1)[1]), 4) * 100, # percentage of used Memory
#                           userName=getUserName(),
                           ipAddress=getIpAddress()[0],
                           processInfo=getProcessInfo()
                          )

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=80)
