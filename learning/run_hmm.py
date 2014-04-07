import numpy as np
import pylab as pl
from sklearn.hmm import MultinomialHMM
from sklearn import preprocessing



###############################################################################
in_file = "features_bin_cut.csv"
data = np.genfromtxt(in_file, delimiter = ',', skip_header = 0).T

le = preprocessing.LabelEncoder()

for idx, col in enumerate(data):
	le.fit(col)
	data[idx] = le.transform(col)

X = data.T.astype(int)

###############################################################################
# Run Gaussian HMM
print("fitting to HMM and decoding ...")
n_components = 3 # hidden node support

# make an HMM instance and execute fit
model = MultinomialHMM(n_components,n_iter = 1)

inputX= X
print inputX.shape
model.fit(inputX)

print("done\n")


###############################################################################
# print trained parameters and plot
# print("Transition matrix")
# print(model.transmat_)

print("Emissions matrix")
print model.emissionprob_


print X.shape
predicted_probs = model.predict_proba(X[0:30, :])

# print predicted_probs, len(predicted_probs)


# fpr, tpr, thresholds = roc_curve(Y, predicted_probs[:, desired_label_index],  pos_label=desired_label)
# roc_auc = auc(fpr, tpr)
