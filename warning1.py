import os, re

path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'

# file = 'BVRScoring.2020-06-13_132713841860.log'


def readingLog(file):
    updated_file = os.path.join(path, file) 
    with open(updated_file) as f:
        f = f.readlines()
    
    warnings =[]
    warning_details = []
    for line in f:
        if "WARNING - " in line:
            a, b = line.split("WARNING - ", 1)
            b = b.strip()
            warnings.append(b)
            warning_details.append(re.findall(r'"([^"]*)"', b)[-1])
    return warning_details

# final = readingLog('BVRScoring.2020-06-13_140234917390.log')
# final = readingLog('BVRScoring.2020-06-13_140825661877.log')
final = readingLog('BVRScoring.2020-06-13_142730671371.log')
# final = readingLog('BVRScoring.2020-06-13_151243066266.log')
print(final)
