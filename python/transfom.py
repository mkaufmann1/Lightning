import sys,os,csv,argparse


def extract(nlc_csv,class_file,output_file):

	keys=dict()
	with open(class_file, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			keys[row[0]]=row[1]



	output_writer = csv.writer(open(output_file, 'w'), delimiter=',',
	                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
	with open(nlc_csv, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:	
			if row[1] in keys:
				l= [row[0],keys[row[1]]]
				output_writer.writerow(l)
			#else:
				#print row[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("nlc_csv", help="The CSV output from extract.py")
    parser.add_argument("class_file", help="CSV that maps PAU ID's to class names ")
    parser.add_argument("output_file", help="Output CSV File that will have the PAU ID's replaced with class names")
    args = parser.parse_args()
    extract(args.nlc_csv, args.class_file, args.output_file)

	

		
