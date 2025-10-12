from input_check import input_check
from Protein_Database import AMINO_ACID_PROPERTIES


def calculate_weighted_properties(hit_sequence):
    Gh, Gw, Gp = 0, 0, 0

    # invoke input_check to calculate the average properties
    avg_h = input_check(hit_sequence)['average_hydrophobicity']
    avg_w = input_check(hit_sequence)['average_molecular_weight']
    avg_p = input_check(hit_sequence)['average_isoelectric_point']

    # 计算每种特性与平均值的最大差值
    max_h = max([abs(AMINO_ACID_PROPERTIES[j]['hydrophobicity'] - avg_h) for j in AMINO_ACID_PROPERTIES])
    max_w = max([abs(AMINO_ACID_PROPERTIES[j]['molecular_weight'] - avg_w) for j in AMINO_ACID_PROPERTIES])
    max_p = max([abs(AMINO_ACID_PROPERTIES[j]['isoelectric_point'] - avg_p) for j in AMINO_ACID_PROPERTIES])

    # 特定位置的索引
    specific_position = [0, 2, 13]

    for i in specific_position:

        j = hit_sequence[i]  # 提取特定位置的氨基酸
        if j in AMINO_ACID_PROPERTIES:  # 确保氨基酸在特性字典中
            h_k = AMINO_ACID_PROPERTIES[j]['hydrophobicity']
            w_k = AMINO_ACID_PROPERTIES[j]['molecular_weight']
            p_k = AMINO_ACID_PROPERTIES[j]['isoelectric_point']

            # 累加计算加权得分
            Gh += (1 - (abs(h_k - avg_h) / max_h))
            Gw += (1 - (abs(w_k - avg_w) / max_w))
            Gp += (1 - (abs(p_k - avg_p) / max_p))


    # 归一化得分
    Gh = Gh + 1 / 14
    Gw = Gw + 1 / 14
    Gp = Gp + 1 / 14
    G = (Gh + Gw + Gp) / 3

    return {
        'GH': Gh,
        'GW': Gw,
        'GP': Gp,
        'G': G
    }