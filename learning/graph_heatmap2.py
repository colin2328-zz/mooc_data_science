import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np

HEADERS=['lead','lag','auc']

cohorts = ["wiki_only", "no_collab", "forum_only", "forum_and_wiki"]

count=0
for cohort in cohorts:
	in_file = "results/logistic_reg_features_%s_test.csv" % cohort
	df = pd.read_csv(in_file)

	fig_title = cohort
	# The length and witdth of the heatmap
	n=int(max(df[HEADERS[0]]))

	coord=[(x+1,y+1) for x in range(n) for y in range(n)]
	val_dict={c:0 for c in coord}

	for c in coord:
		for i in range(len(df)):
			if list(df[HEADERS[0]])[i]==c[0] and list(df[HEADERS[1]])[i]==c[1]:
				val_dict[c]=list(df[HEADERS[2]])[i]
				break

	xx, yy = np.meshgrid(range(n),range(n))

	valgrid=np.zeros(xx.shape)
	for i in range(xx.shape[0]):
		for j in range(xx.shape[1]):
			valgrid[i,j]=val_dict[(i+1),(j+1)]
			
	plt.subplot(2,2,count)

	plt.imshow(valgrid.transpose(),interpolation='nearest',origin='lower', vmin=0, vmax=1)
	for x in range(n):
		for y in range(n):
			if valgrid[x,y] > 0:
				plt.text(x-0.35,y,((int)(1000*valgrid[x,y]))/1000.0,fontsize=12)

	ax=plt.gca()
	ax.set_title(fig_title,fontsize=18)
	ax.set_xlabel(HEADERS[0],fontsize=14)
	ax.set_ylabel(HEADERS[1],fontsize=14)

	ax.set_xticks([])
	ax.yaxis.set_ticks([])
	count = count +1
	plt.colorbar()

# plt.tight_layout()
plt.show()








