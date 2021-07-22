#! /usr/bin/env python3
import argparse
import sys
import os
import re
import glob
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='Su Lin'
__mail__= 'linsu@annoroad.com'
__doc__='the programis to anno the Known Gtf RPKM file'

pat1=re.compile('^\s+$')

def getInfo(info):
	tmp = info.split(';')
	result = []
	genename = biotype = ''
	for i in tmp:
		i = i.lstrip(' ')
		if 'gene_id' in i:
			geneid = i.split(' ')[1].replace('\"','')
			#result.append(geneid)
		if 'gene_name' in i:
			genename = i.split(' ')[1].replace('\"','')
			#result.append(genename)
		if 'gene_biotype' in i:
			biotype = i.split(' ')[1].replace('\"','')
			#result.append(biotype)
	if genename=='' :
		genename =  geneid
	if biotype == '':
		biotype = 'protein_coding'
	result = [geneid,genename,biotype]
	return(result)

def AnnoDic(gtf_file):
	g_file = open(gtf_file)
	anno_dic = {}
	for line in g_file:
		if line.startswith('#'):continue
		lines= line.rstrip().split('\t')
		info = lines[8]
		result = getInfo(info)
		if result[0] not in anno_dic:
			anno_dic[result[0]] = result[1:]
		else:continue
	return(anno_dic)

def Anno(anno_dic,rpkm_file,output):
	r_file = open(rpkm_file)
	dir = os.path.dirname(rpkm_file)
	#output = '{0}/rpkm.anno.xls'.format(dir)
	#print('The annotation result file is {0}'.format(output))
	outfile = open(output,'w')
	for index,line in enumerate(r_file):
		if index == 0 :
#		if line.startswith('name') or line.startswith('Gene') or line.startswith('gene'):
			outfile.write(line.rstrip()+'\tGeneName\tBiotype\n')
			continue
		lines= line.rstrip().split('\t')
		if lines[0] in anno_dic:
			outfile.write(line.rstrip()+'\t'+'\t'.join(anno_dic[lines[0]])+'\n')
		else:
			continue
	outfile.close()

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-r','--rpkm',help='input rpkm file',required=True)
	parser.add_argument('-g','--gtf',help='input gtf file',required=True)
	parser.add_argument('-o','--output',help='output file',required=True)
	#parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()
	anno_dic = AnnoDic(args.gtf)
	fileList=glob.glob(args.rpkm)
	for file in fileList:
		if file:
			Anno(anno_dic,file,args.output)
		else:
			print('The rpkm file doesn\'t exit!')

if __name__ == '__main__':
	main()
