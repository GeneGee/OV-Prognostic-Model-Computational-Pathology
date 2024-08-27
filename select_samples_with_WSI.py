import os,sys

# python select_samples_with_WSI.py tcga_ov_clin.csv process_list_autogen.csv tcga_ov_clin.prognosis.csv

tcga_ov_clin_fi = sys.argv[1]
svs_fi = sys.argv[2]
tcga_ov_prog_fi = sys.argv[3]

fw = open(tcga_ov_prog_fi,"w")
svs_list = []
with open(svs_fi) as fr:
  for line in fr.readlines():
    recs = line.strip().split(",")
    fi = recs[0]
    if fi == "slide_id":
      continue
    svs_list.append("-".join(fi.split('-')[:-1]))
with open(tcga_ov_clin_fi) as fr:
  for line in fr.readlines():
    recs = line.strip().split(',')
    sample = recs[1]
    if sample == "slide_id":
      headers = recs
      fw.write(",".join(headers+['label'])+'\n')
      continue
    if sample not in svs_list:
      continue
    if recs[headers.index('OS_MONTHS')] <= 24:
      fw.write(",".join(recs+['Bad'])+'\n')
    else:
      fw.write(",".join(recs+['Good'])+'\n')
fw.close()
    
    
