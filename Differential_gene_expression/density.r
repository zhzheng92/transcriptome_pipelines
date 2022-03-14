args = commandArgs(T)

if (length(args) != 4){
		print("Rscript density.r <InFile> <OutFile> <Title> <xlab> <xmin> <xmax> <ymin> <ymax>")
		print("Example : Rscript density.r test.txt  test.pdf Test expression 0 0.2 0 80")
		q()
	}

pdf(args[2],w=10,h=8)
library(RColorBrewer)
d<-read.table(args[1],header=TRUE,stringsAsFactors=FALSE,check.names=F,row.names=1,sep="\t")
n=0;
if (ncol(d) == 1){
	n= c("#66C2A5")
}else if (ncol(d) == 2){
	n= c("#66C2A5","#FC8D62");
}else if (ncol(d) >=3 && ncol(d)<8){
	n = brewer.pal(ncol(d),"Set2")
}else if (ncol(d)>=8 && ncol(d)<=17){
	n = c(brewer.pal(8,"Set2"),brewer.pal(ncol(d) - 8,"Accent"))
}else {
#	n = 1:ncol(d)
	n=c(brewer.pal(8,"Set2"),brewer.pal(9,'Set1'),brewer.pal(8,"Accent"),brewer.pal(12,'Set3'),brewer.pal(12,'Paired'),brewer.pal(8,'Dark2'),brewer.pal(5,'Pastel1'),brewer.pal(3,'BrBG'),brewer.pal(6,'Spectral'),brewer.pal(9,'OrRd'))
}
LengendSize=max(strwidth(colnames(d),units="inches",cex=1.5,font=2))
par(font=2,font.axis=2,font.lab=2,cex.axis=1.5,cex.lab=1.5,cex.main=2,mai=c(1,1.5,1,LengendSize+2))
den = density(d[,1])

x_min = min(den$x)
x_max = max(den$x)
y_min = min(den$y)
y_max = max(den$y)+0.01
print('yes')
print(ncol)
print(length(d[1,]))
if(length(d[1,])>2){
for (i in 2:ncol(d)){
den = density(d[,i])
if (min(den$x)<x_min){x_min<-min(den$x)}
if (min(den$y)<y_min){y_min<-min(den$y)}
if (max(den$x)>x_max){x_max<-max(den$x)}
if (max(den$y)>y_max){y_max<-max(den$y)}
}
}
print('yes')
#plot(d[,1],type="l")
#plot(density(d[,1]),type="l",col=n[1],ylim=c(as.numeric(args[7]),as.numeric(args[8])),xlim=c(as.numeric(args[5]),as.numeric(args[6])),xlab=args[4],main=args[3],lwd=2)
plot(density(d[,1]),type="l",col=n[1],ylim=c(y_min,y_max),xlim=c(x_min,x_max),xlab=args[4],main=args[3],lwd=2)
if(length(d[1,])>1){
for (i in 2:ncol(d)){
	lines(density(d[,i]),col=n[i],lwd=2)
}
}
xy=par("usr")
#legend("topright",legend=colnames(d),col=n,lty='solid',bty='n',lwd=2)
legend(x=xy[2L]-xinch(0.1),y=xy[4L],xpd=T,legend=colnames(d),col=n,lty='solid',bty='n',lwd=2,ncol=2)
dev.off()
