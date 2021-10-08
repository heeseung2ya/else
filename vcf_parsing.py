f_vcf = "/data/home/hhs6549/week3/vcf_per_chr/NA12878.vcf"
fr_vcf = open(f_vcf, "r")

header = ""
l_ChrName = []
for line in fr_vcf:
    if line.startswith("#"):
        header += line
    else:
        line = line.strip()
        if line.split()[0] not in l_ChrName:
            l_ChrName.append(line.split()[0])
            fw_chr = f"/data/home/hhs6549/week3/vcf_per_chr/NA12878_{line.split()[0]}.vcf"
            fw = open(fw_chr, "w")
            fw.write(f"{header}")
        fw.write(f"{line}\n")

fr_vcf.close()
fw.close()
