args <- commandArgs(TRUE)
	if (length(args) != 7){
		print("Rscript pheatmap.r <InFile <OutFile> <cluster:none/rows/cols/both> <display_numbers(T/F)> <height> <width> <Title(default:NULL)>")
			print("Example : /zhzheng/bioinfo/bin/R-3.0.1/bin/Rscript pheatmap.r pheatmapTest.txt pheatmapTestCluster_both.pdf both T 8 8 Test")
			q()
	}

	library(pheatmap)
	library(RColorBrewer);
	pdf(args[2],h=as.numeric(args[5]),w=as.numeric(args[6]))
	par(font=2,font.axis=2,font.lab=2)
d<-read.table(args[1],header=T,stringsAsFactors=FALSE, row.names = 1)
	if(args[7]=="NULL") main = "" else main = args[7]
	if (args[3] == "none"){
		pheatmap(as.matrix(d),
				display_numbers = args[4],
				color = colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100),
				scale="none",
				cluster_rows = F,
				cluster_cols=F,
				main =main,
				fontsize_row=20,
				fontsize_col=20,
				fontsize_number=15,
				legend=T,
				border_color = "grey",
				number_format = "%.2f",
				)
}else if (args[3] == "rows"){
	pheatmap(as.matrix(d),
			display_numbers = args[4],
			color = colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100),
			scale="none",
			cluster_rows = T,
			clustering_distance_rows="euclidean",
			clustering_method="complete",
			cluster_cols=F,
			main =main,
			fontsize_row=20,
			fontsize_col=20,
			fontsize_number=15,
			legend=T,
			show_rownames = F,
			border_color = "grey",
			number_format = "%.2f",
			)
}else if (args[3] == "cols"){
	pheatmap(as.matrix(d),
			display_numbers = args[4],
			color = colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100),
			scale="none",
			cluster_rows = F,
			clustering_distance_cols="euclidean",
			clustering_method="complete",
			cluster_cols=T,
			show_colnames = F,
			main =main,
			fontsize_row=20,
			fontsize_col=20,
			fontsize_number=15,
			legend=T,
			border_color = "grey",
			number_format = "%.2f",
			)
} else {
	pheatmap(as.matrix(d),
			display_numbers = args[4],
			color = colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100),
			scale="none",
			cluster_rows = F,
			clustering_distance_cols="euclidean",
			clustering_method="complete",
			cluster_cols=F,
			main =main,
			fontsize_row=20,
			fontsize_col=20,
			show_colnames = T,
			show_rownames = T,
			fontsize_number=15,
			legend=T,
			border_color = "grey",
			number_format = "%.4f",
			)
}
dev.off()
