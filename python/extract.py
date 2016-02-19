import csv
import xml.etree.ElementTree as ET
import argparse
from collections import defaultdict
# Extracts questions, PAUs from Ground Truth Snapshot XML and creates a CSV file for NLC training purposes
# Pre-Requisite : The XML must be exported from WEA ExperienceManager using the GroundTruthSnapshot export option
# Parameters :
# gttsnapshotxml - GTT Snapshot XML
# outputfile - output CSV
# numquestion - No. of questions to limit (NLC has a limitation of 20 MB size for the jSON and 10K training instance)
# classesreportfile - Reports the number of unique classes. Each line is a class, with the primary question as a key

#TODO # o
def extract(gttsnapshotxml, csvfile):


    root = ET.parse(gttsnapshotxml).getroot()

    csvWriter = csv.writer(open(csvfile, 'w'), delimiter=',')

    tCount = 0
    count = 0
    questionDictionary = dict()
    classesDict = dict()
    classCount = 0

    for question in root.iter('question'):

	
        id = question.find('id').text if question.find('id') is not None else ""
        value = question.find('value').text if question.find('value') is not None else ""
        questionText = value.lstrip().rstrip()

        # Get primary question PAU
        predefinedAnswerUnit = question.find('predefinedAnswerUnit').text if question.find(
            'predefinedAnswerUnit') is not None else ""

        # Look for mapped question
        mappedQuestion = question.find('mappedQuestion') if question.find('mappedQuestion') is not None else ""

        # Check for valid question, has mapped question section and not PAU - This means secondary question
        if questionText != "" and predefinedAnswerUnit == "" and mappedQuestion != "":
            parentQuestionPau = mappedQuestion.find('predefinedAnswerUnit') if mappedQuestion.find(
                'predefinedAnswerUnit') is not None else ""

            	

            mappedQuestionText = mappedQuestion.find("value").text

            if parentQuestionPau != "":
                if questionDictionary.get(questionText) is None or questionDictionary.get(questionText) == "":
                    csvWriter.writerow([questionText.encode('utf-8'), parentQuestionPau.text])
                    questionDictionary.update({questionText: parentQuestionPau.text})
                    classesDict.update({parentQuestionPau.text: questionText.encode('utf-8')})

                    classCount += 1
                    count += 1
                else:
                    existingPau = questionDictionary.get(questionText)
                    if questionDictionary.get(questionText) is None or questionDictionary.get(questionText) == "":
                        csvWriter.writerow([questionText.encode('utf-8'), existingPau])
                        questionDictionary.update({questionText: existingPau.text})
                        count += 1
        elif questionText != "" and predefinedAnswerUnit != "" and mappedQuestion == "" and questionDictionary.get(questionText) is None:
            # This means primary question
            csvWriter.writerow([questionText.encode('utf-8'), predefinedAnswerUnit])
            classesDict.update({predefinedAnswerUnit: questionText})
            questionDictionary.update({questionText: predefinedAnswerUnit})
            count += 1
            classCount += 1
    print("No. of classes found : " + str(len(classesDict)))
    print("Total Questions Generated : " + str(count))

    #compute question statistics 
    #invert question map to find # of questions per class 
    inv_map = {}
    for k, v in questionDictionary.iteritems():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)    
    #turn the inverted map into a map where the key is list of classes and the value is the # of entries for that class 
    count_map = defaultdict(list)
    for k,v in inv_map.iteritems():
        count_map[len(v)].append(k)

    #print statistics about the training file 
    print "\nThe NLC recommends having 8  items per class AT MINIMUM. Using the information below see if a substantial portion of your data does not meet this criteria. If not, consider adding more data to each class!!"
    for k,v in count_map.iteritems():
        print len(v), "classes with", k, "items"



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gttsnapshotxml", help="Ground Truth Snapshot XML File")
    parser.add_argument("outputfile", help="Output CSV File ")
    args = parser.parse_args()
    extract(args.gttsnapshotxml, args.outputfile)

	
