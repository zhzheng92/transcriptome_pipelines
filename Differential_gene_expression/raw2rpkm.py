#! /usr/bin/env python3
import argparse
import sys
import os
import re
sys.path.append('/annoroad/bioinfo/PMO/liutao/config/bin/RNASeq/DEGSeq')
import gff_reader
import gtf_reader

__author__='Liu Tao'
__mail__= 'taoliu@annoroad.com'

pat1=re.compile('^\s+$')

def read_input(file,header):
	t1,t2 =0 ,0 
	record = {} 
	with open(file) as f_file:
		for count,line in enumerate(f_file):
			if line.startswith('#') or re.search(pat1,line):continue
			if line.startswith('__'):continue
			if count < header : continue
			tmp=line.rstrip().split('\t')
			for cc,value in enumerate(tmp[1:]):
				if not cc in record:
					record[cc] = 0 
				if not (value == 'NA' or  value == 'miss') : 
					record[cc] += float(value)
	return record

def rpkm(c1,t1,long):
	#long = end -start +1 
	tt = float(c1)*1000000/(t1*(long))*1000
	return str(tt)
def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',required=True)
	parser.add_argument('-head','--header',help='header number',dest='head',type=int,default=0)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	parser.add_argument('-g','--gxf',help='gtf/gff file ',dest='gxf')
	parser.add_argument('-t','--type',help='gxf file type',dest='type',default='CDS')
	parser.add_argument('-s','--search',help='search id ',dest='s_id',default='Parent')
	parser.add_argument('-w','--withchr',help='add chr',dest='chr',default=False)
	parser.add_argument('-cutoff','--cutoff',help='delete rpkm < cutoff value',type=float,default=0.0)
	args=parser.parse_args()

	annotation = {}
	if args.gxf:
		bn = os.path.basename(args.gxf)
		suffix = bn.split(r'.')[-1]
		f_file = open(args.gxf)
		if suffix == 'gtf' :
			annotation = gtf_reader.gtf_reader(f_file, args.type,args.s_id,args.chr,True)
		elif suffix == 'gff' or suffix == 'gff3':
			annotation = gff_reader.gff_reader(f_file, args.type,args.s_id,args.chr,True)
		f_file.close()
	
	#record = read_infile(args.input,args.col,args.header)
	total_count = read_input(args.input,args.head)

	f_file = open(args.input)
	for count,line in enumerate(f_file):
		if line.startswith('#') or re.search(pat1,line):continue
		if line.startswith('__'):continue
		if count < args.head :
			args.output.write(line)
		tmp=line.rstrip().split('\t')
		gene = tmp[0]
		output = '{0}\t'.format(gene)
		if gene in annotation:
			if len(annotation[gene]) == 1  :
				long = annotation[gene][0].output_length()
				#print(gene,long)
				for cc,value in enumerate(tmp[1:]):
					r1 = 0 
					if not (value == 'NA' or  value == 'miss') : 
						r1 = rpkm(value,total_count[cc],long)
				#		print(gene,long,value,total_count[cc])
					output+='{0}\t'.format(r1)
				output_value = output.rstrip().split('\t')[1:]
				output_value_tmp = [i for i in output_value if float(i) > args.cutoff]
				if len(output_value_tmp) == 0:continue
				args.output.write(output.rstrip()+'\n')
			else:
				print('{0} is more than one'.format(gene))
		else:
			pass
	f_file.close()

if __name__ == '__main__':
	main()
