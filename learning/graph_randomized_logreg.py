import numpy as np
from numpy.linalg import norm
import pylab as pl
import utils

cohorts = "no_collab", "forum_and_wiki", "forum_only", "wiki_only"
AUC_fontsize = 10
med_fontsize = 12
fontsize = 16

# feature weights
no_collab = [0.213747149544,0.0,0.0,0.0,0.14803320608,0.160584649213,0.336172533683,0.21862390176,0.0428008527187,0.54256851059,0.216995003806,0.0674867789618,0.0,0.413245102913,0.205391521177,0.0521521988593,0.00790958049887,0.0,0.371156108574,0.520039573257,0.47036043031,0.414019300805,0.360717167224,0.464722158529,0.304829858369,0.502566266538,0.691742190746]
forum_and_wiki = [0.0396125472411,0.0,0.0037008726723,0.00122040803112,0.1201860198,0.026250170068,0.0828347429026,0.0270680083144,0.00319875283447,0.0530185630507,0.0256037226002,4.7619047619e-05,6.7353545925e-05,0.12664960106,0.0758534769463,0.00136507936508,0.000880343466058,0.0,0.0409617535903,0.111771017871,0.17984847322,0.143466375027,0.19820244491,0.285409798931,0.0900591265877,0.0517125938876,0.128076654298]
forum_only = [0.172868051922,0.0911562358277,0.0,0.353434898303,0.211512944067,0.0809446289161,0.238780787863,0.140360300282,0.0256350007136,0.19039148312,0.141493580494,0.0511277224099,0.0929112811791,0.27389696679,0.177149775225,0.0212509826153,0.00773492592064,0.0147116780045,0.234974646253,0.353244022512,0.348405023416,0.271349056763,0.364481246796,0.426207957254,0.254981183763,0.208745475953,0.397507366047]
wiki_only = [0.0223512340834,0.0,0.0125774067203,0.0,0.0432492018055,0.060167460287,0.0801864530463,0.0418008767789,0.00574598737648,0.0229168378935,0.0412575785021,0.0059419846027,0.0112606639392,0.0545938650788,0.0285190999477,0.00966066717166,0.00274783549784,0.0,0.0122859057914,0.122085024103,0.125954992504,0.102063242923,0.131585522384,0.185847665003,0.0762738993302,0.0160662646267,0.132162175126]

feature_vectors = {}
feature_vectors["no_collab"] = no_collab / norm(no_collab)
feature_vectors["forum_and_wiki"] = forum_and_wiki / norm(forum_and_wiki)
feature_vectors["forum_only"] = forum_only / norm(forum_only)
feature_vectors["wiki_only"] = wiki_only / norm(wiki_only)

features = range(2,19) + range(201, 211)

for cohort in cohorts:
	
	n = len(feature_vectors[cohort])

	ax = pl.gca()
	pl.bar(range(n), feature_vectors[cohort], color = '0.75')
	# pl.title('Randomized logistic Regression: %s' % cohort, fontsize=fontsize)
	
	ax.set_xlabel("Feature number", fontsize=fontsize)
	ax.set_ylabel("Average feature weight", fontsize=fontsize)


	ax.set_xticks(range(n))
	ax.set_xticklabels(features,fontsize=AUC_fontsize, rotation='vertical')

	
	
	utils.save_fig("/home/colin/evo/papers/thesis/figures/logreg/randomized_%s" % cohort)
	# pl.show()
	# break
	pl.clf()

for cohort in cohorts:
	in_file = "results/randomized_logistic_reg_features_%s_time_averaged.csv" % cohort
	data = np.genfromtxt(in_file, delimiter=",")[1:, :-1]
	n = len(data)
	for i in range(n):
		if np.all(data[:,i]==0):
			n = i
	data = data[:n,:n]
	for col in range(n):
		data[:, col] /= norm(data[:, col])

	for x in range(n):
		for y in range(n):
			if x < y:
				data[x,y] = None
	

	pl.imshow(np.transpose(data), interpolation='nearest',origin='lower', vmin=0, vmax=1, cmap='RdBu')
	ax = pl.gca()
	# pl.title('Feature weeks importance: %s' % cohort, fontsize=fontsize)
	
	ax.set_xlabel("Lag", fontsize=fontsize)
	ax.set_ylabel("Week's features used", fontsize=fontsize)
	

	ax.set_xticks(range(n))
	ax.set_yticks(range(n))
	ax.set_xticklabels(range(1,n+1),fontsize=med_fontsize)
	ax.set_yticklabels(range(1,n+1),fontsize=med_fontsize)

	for week in range(n):
		for lag in range(n):
				if week >= lag and not np.isnan(data[week][lag]):
					pl.text(week - .3, lag - .1,np.around(data[week][lag], decimals=2),fontsize=AUC_fontsize)

	cb = pl.colorbar()
	for t in cb.ax.get_yticklabels():
		t.set_fontsize(med_fontsize)

	
	
	
	utils.save_fig("/home/colin/evo/papers/thesis/figures/logreg/randomized_%s_over_time" % cohort)
	# pl.show()
	# break




