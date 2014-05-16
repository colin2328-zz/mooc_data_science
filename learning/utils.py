import os
import matplotlib.pyplot as plt
import shutil
import numpy as np
import pylab as pl

def remove_and_make_dir(directory):
	# If the directory exists, remove it
	if os.path.exists(directory):
		shutil.rmtree(directory)
	os.makedirs(directory)

def move_emissions_transitions(source_dir, destination_dir):
	remove_and_make_dir(destination_dir)
	shutil.move(source_dir + "emissions.txt", destination_dir)
	shutil.move(source_dir + "transitions.txt", destination_dir)

def copy_files(files, source_dir, destination_dir):
	for f in files:
		shutil.copyfile(os.path.join(source_dir,f), os.path.join(destination_dir,f))

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

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

def save_fig(path, ext='png', close=True):
	"""Save a figure from pyplot.

	Parameters
	----------
	path : string
		The path (and filename, without the extension) to save the
		figure to.

	ext : string (default='png')
		The file extension. This must be supported by the active
		matplotlib backend (see matplotlib.backends module).  Most
		backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.

	close : boolean (default=True)
		Whether to close the figure after saving.  If you want to save
		the figure multiple times (e.g., to multiple formats), you
		should NOT close it in between saves or you will have to
		re-plot it.

	"""
	
	# Extract the directory and filename from the given path
	directory = os.path.split(path)[0]
	filename = "%s.%s" % (os.path.split(path)[1], ext)
	if directory == '':
		directory = '.'

	# If the directory does not exist, create it
	if not os.path.exists(directory):
		os.makedirs(directory)

	# The final path to save to
	savepath = os.path.join(directory, filename)

	# Actually save the figure
	plt.savefig(savepath)
	
	# Close it
	if close:
		plt.close()