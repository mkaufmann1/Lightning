Welcome to the Lightning project!!!



This project is primarly a set of tools to help you migrate from WEA to NLC. It also consists of a series or wrappers and tools that can make it easier to work with the Watson Natural Language Classifier (NLC). If you haven't used it before, read up on it at http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/nl-classifier.html.



For each script, you can run it without arguments to see example usage.

If you are using this to migrate from WEA to NLC, we reccommend the following workflow:
Step 0: Export the Ground truth XML from WEA. Make sure you export your groundtruth in the following way: 
	Go to the following URL:https://watson-wdc01.ihost.com/instance/{YOUR_INSTANCE_ID}/predeploy/{YOUR_PROJECT_ID}/deepqa/tools/?action=/workbench/questionsets&root=true
	Go to Ground Truth -> Ground Truth Snapshot format. Put in a file name, and hit save.	
	Download the output from the 'Messages' tab on the top right
Step 1 : Use python/extract.py to convert ground truth snapshot into CSVs. The class labels extracted will be the PAU ID's. If you want to use human-readable names, use transform.py to substitute them in. 
Step 2 : Use python/split.py to split train and test set. We recommend reserving 70% for training and 30% for testing
Step 3 : Use python/train.py to train NLC using the train set. You can use python/view_classifiers.py to view the status of your classifier
Step 4 : Use python/test.py to test NLC using the test set. 