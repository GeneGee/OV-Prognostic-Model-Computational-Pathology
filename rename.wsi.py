import sys,os

svs_dir = sys.argv[1]

for fi in os.listdir(svs_dir):
  if not fi.endswith('.svs'):
    continue
  fiArr = fi.split('-')
  sample = "-".join(fiArr[:3]+[fiArr[3][:2]])
  old_path = os.path.join(svs_dir,fi)
  new_path = os.path.join(svs_dir,sample+".svs")
  os.system("mv %s %s" %(old_path, new_path))
  
