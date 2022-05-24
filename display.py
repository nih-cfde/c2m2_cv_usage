#! /usr/bin/env python
import sys
import argparse
import csv
import json
import pprint

dccs = ["KFDRC", "SPARC", "ERCC_DCC", "HMP", "4DN_DCIC", "GTEx", "IDG", "LINCS", "MW", "GlyGen", "HuBMAP"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_json', help='output of c2m2_cv_usage.py')
    p.add_argument('-o', '--output-file', required=True, help='output CSV')
    args = p.parse_args()

    with open(args.input_json, "rt") as fp:
        data = json.load(fp)

    output_fp = open(args.output_file, "w", newline="")
    csv_w = csv.writer(output_fp)
    
    header = ["rownum", "format_type", "label", "record_type"] + dccs
    csv_w.writerow(header)

    n = 0
    for _, all_dcc_dict in data.items():
        for term, dcc_matches in all_dcc_dict.items():
            row = []
            row.append(term)
            for dcc_name in dccs:
                dcc_values = dcc_matches.get(dcc_name,{})
                num_biosamples = dcc_values.get("num_biosamples", 0)
                row.append(num_biosamples)

            csv_w.writerow(row)
            n += 1

    print(f"Wrote {n} rows.", file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
