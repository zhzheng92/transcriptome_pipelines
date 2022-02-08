args<-commandArgs(T)
## args1 raw_count_table
## args2 conditions 
## args3 condition1 name ,  condition2 name
## args4 outdir

## read raw count table
new_data=read.table(args[1],header=T,row.names=1)

##read condition 
design=read.table(args[2],header=T,row.names=1)
print(design)
cmp = unlist(strsplit(args[3],','))
print(cmp)
library(DESeq2)
library(gplots)
#dd=which(design$condition==cmp[1] | design$condition==cmp[2])
#print(dd)
#new_data = data[,dd]
print('generate DEseq object')
ddsFullCountTable <- DESeqDataSetFromMatrix(countData = new_data, colData = design , design = ~condition)
dds = DESeq(ddsFullCountTable)
res = results(dds , contrast = c("condition",cmp[1],cmp[2]))

file_name = paste(cmp[1],cmp[2],"transcript.xls",sep="_")
abs_file_name = paste(args[4],file_name,sep="/")
write.table(res,file=abs_file_name,sep="\t", quote = FALSE, row.names = TRUE)

