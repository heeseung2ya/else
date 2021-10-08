# TRR_Coding_TEST
# Using Python 3.8.8

from scipy.spatial import distance

fr = open("/data/home/hhs6549/TRR_Coding_TEST/TT_Set_A.csv", "r")
fw_dist = open("/data/home/hhs6549/TRR_Coding_TEST/HHS_HammingDist.txt", "w")
fw_freq = open("/data/home/hhs6549/TRR_Coding_TEST/HHS_HammingDist.Freq.txt", "w")

fw_dist.write("IndexSet")
l_IndexSet = []
fr.readline()
for line in fr:
    line = line.strip().split(",")
    l_IndexSet.append(f"{line[1]}+{line[2]}")
    fw_dist.write(f"\t{line[1]}+{line[2]}")

d_freq = {}
for row in l_IndexSet:
    fw_dist.write(f"\n{row}")
    row_split = [list(row.split("+")[0]), list(row.split("+")[1])]
    for col in l_IndexSet:
        col_split = [list(col.split("+")[0]), list(col.split("+")[1])]
        try:
            d_freq[
                f"{int(distance.hamming(row_split[0],col_split[0])*len(row_split[0]))}+{int(distance.hamming(row_split[1],col_split[1])*len(row_split[1]))}"
            ] += 1
        except:
            d_freq[
                f"{int(distance.hamming(row_split[0],col_split[0])*len(row_split[0]))}+{int(distance.hamming(row_split[1],col_split[1])*len(row_split[1]))}"
            ] = 1
        fw_dist.write(
            f"\t{int(distance.hamming(row_split[0],col_split[0])*len(row_split[0]))}+{int(distance.hamming(row_split[1],col_split[1])*len(row_split[1]))}"
        )

fw_freq.write("HammingDist_i7\tHammingDist_i5\tIndex_Count")

# python 3.7 이상 version부터 dictionary 값이 순서대로 뽑힘.
for key in d_freq:
    fw_freq.write(f"\n{key.split('+')[0]}\t{key.split('+')[1]}\t{d_freq[key]}")

fr.close()
fw_dist.close()
fw_freq.close()
