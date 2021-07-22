args=commandArgs(T)
	if (length(args) != 6){
		print("Rscript Volcanoplot.r <InFile> <OutFile>  <Xlab> <Ylab> <Title> <PointSize(default:3)>")
		print("Example : Rscript Volcanoplot.r VolcanoplotTest.txt VolcanoplotTest.pdf  'FoldChange(log2)' '-lgP' '' 3")
			q()
	}
	pdf(args[2],w=7,h=7)
	par(font=2,font.axis=2,font.lab=2,cex.axis=1.5,mar=c(5,5,4,6),cex.lab=1.5,cex.main=2)
	library(RColorBrewer)
#	col=brewer.pal(8,"Set2")
col=c('#2b4490','#ffd400','#d3c6a6')
data<-read.table(args[1],stringsAsFactors=FALSE,header=T,row.names=1,check.names=FALSE,quote="",sep="\t")
	for (i in 1:length(data[,1])){
		if(data[i,3]=="down")
		{data[i,4]=col[1]}
		else if(data[i,3]=="up")
		{data[i,4]=col[2]}
		 else
		 {data[i,4]=col[3]}
	}
if (args[6]==""){
	cex=3
}else {
	cex=as.numeric(args[6])
}
a=(-log10(0.05))
plot(data[,1],data[,2],pch=".",col=data[,4],xlab=args[3],ylab=args[4],main=args[5],cex=cex)
#abline(v=0,h=3,lwd=2,col="gray")
#legend("topright","n=273",cex=1.5,bty="n")
xy<-par("usr")
legend(x=xy[2L]-xinch(0.1),y=xy[4L],c("Down","Up","None"),pch=16,col=col,bty="n",cex=1.5,xpd=T)

dev.off()
