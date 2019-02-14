import os
import numpy as np
from tqdm.autonotebook import tqdm


class ABIDEDataReader:
    """Class for reading the ABIDE dataset for easy processing

    :param verbose: [True|False] specify if you want the data processing progress to be shown as progress bars'

    Example:
    --------------------
    >>> reader = ABIDEDataReader()
    >>> reader.read('../data/ABIDE/rois_cc200', num_rois=200)
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def read(self, data_dir, num_rois=200):
        """
        Read the data from specified `data_dir`

        :param data_dir: path where the ABIDE ROI data is stored
        :param num_rois: either 200 or 400 (stands for CC200 or CC400 dataset)
        :return: list of Subject objects that contains the subject id, label and time series data for each individual
        """

        subject_data = []

        with open(os.path.join(data_dir, '..', 'site_labels.csv')) as site_labels:
            # Remove the header
            next(site_labels)

            # If verbose display progress bar using tqdm
            if self.verbose:
                site_iterator = tqdm(site_labels, total=1112, desc='Reading ABIDE data (CC{})'.format(num_rois))
            else:
                site_iterator = site_labels

            for line in site_iterator:

                fname, label = line.rstrip().split(',')

                if fname != 'no_filename':
                    subject_id = fname
                    label = int(label) - 1
                    roi_time_series = np.genfromtxt(os.path.join(data_dir, fname + '_rois_cc' + str(num_rois) + '.1D'))

                    subject_data.append(Subject(subject_id, label, roi_time_series))

        return subject_data