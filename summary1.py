import os, re, copy, time, pandas as pd


path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'


def readingLog(file):
    start_time = time.time()
    updated_file = os.path.join(path, file) 
    with open(updated_file) as f:
        f = f.readlines()
    total_features = 0
    feature_dict = {}
    product_details = {}
    new_product = ""
    old_product = ""
    negative_count = 0
    positive_count = 0
    neutral_count = 0
    eachFeature_count = 0
    total_count = 0
    for line in f:
        if "feature_mentions" in line:
            total_features = line.count(":") - 5
            position = len(line)
            feature_list = []
            for i in range(total_features):
                position = line.rfind(':', 0, position)
                co_position = line.rfind(",",0,position)
                feature_list.append(line[co_position+2:position])
                position -= 1
            break
    for eachFeature in feature_list:
        feature_dict[eachFeature] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
    feature_dict_copy = copy.deepcopy(feature_dict)
    for line in f:
        if "Scoring product" in line:
            new_product = re.findall(r'"([^"]*)"', line)[-1]
        if "feature_mentions" in line:
            if "negative: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_dict[eachFeature]["negative"] = 0
                    feature_dict[eachFeature]["negative"] += eachFeature_count
                    feature_dict[eachFeature]["total"] = feature_dict[eachFeature]["negative"]
                neg_count = line.find("negative: :") + len("negative: :")
                if old_product != new_product:
                    negative_count = 0
                negative_count += int(line[neg_count:neg_count+3].replace(" ","").replace(",",""))    
            if "neutral: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_dict[eachFeature]["neutral"] = 0
                    feature_dict[eachFeature]["neutral"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["neutral"]
                neu_count = line.find("neutral: :") + len("neutral: :")
                if old_product != new_product:
                    neutral_count = 0
                neutral_count += int(line[neu_count:neu_count+3].replace(" ","").replace(",",""))
            if "positive: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_dict[eachFeature]["positive"] = 0
                    feature_dict[eachFeature]["positive"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["positive"]
                pos_count = line.find("positive: :") + len("positive: :")
                if old_product != new_product:
                    positive_count = 0
                    old_product = new_product
                positive_count += int(line[pos_count:pos_count+3].replace(" ","").replace(",",""))
                feature_dict_copy = copy.deepcopy(feature_dict)
        total_count = negative_count + neutral_count + positive_count
        product_details[new_product] = [{"total": total_count, "negative": negative_count, "neutral": neutral_count, "positive": positive_count}, feature_dict_copy]
    product_details.pop('')
    df = pd.DataFrame.from_dict(product_details, orient='index')
    
    df2 = pd.concat([df.drop([0,1], axis=1), df[0].apply(pd.Series), df[1].apply(pd.Series)], axis=1)

    df2.to_csv("data.csv")
    return time.time() - start_time

final = readingLog('BVRScoring.2020-06-13_132713841860.log')

print(final)
