# How to run this code:
# $ python3 Statistics.py [read1_filename] [read2_filename] -o [output_filename]


import sys
import gzip


def manual():
    if len(sys.argv) == 5 and sys.argv[3] == "-o":
        read1_filename = sys.argv[1]
        read2_filename = sys.argv[2]
        output_filename = sys.argv[4]
        if "/" in sys.argv[1]:
            sample_name = sys.argv[1].split("/")[-1]
        else:
            sample_name = sys.argv[1]
        print(f"read1: {read1_filename}")
        print(f"read2: {read2_filename}\n")
        main(sample_name, read1_filename, read2_filename, output_filename)
    elif len(sys.argv) == 2 and (
        sys.argv[1] == "-h" or sys.argv[1] == "--help"
    ):
        print(
            f"USAGE\n  python3 {sys.argv[0]} [read1_filename] [read2_filename] -o [output_filename]"
        )
        sys.exit(2)
    else:
        print(
            "!!! Argument Error !!!\n  Use '-h' or '--help' to print detailed descriptions of command line arguments"
        )
        sys.exit(1)


def open_file(read1_filename, read2_filename):
    format = read1_filename.split(".")[-1]
    if format == "gz":
        read1 = gzip.open(read1_filename, "rb")
        read2 = gzip.open(read2_filename, "rb")
    elif format == "fastq" or format == "fq":
        read1 = open(read1_filename, "r")
        read2 = open(read2_filename, "r")
    return format, read1, read2


def close_file(read1, read2):
    read1.close()
    read2.close()


def make_file(d_sum_result, output_filename):
    print(f"*** Writing sqs file ***\noutput file: {output_filename}")
    w_sqs = open(output_filename, "w")
    w_sqs.write(
        "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            d_sum_result["sample_name"],
            d_sum_result["total_read_bases"],
            d_sum_result["total_reads"],
            d_sum_result["n_percent"],
            d_sum_result["GC_contents"],
            d_sum_result["q20"],
            d_sum_result["q30"],
        )
    )
    w_sqs.write("SampleName : {}\n".format(d_sum_result["sample_name"]))
    w_sqs.write("Total A : {}\n".format(d_sum_result["count_A"]))
    w_sqs.write("Total C : {}\n".format(d_sum_result["count_C"]))
    w_sqs.write("Total G : {}\n".format(d_sum_result["count_G"]))
    w_sqs.write("Total T : {}\n".format(d_sum_result["count_T"]))
    w_sqs.write("Total N : {}\n".format(d_sum_result["count_N"]))
    w_sqs.write("Q30 Bases: {}\n".format(d_sum_result["q30_bases"]))
    w_sqs.write("Q30 Bases: {}\n".format(d_sum_result["q20_bases"]))
    w_sqs.close()
    print()


def readlines(sample_name, format, read):
    print("Please wait . . .")

    d_result = {
        "sample_name": sample_name.split(".")[0],
        "count_A": 0,
        "count_C": 0,
        "count_G": 0,
        "count_T": 0,
        "count_N": 0,
        "total_read_bases": 0,
        "total_reads": 0,
        "q20_bases": 0,
        "q30_bases": 0,
        "q20": 0,
        "q30": 0,
        "n_percent": 0,
        "GC_contents": 0,
    }

    line_idx = 0
    for line in read:
        if format == "gz":
            line = str(line, "utf-8").strip()
        else:
            line = line.strip()

        line_idx += 1
        if line_idx % 4 == 2:
            d_result["total_read_bases"] += len(line)
            d_result["count_A"] += line.count("A")
            d_result["count_C"] += line.count("C")
            d_result["count_G"] += line.count("G")
            d_result["count_T"] += line.count("T")
            d_result["count_N"] += line.count("N")
        elif line_idx % 4 == 0:
            for q in line:
                score = ord(q) - 33
                if score >= 20:
                    d_result["q20_bases"] += 1
                if score >= 30:
                    d_result["q30_bases"] += 1
    d_result["total_reads"] = line_idx // 4
    d_result["q20"] = d_result["q20_bases"] / d_result["total_read_bases"] * 100
    d_result["q30"] = d_result["q30_bases"] / d_result["total_read_bases"] * 100
    d_result["n_percent"] = (
        d_result["count_N"] / d_result["total_read_bases"] * 100
    )
    d_result["GC_contents"] = (
        (d_result["count_G"] + d_result["count_C"])
        / d_result["total_read_bases"]
        * 100
    )

    print_result(d_result)

    return d_result


def sum_read1_read2(d_read1_result, d_read2_result):
    print("*** Calculating read1 + read2 ***\nPlease wait . . .")

    d_sum_result = {
        "sample_name": "",
        "count_A": 0,
        "count_C": 0,
        "count_G": 0,
        "count_T": 0,
        "count_N": 0,
        "total_read_bases": 0,
        "total_reads": 0,
        "q20_bases": 0,
        "q30_bases": 0,
        "q20": 0,
        "q30": 0,
        "n_percent": 0,
        "GC_contents": 0,
    }
    for key in d_sum_result.keys():
        if (
            key == "sample_name"
            or key == "q20"
            or key == "q30"
            or key == "n_percent"
            or key == "GC_contents"
        ):
            pass
        else:
            d_sum_result[key] = d_read1_result[key] + d_read2_result[key]

    d_sum_result["sample_name"] = d_read1_result["sample_name"].split("_")[0]
    d_sum_result["q20"] = (
        (d_read1_result["q20_bases"] + d_read2_result["q20_bases"])
        / d_sum_result["total_read_bases"]
        * 100
    )
    d_sum_result["q30"] = (
        (d_read1_result["q30_bases"] + d_read2_result["q30_bases"])
        / d_sum_result["total_read_bases"]
        * 100
    )
    d_sum_result["n_percent"] = (
        d_sum_result["count_N"] / d_sum_result["total_read_bases"] * 100
    )
    d_sum_result["GC_contents"] = (
        (d_sum_result["count_G"] + d_sum_result["count_C"])
        / d_sum_result["total_read_bases"]
        * 100
    )
    print_result(d_sum_result)

    return d_sum_result


def check_under_point(d_result):
    for key, value in d_result.items():
        if "float" in str(type(value)):
            if value < 0.01:
                exp = 0
                while value < 1:
                    exp += 1
                    value *= 10
                d_result[key] = str(round(value, 1)) + "E-" + str(exp)
            else:
                d_result[key] = round(d_result[key], 2)
    return d_result


def print_result(d_result):
    print("*** result ***")
    d_result = check_under_point(d_result)
    print(
        "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
            d_result["sample_name"],
            d_result["total_read_bases"],
            d_result["total_reads"],
            d_result["n_percent"],
            d_result["GC_contents"],
            d_result["q20"],
            d_result["q30"],
        )
    )
    print("SampleName : {}".format(d_result["sample_name"]))
    print("Total A : {}".format(d_result["count_A"]))
    print("Total C : {}".format(d_result["count_C"]))
    print("Total G : {}".format(d_result["count_G"]))
    print("Total T : {}".format(d_result["count_T"]))
    print("Total N : {}".format(d_result["count_N"]))
    print("Q30 Bases: {}".format(d_result["q30_bases"]))
    print("Q20 Bases: {}".format(d_result["q20_bases"]))
    print()


def main(sample_name, read1_filename, read2_filename, output_filename):
    format, read1, read2 = open_file(read1_filename, read2_filename)

    print("*** Calculating read1 ***")
    d_read1_result = readlines(sample_name, format, read1)

    print("*** Calculating read2 ***")
    sample_name = sample_name.replace("_1", "_2")
    d_read2_result = readlines(sample_name, format, read2)

    d_sum_result = sum_read1_read2(d_read1_result, d_read2_result)

    make_file(d_sum_result, output_filename)

    close_file(read1, read2)
    print("\nFINISH !!!\n")


manual()
