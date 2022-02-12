import os
import sys
import re
pat1=re.compile('gene|name')
def main():
	print("\n total four parameters : <listfile>,<reportfile>,<outfile>,<listname index in reportfile>\n\n")
	f1=open(sys.argv[1])
	f2=open(sys.argv[2])
	out=open(sys.argv[3],'w')
	list={}
	for line in f1:
		tmp=line.rstrip().split('\t')
		if tmp[0] not in list :
			list[tmp[0]]=tmp[1]
	for index,line in enumerate(f2) :
		if index == 0:
			tmp=line.rstrip().split('\t')
			tmp.insert(1,'Group')
			out.write('\t'.join(tmp)+'\n')
		else:
			nn=line.rstrip().split('\t')[0]
			if nn in list :
				out.write(nn+'\t'+list[nn]+'\t'+'\t'.join(line.rstrip().split('\t')[1:])+'\n')
	f1.close()
	f2.close()
	out.close()
if __name__ =='__main__':
	main()

