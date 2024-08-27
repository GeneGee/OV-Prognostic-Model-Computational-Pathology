ov_patient_clin <- read.table("data_clinical_patient.txt", sep='\t', header = TRUE,
                              na.strings = c("[Not Available]","[Not Applicable]"), stringsAsFactors = TRUE, skip=4)
ov_sample_clin <- read.table("data_clinical_sample.txt", sep='\t', header = TRUE,
                             na.strings = c("[Not Available]"), stringsAsFactors = TRUE, skip=4)
ov_clin <- merge(paad_sample_clin,paad_patient_clin,by=c('PATIENT_ID'))
ov_clin_evaled <- subset(ov_clin, !(OS_MONTHS %in% c(NA)), 
                           select = c("PATIENT_ID","SAMPLE_ID","SEX","AGE","CANCER_TYPE_DETAILED","GRADE",
                                       "CLINICAL_STAGE","ECOG_SCORE","OS_STATUS","OS_MONTHS","DFS_STATUS","DFS_MONTHS"))
out_df <- rename(ov_clin_evaled , c(PATIENT_ID="case_id", SAMPLE_ID="slide_id"))
#sample_id <- read.csv("process_list_autogen.csv",header = TRUE, sep = ",")
#for (i in 1:length(sample_id$slide_id)) print(tools::file_path_sans_ext(sample_id$slide_id[i]))
write.csv(out_df, "ov_clin.csv", row.names=FALSE)
