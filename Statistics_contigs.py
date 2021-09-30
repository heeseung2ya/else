# How to run this code:
# $ python3 Statistics_contigs.py [input_filename]

import sys

fasta_file = open(sys.argv[1], "r")

d_contigs_len = {}
for line in fasta_file:
    line = line.strip()
    if line.startswith(">"):
        d_contigs_len["_".join(line.split("_")[:2])[1:]] = int(
            line.split("_")[3]
        )

# Number of contigs
contigs_number = len(d_contigs_len)

# Total contig bases
total_contig_bases = sum(d_contigs_len.values())

l_sorted_contigs_len = sorted(
    d_contigs_len.items(), key=lambda x: x[1], reverse=True
)

# N50
sum_contigs = 0
for i in l_sorted_contigs_len:
    sum_contigs += i[1]
    if sum_contigs >= (total_contig_bases / 2):
        n50 = i[1]
        break

# Longest
longest = l_sorted_contigs_len[0][1]

# Shortest
shortest = l_sorted_contigs_len[-1][1]

# Average length
avg_len = total_contig_bases / contigs_number

# Write stat_file.txt
stat_file = open("stat.txt", "w")
stat_file.write(
    f"{contigs_number}\t{total_contig_bases}\t{n50}\t{longest}\t{shortest}\t{avg_len:.2f}"
)
print(
    f"{contigs_number}\t{total_contig_bases}\t{n50}\t{longest}\t{shortest}\t{avg_len}"
)

fasta_file.close()
stat_file.close()
