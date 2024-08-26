import sys

all_diagnostic_svs_manifest_file = sys.argv[1]
all_ov_manifest_file = sys.argv[2]
ov_diagnostic_svs_manifest_file = sys.argv[3]

fw = open(ov_diagnostic_svs_manifest_file, "w")
diag_svs_list = []
with open(all_diagnostic_svs_manifest_file) as fr:
  for line in fr.readlines():
    recs = line.strip().split("\t")
    diag_svs_list.append(recs)
with open(all_ov_manifest_file) as fr:
  for line in fr.readlines():
    recs = line.strip().split("\t")
    if recs in diag_svs_list:
      fw.write("\t".join(recs)+"\n")
fw.close()
  
