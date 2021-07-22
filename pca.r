help_usage <- function()
{
	cat("\n+++++++++++++++++++++++++++++++++++++++++++++++++\n")
	cat("Usage:\n")
	cat("Rscript pca_analysis.r <rpkm> T <outdir>")
	cat("Example:\n/annoroad/share/software/install/R-3.2.2/bin/Rscript pca_analysis.R rpkm.trans.xls T ./ \n")
	cat("Note:\n")
	cat("rpkm.trans.xls: Group info of each sample must be included in this file ,and the columns are genes ,while the rows are samples; Group Info should be located in the first column\n")
	cat("************************************************\n")
	cat("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
}

# install and load multiple R packages
ipak <- function(pkg)
{
#new_pkg <- pkg[!(pkg %in% installed.packages()[,"Pakcage"])]
	new_pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
	if (length(new_pkg) != 0)
	{
		install.packages(new_pkg, dependencies=TRUE)
	}
	sapply(pkg, require, character.only=TRUE)
}

#create and set the output dir
mk_subdir <- function(parent_out_dir, result_dir)
{
	setwd(parent_out_dir)
	if(file.exists(result_dir))
	{
		unlink(result_dir, recursive=TRUE)
	}
	new_dir <- file.path(parent_out_dir,result_dir)
	dir.create(new_dir)
	setwd(new_dir)
}
###PCA Analysis
pca_analysis <- function(comm_input,parent_out_dir,label)
{
	mk_subdir(parent_out_dir,"pca_output")
	comm_counts <- comm_input[,-1]
	res_pca <- PCA(comm_counts,graph=FALSE)
	cat("[Running]:PCA function Analysis finished ... ...\n")
###+++++++++++++PCA_summary Output++++++++++++++++++++++
	Comp <- rownames(res_pca$eig)
	summary_pca <- cbind(Comp,res_pca$eig)
	write.table(summary_pca,"PCA_summary.xls",sep="\t",col.names=T,row.names=F,quote=F)

###+++++++++++++Dim Explanation for Variable(gene)++++++
	Variable <- rownames(res_pca$var$cos2)
	Var_exp <- cbind(Variable,res_pca$var$cos2)
	write.table(Var_exp,"Variable_gene_cos2.xls",sep="\t",col.names=T,row.names=F,quote=F)

###+++++++++++++Variable Contribute for Dim ++++++++++++++
	Var_contrib <- cbind(Variable,res_pca$var$contrib)
	write.table(Var_contrib,"Varable_gene_contrib.xls",sep="\t",col.names=T,row.names=F,quote=F)

###+++++++++++++Individual(Sample) Coordinates on the principle components+++++++++++++++++++
	Sample <- rownames(res_pca$ind$coord)
	Sample_cor <- cbind(Sample,res_pca$ind$coord)
	write.table(Sample_cor,"Sample_coordinate.xls",sep="\t",col.names=T,row.names=F,quote=F)
######++++++++++++++++++Table Output End++++++++++++++++++++
	cat("[Running]:Plot PCA_individual ... ...\n")
	pdf("PCA_individual_dim1_dim2.pdf")
	#fviz_pca_ind(res_pca, label="none", habillage=comm_input$group,addEllipses=TRUE, ellipse.level=0.95)
	#f <- factor(comm_input$group)
	a <- comm_input$group
	str(a)
	get_eig(res_pca)
	f <- factor(a)
	groups <- f
	#print(comm_input$group)
	if (label == "True")
	{
		pa <- fviz_pca_ind(res_pca, habillage=a)
	}else
	{
		#pa <- fviz_pca_ind(res_pca, label="none", habillage=comm_input$group)
		pa <- fviz_pca_ind(res_pca, label="none",habillage=f)
		pa<- pa +
		theme_classic() +
		scale_shape_manual(values=c(16,16,3,17,15,11,8,16,16,3,17,15,11,8,16,16,3,17,15,11,8)) +
		scale_color_manual(values=c("#ADFF2F","#EE2C2C","#EE2C2C","#EE2C2C","#EE2C2C","#EE2C2C","#EE2C2C","#EE00EE","#EEEE00","#EEEE00","#EEEE00","#EEEE00","#EEEE00","#EEEE00","#000000","#00FFFF","#00FFFF","#00FFFF","#00FFFF","#00FFFF","#00FFFF" )) +
		#theme(legend.position = "none") +
#		scale_shape_manual(values=c(16,16,3))+
#		scale_color_manual(values=c("#ADFF2F","#EE2C2C","#EE2C2C")) +
		labs(x="PC1", y = "PC2", title="PCA-Individuals factor map")
	}
	print(pa)
	dev.off()
######++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	cat("[Running]:PCA_individual Plot finished ... ...\n")
	cat("[Running]:Plot PCA_variable ... ...\n")
	pdf("PCA_variable_dim1-dim2.pdf")
	select_var <- NULL
	if(ncol(comm_counts) >= 20){
		select_var <- list(contrib = 20)
	}
	#pb <-fviz_pca_var(res_pca,col.var="contrib",select.var=select_var)+scale_color_gradient2(low="white", mid="blue",high="red",midpoint=55)+theme_bw()
	pb <- fviz_pca_var(res_pca,col.var="contrib",select.var=select_var)+theme_bw()
	print(pb)
	dev.off()
	cat("[Running]:PCA_variable Plot finish ... ...\n")
############################++++++++3d plot+++++++++++++++++++++++++++++++++++++++++++++++
	cat("[Running]:PCA 3d plot ... ...\n")
	col<-c("#FFFF00","#FF00FF","#FF0000","#FA8072","#F4A460","#F08080","#EED2EE","#CAFF70","#B8B8B8","#AB82FF","#A0522D","#8E388E","#000000","#006400","#0000EE","#27408B","#636363","#5D478B","#218868","#00688B","#191970")
	#col<-c("#FFFF00","#FF00FF","#FF0000")
	beuty <- col
	sample<-rownames(comm_input)
	print(sample)
	group<-comm_input$group
	tmpdata<-cbind(group,sample)
	groupCol<-cbind(unique(comm_input$group),col[1:length(unique(comm_input$group))])
	sampleCol<-merge(groupCol,tmpdata,by.x=1,by.y=1)
	print(sampleCol)
	col<-sampleCol$V2
	pdf("PCA.3d.pdf",width=10,height=10)
	dim1<-paste("Dim1(",round(res_pca$eig[1,2],2),"%)",sep="")
	dim2<-paste("Dim2(",round(res_pca$eig[2,2],2),"%)",sep="")
	dim3<-paste("Dim3(",round(res_pca$eig[3,2],2),"%)",sep="")
	scatterplot3d(res_pca$ind$coord[,1],res_pca$ind$coord[,2],res_pca$ind$coord[,3],color=col,pch=19,xlab=dim1,ylab=dim2,zlab=dim3,cex.symbols=1.5,cex.lab=1.5,cex.axis=1.2)
	#legend("bottomright",col= c("#CAFF70","#FF00FF","#FF0000","#FA8072","#F4A460","#EED2EE","#F08080","#0000EE","#B8B8B8","#AB82FF","#A0522D","#8E388E","#006400","#000000","#27408B","#636363","#5D478B","#218868","#191970","#00688B","#FFFF00"),legend = c("CC","Invivo_1","Invivo_2","Invivo_4","Invivo_8","Invivo_B","Invivo_M","MEF","NTC_1","NTC_2","NTC_4","NTC_8","NTC_B","NTC_M","NTM_1","NTM_2","NTM_4","NTM_8","NTM_B","NTM_M","Oocyte"),pch=19)
	legend("bottomright",col= c("#CAFF70","#FF00FF","#FF0000","#FA8072","#F4A460","#EED2EE","#F08080","#0000EE","#B8B8B8","#AB82FF","#A0522D","#8E388E","#006400","#000000","#27408B","#636363","#5D478B","#218868","#191970","#00688B","#FFFF00"),legend = groups,pch=19)
	#print(s3d)
	dev.off()
	cat("[Running]:PCA 3d plot finish ... ...\n")
############################++++++++++++++++3d plot End+++++++++++++++++++++++++++++++++++
}

###Main Function
main_fun <- function()
{
	## input arguments
	input_file <- commandArgs(trailingOnly=TRUE)
	if (length(input_file) == 1 && input_file[1] == "--help")
	{
		help_usage()
		cat("Introduction:\n\n")
		quit(save="no", runLast=FALSE)
	}

	if (length(input_file) < 2)
	{
		help_usage()
		stop("At least 2 arguments is required!\n\n")
	}

	cat("Your input arguments are listed as follows:\n")
	print(input_file)
	## the concise packages are needed in the analysis
	#concise_packages <- c("FactoMineR","ade4","adegraphics","factoextra","devtools")
	#ipak(concise_packages)
	library("ade4")
	library("adegraphics")
	library("FactoMineR")
	library("factoextra")
	library("devtools")
	library("scatterplot3d")
	library("ggplot2")
	#library("ggthemes")
	#input file & read your rpkm table
	ori_input <- read.table(input_file[1],header=TRUE,sep="\t",row.names=1,stringsAsFactors=FALSE)

	#comm_input <- ori_input[, colSums(ori_input ^ 2) != 0]
	comm_input <- ori_input

	## define the output dir
	parent_out_dir <- getwd()
	if(length(input_file) == 3)
	{
		parent_out_dir <- input_file[3]
	}
	if(! file.exists(parent_out_dir))
	{
		dir.create(parent_out_dir)
	}

	## check and match the input files
	cat("PCA Begins ... ...\n")
	pca_analysis(comm_input,parent_out_dir,input_file[2])
}

main_fun()
