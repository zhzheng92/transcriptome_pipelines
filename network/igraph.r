args=commandArgs(T)
if(length(args) !=3 && length(args) !=4){
	print ("/annoroad/share/software/install/R-3.2.2/bin/Rscript igraph.r <Nodes> <Edges> <Outfile> <shape> alternative")
	q()
}

if (grepl(pattern = '.pdf',args[3])){ 
	pdf(args[3],w=8,h=8)
}else{
	svg(args[3],w=8,h=8)
}

nodes <- read.table(args[1],head=F)
edges <- read.table(args[2],head=F)
library(igraph)

g <- graph.empty()
if ( ncol(nodes) == 2){
	g <- add.vertices(g,nrow(nodes),name=as.character(nodes[,1]),class=as.character(nodes[,2]))
}else if ( ncol(nodes) == 3){
	g <- add.vertices(g,nrow(nodes),name=as.character(nodes[,1]),class=as.character(nodes[,2]),class1=as.character(nodes[,3]))
}else{
	print('Please check if you have label colum in nodes file.')
}

#frame.color =
total <-length(V(g)$name)
ids <- 1:length(V(g)$name)
names(ids) <- V(g)$name
#print(ids)
source <- as.character(edges[,1])
target <- as.character(edges[,2])
#inte <- as.character(edges[,3])

network <- matrix(c(ids[source],ids[target]),nc=2)
g <- add.edges(g,t(network))

V(g)$label = NA
V(g)$size = 3
V(g)[class == "up"]$color <- "#ffd400"
V(g)[class == "down"]$color <- "#2b4490"
arrow_mode =0

if ( ncol(edges) == 3 ){
#	g <- add.edges(g,t(network),level = as.character(edges[,3]))
	V(g)[class=="None"]$color <- "#B0B0B0"
	V(g)[class1=='lnc']$shape <- "circle"
	V(g)[class1=='mrna']$shape <- "square"
	E(g)$level = as.character(edges[,3])
	E(g)[level=="trans"]$color <- "black"
	E(g)[level=="cis"]$color <- "orange3"
	arrow_mode = 2
}

#layout = layout.kamada.kawai
#layout = layout.graphopt
if (total < 500){
	#V(g)$size <-3+degree(g)*0.2
	plot(g, layout = layout.kamada.kawai, vertex.color = V(g)$color, 
		 edge.arrow.mode = arrow_mode, edge.arrow.size= 0.2, edge.label.cex = 0.8,
		 vertex.label.degree = pi/2, vertex.label.dist = 0.25, vertex.label.cex = 0.8
		)
}else{
	plot(g, layout = layout.graphopt, vertex.color = V(g)$color,
		 edge.arrow.mode = arrow_mode, edge.arrow.size= 0.2, edge.label.cex = 0.8,
		 vertex.label.degree = pi/2, vertex.label.dist = 0.25, vertex.label.cex = 0.8
		)
}

dev.off()
