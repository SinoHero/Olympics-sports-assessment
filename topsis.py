import numpy as np
import pandas as pd

def rescale_dict_values(dictionary):
    # Step 1: Find the minimum and maximum values in the dictionary
    min_val = min(dictionary.values())
    max_val = max(dictionary.values())
    
    # Step 2: Rescale the values
    rescaled_dict = {key: (value - min_val) / (max_val - min_val) for key, value in dictionary.items()}
    
    return rescaled_dict

def topsis(data, headers):
    # 转换为 DataFrame
    df = pd.DataFrame(data, columns=headers)

    # 提取矩阵 A 和运动项目名称
    A = df.iloc[:, 1:].values
    sports = df['Sport'].values

    # 数据行列尺寸
    n, m = A.shape

    # 计算熵权
    p = (A + np.finfo(float).eps) / np.sum(A + np.finfo(float).eps, axis=0)
    p[p == 0] = np.finfo(float).eps  # 避免 log(0)
    entropy = -np.sum(p * np.log(p), axis=0) / np.log(n)
    weight = (1 - entropy) / np.sum(1 - entropy)

    print("Weight:")
    print(weight)

    # 计算正理想解和负理想解
    positive_ideal = np.max(A, axis=0)  # 每列最大值
    negative_ideal = np.min(A, axis=0)  # 每列最小值

    # 计算每个样本到正负理想解的距离
    diff_positive = A - positive_ideal
    diff_negative = A - negative_ideal

    # 修正可能的负数平方根问题
    distance_to_positive = np.sqrt(np.maximum(np.sum((diff_positive**2) * weight, axis=1), 0))
    distance_to_negative = np.sqrt(np.maximum(np.sum((diff_negative**2) * weight, axis=1), 0))

    # 计算 TOPSIS 分数
    topsis_scores = distance_to_negative / (distance_to_positive + distance_to_negative)

    # 转换为 DataFrame 输出
    results = pd.DataFrame({'Sport': sports, 'Topsis_Score': topsis_scores})



    return weight, results