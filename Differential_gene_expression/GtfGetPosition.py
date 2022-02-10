#! /usr/bin/env python3
import argparse
import sys
import os
import re
bindir = os.path.abspath(os.path.dirname(__file__))
import gtf_reader

__author__='Zihao Zheng'
__mail__= 'billzhengzh@gmail.com'
__doc__='the decription of program'

pat1=re.compile('^\s+$')

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input gtf file',dest='input',type=open,required=True)
	parser.add_argument('-a','--anno',help='input annotation file',required=True)
	parser.add_argument('-c','--col',help='the col to annotation',type=int,required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	parser.add_argument('-s','--search_id',help='gene_id or transcript_id',default='gene_id')
	args=parser.parse_args()
	r_dict = gtf_reader.gtf_reader(args.input,type='exon',s_id=args.search_id)
	file_anno = open(args.anno)
	for index,line in enumerate(file_anno):
		lines = line.rstrip().split('\t')
		if line.startswith('#') or index == 0:
			args.output.write('\t'.join(lines[0:args.col+1])+'\t'+lines[args.col]+'_position'+'\t'+'\t'.join(lines[args.col+1:])+'\n')
			continue
		args.output.write('\t'.join(lines[0:args.col+1]))
		gene = lines[args.col]
		#print(gene)
		gene_object = r_dict[gene][0]
		region = [str(i) for i in gene_object.output_region()]
		position = '{0}:{1}-{2}:{3}'.format(gene_object.chr,region[0],region[1],gene_object.strand)
		args.output.write('\t'+position)
		args.output.write('\t'+'\t'.join(lines[args.col+1:])+'\n')

if __name__ == '__main__':
	main()
