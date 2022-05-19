import json
import pprint
with open("out.txt", "rt") as fp:
    data = json.load(fp)

dccs = ["KFDRC", "SPARC", "ERCC_DCC", "HMP", "4DN_DCIC", "GTEx", "IDG", "LINCS", "MW", "GlyGen", "HuBMAP"]

print("format_type,", "KFDRC,", "SPARC,", "ERCC_DCC,", "HMP,", "4DN_DCIC,", "GTEx,", "IDG,", "LINCS,", "MW,", "GlyGen,", "HuBMAP,")

for k, v in data.items():
   for term, dcc_matches in v.items():
      print(term, end = ", ")
      for dcc_name in dccs:
         dcc_values = dcc_matches.get(dcc_name,{})
         print(dcc_values.get("num_biosamples", 0), end = ", ")
      print("")
     # for (dcc_name, dcc_values) in dcc_matches.items():
     #    print(term, dcc_name, dcc_values['num_biosamples'])

#pprint.pprint(data)
