import os
import matplotlib.pyplot as plt
import shutil

def move_emissions_transitions(destination_dir):
	# If the directory exists, remove it
	if os.path.exists(destination_dir):
		shutil.rmtree(destination_dir)
	os.makedirs(destination_dir)
	shutil.move("emissions.txt", destination_dir)
	shutil.move("transitions.txt", destination_dir)

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