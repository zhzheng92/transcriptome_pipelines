args<-commandArgs(T)
## args1 raw_count_table
## args2 conditions 
## args3 condition1 name ,  condition2 name
## args4 outdir

library(DESeq)
library(gplots)
## read raw count table
data=read.table(args[1],header=T,row.names=1)

##read condition 
design=read.table(args[2],header=T,row.names=1)
print(design)
cmp = unlist(strsplit(args[3],','))
print(cmp)
print(which(design$condition==cmp[1]))
print(which(design$condition==cmp[2]))
dd=which(design$condition==cmp[1] | design$condition==cmp[2])
print(dd)
new_data = data[,dd]
print('generate DEseq object')
cds=newCountDataSet(new_data,design[dd,1])
print('estimate Size Factors')
cds=estimateSizeFactors(cds)
print('estimate Dispersions')
cds=estimateDispersions(cds,method='per-condition',fitType="local")
print('caculate DE gene')
res=nbinomTest(cds,cmp[1],cmp[2])

#outdir = paste(args[4],"/pic",sep='')
#dir.create(outdir)

#draw MA plot
#print('draw MA plot')
#pdf(paste(outdir,"maplot.pdf",sep='/'),w=8,h=6)
#plotMA(res,col=ifelse(res$pval >= 0.05, "gray32", "red3"))
#dev.off()

##draw P value distribution
#print('draw p hist ')
#pdf(paste(outdir,"p_hist.pdf",sep='/'),w=8,h=6)
#hist(res$pval,breaks=100,col='skyblue',border='slateblue',main='')
#dev.off()

#print('get significant gene')
#resSig=res[res$padj < 0.05,]

print('output all result')
result = array('no',dim=c(length(res$padj),1))
result[which(res$padj < 0.05)] = 'yes'
total =cbind(res,counts(cds,normalized =T),result)

file_name = paste(cmp[1],cmp[2],"transcript.xls",sep="_")
abs_file_name = paste(args[4],file_name,sep="/")
write.table(total,file=abs_file_name,sep="\t", quote = FALSE, row.names = FALSE)

#draw dispersion plot
#print('draw dispersion plot')
#pdf(paste(outdir,"isoforms.DispEst.pdf",sep='/'),w=8,h=6)
#plotDispEsts(cds)
#dev.off()

## draw overall cluster
#print('draw overall cluster heatmap')
#cdsFullBlind <- estimateDispersions( cds, method = "blind" )
#vsdFull <- getVarianceStabilizedData( cdsFullBlind )
#dists <- dist( t( vsdFull ) )
#pdf(paste(outdir,"sample_heatmap.pdf",sep='/'),w=8,h=6)
#heatmap(as.matrix(dists),symm=TRUE,scale="none",col=colorRampPalette(c("green","red"))(100),labRow=pData(cds)$condition,cexCol=0.6,cexRow=0.6)
#dev.off()

### draw cluster map
#print('draw significant heatmap')
#select=which(res$padj<0.05)
#mm = counts(cds)[select,]
#mm2 =log2(mm)
#for (i in 1:ncol(mm2)){
#	mm2[which(mm2[, i] == "-Inf"),] = 0.01
#}
#pdf(paste(outdir,"sig_heatmap.pdf",sep='/'),w=8,h=6)
#heatmap.2(mm2, col = colorRampPalette(c("green","red"))(100), scale = "none",trace='none',cexCol=0.6,cexRow=0.4,density.info=c("none"))
#dev.off()
#png(paste(outdir,"sig_heatmap.png",sep='/'))
#heatmap.2(mm2, col = colorRampPalette(c("green","red"))(100), scale = "none",trace='none',cexCol=0.6,cexRow=0.4,density.info=c("none"))
#dev.off()

