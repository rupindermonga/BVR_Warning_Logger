import os, re, copy


path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'


def readingLog(file):
    updated_file = os.path.join(path, file) 
    with open(updated_file) as f:
        f = f.readlines()

    product_details = {}
    new_product = ""
    old_product = ""
    negative_count = 0
    positive_count = 0
    neutral_count = 0
    for line in f:
        if "Scoring product" in line:
            new_product = re.findall(r'"([^"]*)"', line)[-1]
        if "feature_mentions" in line:
            if "negative: :" in line:
                neg_count = line.find("negative: :") + len("negative: :")
                if old_product != new_product:
                    negative_count = 0
                negative_count += int(line[neg_count:neg_count+3].replace(" ","").replace(",",""))    
            if "neutral: :" in line:
                neu_count = line.find("neutral: :") + len("neutral: :")
                if old_product != new_product:
                    neutral_count = 0
                neutral_count += int(line[neu_count:neu_count+3].replace(" ","").replace(",",""))
            if "positive: :" in line:
                pos_count = line.find("positive: :") + len("positive: :")
                if old_product != new_product:
                    positive_count = 0
                    old_product = new_product
                positive_count += int(line[pos_count:pos_count+3].replace(" ","").replace(",",""))
        product_details[new_product] = {"negative": negative_count, "neutral": neutral_count, "positive": positive_count}
    product_details.pop('')
    return product_details

# final = readingLog('BVRScoring.2020-06-13_132713841860 (copy).log')
final = readingLog('check.log')
print(final)
