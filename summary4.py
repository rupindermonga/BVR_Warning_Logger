import os, re, copy, time, pandas as pd


path = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/logs'




def readingLog1(file):
    start_time = time.time()
    feature_list =[]
    updated_file = os.path.join(path,file)
    format_type = 0
    total_features = 0
    feature_dict = {}
    feature_summary ={}
    product_details = {}    
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

    with open(updated_file) as f:
        f = f.readlines()
    for line in f:
        if "Pulled data for " in line:
            category = re.findall(r'"([^"]*)"', line)[-1]
            break
    for line in f:
        if "feature_mentions" in line:
            new_line = line.split(',')
            for eachItem in new_line:
                new_item = eachItem.strip().split(':')
                if len(new_item) == 2:
                    if new_item[0] != '':
                        feature_list.append(new_item[0])
                    else:
                        format_type +=1
            break    
    for eachFeature in feature_list:
        feature_dict[eachFeature] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
        feature_summary[eachFeature] = {"negative": 0, "neutral": 0, "positive": 0, "total": 0}
    feature_dict_copy = copy.deepcopy(feature_dict)
    product_details["total"] = [{"total": 0, "negative": 0, "neutral": 0, "positive": 0}, feature_dict_copy]
    for line in f:
        if "Scoring product" in line:
            new_product = re.findall(r'"([^"]*)"', line)[-1]
        if "feature_mentions" in line:
            if "negative:" in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_summary[eachFeature]["negative"] += feature_dict[eachFeature]["negative"]
                        feature_dict[eachFeature]["negative"] = 0
                    feature_dict[eachFeature]["negative"] += eachFeature_count
                    feature_dict[eachFeature]["total"] = feature_dict[eachFeature]["negative"]
                if old_product != new_product:
                    negative_total_count += negative_count
                    negative_count = 0
                if format_type == 0:
                    neg_count = line.find("negative: :") + len("negative: :")
                    negative_count += int(line[neg_count:neg_count+3].replace(" ","").replace(",",""))    
                else:
                    new_line = line.split(',')
                    for eachItem in new_line:
                        new_item =eachItem.strip().split(':')
                        if len(new_item) == 2 and new_item[0] == '':
                            negative_count += int(new_item[1])    
                            break
            if "neutral: " in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_summary[eachFeature]["neutral"] += feature_dict[eachFeature]["neutral"]
                        feature_dict[eachFeature]["neutral"] = 0
                    feature_dict[eachFeature]["neutral"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["neutral"]
                if old_product != new_product:
                    neutral_total_count += neutral_count
                    neutral_count = 0
                if format_type == 0:
                    neu_count = line.find("neutral: :") + len("neutral: :")
                    neutral_count += int(line[neu_count:neu_count+3].replace(" ","").replace(",",""))
                else:
                    new_line = line.split(',')
                    for eachItem in new_line:
                        new_item =eachItem.strip().split(':')
                        if len(new_item) == 2 and new_item[0] == '':
                            neutral_count += int(new_item[1])    
                            break
            if "positive: " in line:
                for eachFeature in feature_list:
                    feature_position = line.find(eachFeature) + len(eachFeature) + 1
                    eachFeature_count = int(line[feature_position:feature_position+3].replace(" ","").replace(",",""))
                    if old_product != new_product:
                        feature_summary[eachFeature]["positive"] += feature_dict[eachFeature]["positive"]
                        feature_dict[eachFeature]["positive"] = 0
                    feature_dict[eachFeature]["positive"] += eachFeature_count
                    feature_dict[eachFeature]["total"] += feature_dict[eachFeature]["positive"]
                if old_product != new_product:
                    positive_total_count += positive_count
                    positive_count = 0
                    old_product = new_product
                if format_type == 0:
                    pos_count = line.find("positive: :") + len("positive: :")
                    positive_count += int(line[pos_count:pos_count+3].replace(" ","").replace(",",""))
                else:
                    new_line = line.split(',')
                    for eachItem in new_line:
                        new_item =eachItem.strip().split(':')
                        if len(new_item) == 2 and new_item[0] == '':
                            positive_count += int(new_item[1])    
                            break
                
                feature_dict_copy = copy.deepcopy(feature_dict)
        total_count = negative_count + neutral_count + positive_count
        
        product_details[new_product] = [{"total": total_count, "negative": negative_count, "neutral": neutral_count, "positive": positive_count}, feature_dict_copy]
    
    for eachFeature in feature_list:
        feature_summary[eachFeature]["negative"] += feature_dict[eachFeature]["negative"]
        feature_summary[eachFeature]["neutral"] += feature_dict[eachFeature]["neutral"]
        feature_summary[eachFeature]["positive"] += feature_dict[eachFeature]["positive"]
        feature_summary[eachFeature]["total"]  = feature_summary[eachFeature]["negative"] + feature_summary[eachFeature]["neutral"] + feature_summary[eachFeature]["positive"]
    
    negative_total_count += negative_count
    neutral_total_count += neutral_count
    positive_total_count += positive_count
    total_total_count = negative_total_count + neutral_total_count + positive_total_count
    product_details["total"] = [{"total": total_total_count, "negative": negative_total_count, "neutral": neutral_total_count, "positive": positive_total_count}, feature_summary]
    product_details.pop('')
    df = pd.DataFrame.from_dict(product_details, orient='index')
    
    df2 = pd.concat([df.drop([0,1], axis=1), df[0].apply(pd.Series), df[1].apply(pd.Series)], axis=1)
    df2_columns = list(df2.columns.values)

    
    data = pd.DataFrame( columns=df2_columns)
    df2 = pd.concat([pd.DataFrame(data), df2])
    df2.to_csv("data.csv")
    ##
    df = pd.read_csv("data.csv")
    df_column_name = df.columns.values
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()
    df6 = pd.DataFrame()
    for i, eachC in enumerate(df_column_name):
        if i <= 4:
            df3 = pd.concat([df3, df[eachC]], axis = 1)
        else:
            df4[eachC] = df[eachC].apply(lambda x : dict(eval(x)))
            df5 = df4[eachC].apply(pd.Series)
            df5_column_names = df5.columns.values
            column_tuple = []
            for eachColumn in df5_column_names:
                new_tuple = [eachC]
                new_tuple.append(eachColumn)
                new_tuple = tuple(new_tuple)
                column_tuple.append(new_tuple)
            a = column_tuple
            df5.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])
            df6 = pd.concat([df6, df5], axis = 1)
    final_df = pd.concat([df3, df6], axis = 1)
    final_df_column = final_df.columns.values
    final_df_column_tuple = []
    for eachColumn in final_df_column:
        if type(eachColumn) == str:
            new_tuple = (eachColumn,'')
        else:
            new_tuple = eachColumn
        final_df_column_tuple.append(new_tuple)
    a = final_df_column_tuple

    final_df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])
    final_df = final_df.rename(columns = {'Unnamed: 0': category })
    os.remove("data.csv")
    final_df.to_csv(category + '.csv')
    
    return time.time() - start_time
    

final = readingLog1('BVRScoring.2020-06-13_140825661877.log')

print(final)
