#! /usr/bin/env python3
import argparse
import sys
import os
import re
import gzip
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='Zihao Zheng'
__mail__= 'billzhengzh@gmail.com'

pat1=re.compile('^\s+$')
def open_a_file(a_file):
	if a_file.endswith('gz'):
		f_file = gzip.open(a_file,'rb')
		for line in f_file:
			yield line.decode()
		f_file.close()
	else:
		f_file = open(a_file,'r')
		for line in f_file:
			yield line
		f_file.close()

def read_input(file,col):
	record = {}
	with open(file) as f_file:
		for line in open_a_file(file):
			if line.startswith('#') or re.search(pat1,line):continue
			tmp=line.rstrip().split('\t')
			geneID = tmp[2]
			if geneID == '--':continue
			if not geneID in record:
				record[geneID] = {}
	return record

def read_ncbi_file(file,record,cols,names,tag=0):
	for line in open_a_file(file):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		tax,geneid = tmp[cols[0]],tmp[cols[1]]
		#if tag == 1 and tmp[12].find('GRCh37') == -1 : continue
		#if tax == species:
		if geneid in record:
			for i,j in enumerate(cols[2:]):
				tt = tmp[j]
				if tag == 1 :
					tt = tt.split(r'.')[0]
				if not names[i] in record[geneid]:
					record[geneid][names[i]] = tt
				else:
					if record[geneid][names[i]] == '-' and tt != '-':
						record[geneid][names[i]] = tt
	return record

def read_go(file,record):
	for line in open_a_file(file):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		tax,geneid = tmp[0],tmp[1]
		if geneid in record:
			go,description,category =  tmp[2],tmp[5],tmp[7]
			go_cata = 'GO_{0}'.format(category)
			if not go_cata in record[geneid]:
				record[geneid][go_cata] = []
			record[geneid][go_cata].append('{0}|{1}'.format(go,description))
	return record

def read_anno(file,pat):
	rr  = {}
	for line in open_a_file(file):
		if  line.startswith('#') or re.search(pat1,line):continue
		tmp = line.rstrip().split("\t")
		name , anno = tmp[0], tmp[1]
		name = name.replace(pat,'')
		if not name in rr:
			rr[name] = anno
	return rr

def read_ko(gene2ko, ko_anno, map_anno, record):
	ko2anno = read_anno(ko_anno,"ko:")
	map2anno = read_anno(map_anno,"path:")
	for line in open_a_file(gene2ko):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		geneid,kos,maps  = tmp[1],tmp[2],tmp[3]
		if not geneid in record:
			continue
			#record[geneid] = {}
		if not 'KO' in record[geneid]:
			record[geneid]['KO'] = []
		for i in kos.split('|'):
			if i in ko2anno : record[geneid]['KO'].append('{0}|{1}'.format(i,ko2anno[i]))
		if not 'Map' in record[geneid]:
			record[geneid]['Map'] = []
		for i in maps.split('|'):
			record[geneid]['Map'].append('{0}|{1}'.format(i,map2anno[i]))
	return record

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-l','--list',help='input list file',dest='list',required=True)
	parser.add_argument('-a','--gene2accession',help='gene2aceesion file',dest='gene2accesion',default = '{0}/current/gene2accession'.format(bindir))
	parser.add_argument('-e','--gene2ensemble',help='gene2ensemble file',dest='gene2ensemble',default = '{0}/current/gene2ensembl'.format(bindir))
	parser.add_argument('-i','--gene2info',help='gene2info file',dest='gene2info',default = '{0}/current/gene_info'.format(bindir))
	parser.add_argument('-g','--gene2go',help='gene2go file',dest='gene2go',default = '{0}/current/gene2go'.format(bindir))
	parser.add_argument('-k','--gene2ko',help='gene2ko file',dest='gene2ko',default = '{0}/current/kegg.list'.format(bindir))
	parser.add_argument('-ka','--ko_anno',help='ko anno file',dest='ko_anno',default = '{0}/current/ko.list'.format(bindir))
	parser.add_argument('-ma','--map_anno',help='map anno file',dest='map_anno',default = '{0}/current/pathway.list'.format(bindir))
	#parser.add_argument('-s','--species',help='species',dest='species',required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()

	col = [0,1]
	record = read_input(args.list,col)
	record = read_ncbi_file(args.gene2accesion,record,[0,1,3,5],['NM','NR'],1)
	print('gene2accession finish')
	record = read_ncbi_file(args.gene2ensemble,record,[0,1,2,4],['Ensemble_gene','Ensemble_rna'])
	print('gene2ensemble finish')
	record = read_ncbi_file(args.gene2info,    record,[0,1,2,8],['Symbol','Description'])
	print('gene2info,finish')
	record = read_go(args.gene2go,  record )
	print('gene2go finish')
	record = read_ko(args.gene2ko, args.ko_anno, args.map_anno,record)
	print('gene2ko finish')

	args.output.write('{0}\n'.format("\t".join(['ID','GeneID','NM','NR','Ensemble_gene','Ensemble_rna','Symbol','Description','GO_Process','GO_Component','GO_Function','KO','Map'])))
	f_file = open(args.list)
	for line in f_file:
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		name , geneid = tmp[0] , tmp[2]
		if geneid == '--':continue
		annotation = ''
		for i in ['NM','NR','Ensemble_gene','Ensemble_rna','Symbol','Description','GO_Process','GO_Component','GO_Function','KO','Map']:
			if i in record[geneid] :
				if isinstance(record[geneid][i],str):
					annotation += '{0}\t'.format(record[geneid][i])
				elif isinstance(record[geneid][i],list):
					annotation += '{0}\t'.format(";".join(record[geneid][i]))
			else:
				annotation += '--\t'
		out = '{0}\t{1}\t{2}\n'.format(name , geneid , annotation.rstrip())
		args.output.write(out)

if __name__ == '__main__':
	main()
