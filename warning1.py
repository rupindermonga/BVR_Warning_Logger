import os, re


path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'


def readingLog(file):
    updated_file = os.path.join(path, file) 
    with open(updated_file) as f:
        f = f.readlines()

    product_details = {}
    new_product = ""
    for line in f:
        if "Scoring product" in line:
            new_product = re.findall(r'"([^"]*)"', line)[-1]
        if "WARNING - " in line:
            a, b = line.split("WARNING - ", 1)
            b = b.strip()
            line = line.strip()
            if re.findall(r'"([^"]*)"', b)[-1] != "":
                if new_product != re.findall(r'"([^"]*)"', b)[-1]:
                    new_product = re.findall(r'"([^"]*)"', b)[-1]
            if new_product in product_details.keys():                        
                product_details[new_product].append(b)
            else:
                product_details[new_product] = [b]
    return product_details

final = readingLog('BVRScoring.2020-06-13_142730671371.log')

print(final)
