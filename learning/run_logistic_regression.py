'''
Created on March 17, 2013
@author: Colin Taylor
'''
import numpy as np
import pylab as pl
import argparse
import time
import os


from sklearn import linear_model
from sklearn.metrics import roc_curve, auc

import flatten_featureset 

def plotROC(fpr, tpr, roc_auc, lead, lag):
	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc)
	pl.plot([0, 1], [0, 1], 'k--')
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('ROC- lead = %s lag = %s' % (lead, lag))
	pl.legend(loc="lower right")
	pl.show()


def run_regression(in_file, lead, lag):
	start_time = time.time()
	intermediate_file = "data/tmp.csv"

	flatten_featureset.create_features(intermediate_file, in_file, lead, lag)

	data = np.genfromtxt(intermediate_file, delimiter = ',')
	os.remove(intermediate_file)
	
	X = data[:,1:-1]
	Y = data[:,-1]

	logreg = linear_model.LogisticRegression(C=1e5)
	logreg.fit(X, Y)
	predicted_probs = logreg.predict_proba(X)

	desired_label = 0 # want to predict if student will dropout
	desired_label_index = logreg.classes_.tolist().index(desired_label) 

	fpr, tpr, thresholds = roc_curve(Y, predicted_probs[:, desired_label_index],  pos_label=desired_label)
	roc_auc = auc(fpr, tpr)

	print "ran regression in", time.time() - start_time, "seconds"
	print "number of data points:", len(X)

	# print("Area under the ROC curve : %f" % roc_auc)

	weights = logreg.coef_[0]
	# print "weights:\n", weights
	# plotROC(fpr, tpr, roc_auc, lead, lag)

	return float(roc_auc)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--in_file',type=str, default="data/features_cut_forum_and_wiki.csv") # input csv
	parser.add_argument('--lead',type=int, default=1)  # number of weeks ahead to predict
	parser.add_argument('--lag',type=int, default=2)  # number of weeks of features to use
	args = parser.parse_args()
	for lead in range (1,15):
		for lag in range(1, 16 -lead):
			try:
				roc_auc = run_regression(args.in_file, lead, lag)
				print "lead: %s lag: %s, roc_auc: %s" % (lead, lag, roc_auc)
			except:
				pass

	# run_regression(args.in_file, args.lead, args.lag)