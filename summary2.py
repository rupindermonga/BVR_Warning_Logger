import os, re, copy, time, pandas as pd


path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'


def readingLog(file):
    start_time = time.time()
    updated_file = os.path.join(path, file) 
    with open(updated_file) as f:
        f = f.readlines()
    total_features = 0
    feature_dict = {}
    feature_summary ={}
    product_details = {}
    total_summary = {}
    new_product = ""
    old_product = ""
    negative_count = 0
    positive_count = 0
    neutral_count = 0
    negative_total_count = 0
    neutral_total_count = 0
    positive_total_count = 0
    total_total_count = 0
    eachFeature_count = 0
    total_count = 0
    for line in f:
        if "Pulled data for " in line:
            category = re.findall(r'"([^"]*)"', line)[-1]
            break
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
    # feature_dict["total"] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
    for eachFeature in feature_list:
        feature_dict[eachFeature] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
        feature_summary[eachFeature] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
    feature_dict_copy = copy.deepcopy(feature_dict)
    product_details[category] = [{"total": "", "negative": "", "neutral": "", "positive": ""}, feature_dict_copy]
    product_details["total"] = [{"total": 0, "negative": 0, "neutral": 0, "positive": 0}, feature_dict_copy]
    for line in f:
        if "Scoring product" in line:
            new_product = re.findall(r'"([^"]*)"', line)[-1]
        if "feature_mentions" in line:
            if "negative: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    # feature_summary[eachFeature]["negative"] += feature_dict[eachFeature]["negative"]
                    if old_product != new_product:
                        # for eachFeature in feature_list:
                        feature_summary[eachFeature]["negative"] += feature_dict[eachFeature]["negative"]
                        feature_dict[eachFeature]["negative"] = 0
                    feature_dict[eachFeature]["negative"] += eachFeature_count
                    feature_dict[eachFeature]["total"] = feature_dict[eachFeature]["negative"]
                neg_count = line.find("negative: :") + len("negative: :")
                if old_product != new_product:
                    negative_total_count += negative_count
                    negative_count = 0
                negative_count += int(line[neg_count:neg_count+3].replace(" ","").replace(",",""))    
            if "neutral: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_summary[eachFeature]["neutral"] += feature_dict[eachFeature]["neutral"]
                        feature_dict[eachFeature]["neutral"] = 0
                    feature_dict[eachFeature]["neutral"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["neutral"]
                neu_count = line.find("neutral: :") + len("neutral: :")
                if old_product != new_product:
                    neutral_total_count += neutral_count
                    neutral_count = 0
                neutral_count += int(line[neu_count:neu_count+3].replace(" ","").replace(",",""))
            if "positive: :" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_summary[eachFeature]["positive"] += feature_dict[eachFeature]["positive"]
                        feature_dict[eachFeature]["positive"] = 0
                    feature_dict[eachFeature]["positive"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["positive"]
                pos_count = line.find("positive: :") + len("positive: :")
                if old_product != new_product:
                    positive_total_count += positive_count
                    positive_count = 0
                    old_product = new_product
                positive_count += int(line[pos_count:pos_count+3].replace(" ","").replace(",",""))
                feature_dict_copy = copy.deepcopy(feature_dict)
        total_count = negative_count + neutral_count + positive_count
        
        product_details[new_product] = [{"total": total_count, "negative": negative_count, "neutral": neutral_count, "positive": positive_count}, feature_dict_copy]
    
    for eachFeature in feature_list:
        feature_summary[eachFeature]["negative"] += feature_dict[eachFeature]["negative"]
        feature_summary[eachFeature]["neutral"] += feature_dict[eachFeature]["neutral"]
        feature_summary[eachFeature]["positive"] += feature_dict[eachFeature]["positive"]
        feature_summary[eachFeature]["total"]  = feature_summary[eachFeature]["negative"] + feature_summary[eachFeature]["neutral"] + feature_summary[eachFeature]["positive"]
        total_summary[eachFeature] = feature_summary[eachFeature]["negative"] + feature_summary[eachFeature]["neutral"] + feature_summary[eachFeature]["positive"]
    negative_total_count += negative_count
    neutral_total_count += neutral_count
    positive_total_count += positive_count
    total_total_count = negative_total_count + neutral_total_count + positive_total_count
    product_details["total"] = [{"total": total_total_count, "negative": negative_total_count, "neutral": neutral_total_count, "positive": positive_total_count}, feature_summary]
    product_details[category] = [{"total": "", "negative": "", "neutral": "", "positive": ""}, total_summary]
    product_details.pop('')
    df = pd.DataFrame.from_dict(product_details, orient='index')
    
    df2 = pd.concat([df.drop([0,1], axis=1), df[0].apply(pd.Series), df[1].apply(pd.Series)], axis=1)
    df2_columns = list(df2.columns.values)
    
    data = pd.DataFrame( columns=df2_columns)
    pd.concat([pd.DataFrame(data), df2])
    
    df2.to_csv("data.csv")
    return time.time() - start_time

final = readingLog('BVRScoring.2020-06-13_132713841860.log')

print(final)
