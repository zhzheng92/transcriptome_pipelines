#! /usr/bin/env python3
import argparse
import sys
import os
import re
sys.path.append('/zhzheng/RNASeq/config/bin/DEGSeq')
import gff_reader
import gtf_reader

__author__='ZZ'
__mail__= 'billzhengzh@gmail.com'

pat1=re.compile('^\s+$')

def read_annotation(f_file,col,tag ,r_dict):
	header = ''
	for count,  line in enumerate(f_file):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		id = tmp[col]
		if count == 0 :
			if tag == 'ref':
				header = '\t'.join(line.rstrip().split('\t')[1:])
			elif tag == 'novel':
				header = "\t".join(tmp[1:])
		else:
			if not id in r_dict:
				r_dict[id] = ''
			if tag == 'ref':
				r_dict[id] = '\t'.join(line.rstrip().split('\t')[1:])
			elif tag == 'novel':
				r_dict[id] = "\t".join(tmp[1:])
	return r_dict,header

def append_annotation(f_file,col,annotation,o_file,symbols):
	for line in f_file:
		if line.startswith('#') or re.search(pat1,line):
			o_file.write('{0}\t{1}\n'.format(line.rstrip(),'annotation'))
			continue
		if line.startswith('ID'):
			o_file.write('{0}\t{1}\n'.format(line.rstrip(),'annotation'))
			continue
		tmp=line.rstrip().split('\t')
		id = tmp[col]
		anno = [symbols]
		if id in annotation:
			anno = annotation[id]
		o_file.write('{0}\t{1}\n'.format(line.rstrip(),'\t'.join(anno[1:])))

def get_position(annotation):
	record = {}
	for gene in annotation:
		obj = annotation[gene][0]
		chr = obj.chr
		strand = obj.strand
		start,end = obj.output_region()
		if not gene in record:
			record[gene] = '{0}:{1}-{2}:{3}'.format(chr,start,end,strand)
	return record

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',type=open,required=True)
	parser.add_argument('-ar','--ref_annotation',help='annotation  ref file',dest='annoref',type=open,required=True)
	parser.add_argument('-an','--novel_annotation',help='annotation novel file',dest='annonovel',type=open)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	parser.add_argument('-g','--gtf',help='gtf file',dest='gtf',required=True,type=open)
	parser.add_argument('-unknown',help='unknown symbol',dest='unknown',default='unknown')
	parser.add_argument('-s','--search',help='search_id ,gene_id or transcript_id',default='gene_id')
	parser.add_argument('-c','--col',help='which col is key, first is input file , second is ref annotation , third is anno novel',dest='col',type=int,nargs='+')
	args=parser.parse_args()

	annotations = gtf_reader.gtf_reader(args.gtf, 'exon', args.search , True)

	position = get_position(annotations)
	annotation = {}
	annotation,header = read_annotation(args.annoref , args.col[1] , 'ref',annotation)
	if not  args.annonovel == None: annotation,header = read_annotation(args.annonovel, args.col[2] , 'novel',annotation )
	for count , line in enumerate(args.input):
		if count == 0 :
			args.output.write('{0}\tPosition\t{1}\n'.format(line.rstrip(),header))
		else :
			tmp = line.rstrip().split('\t')
			name = tmp[args.col[0]]
			pp , anno ='--','--\t'*12
			anno = anno.rstrip()
			if name in position:
				pp = position[name]
			if name in annotation:
				anno = annotation[name]
			args.output.write('{0}\t{1}\t{2}\n'.format(line.rstrip(),pp,anno))

if __name__=='__main__':
	main()
