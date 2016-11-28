import numpy as np
import pandas as pd
import time
from sklearn.model_selection import StratifiedKFold
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import scale

from utilities import Timer, MetaData, ResultsWriter

# file properties
# -----------------------------------------------------
filePath = '../data/consolidated_clean_all.txt'

metadata = MetaData()
dataType = metadata.getProcessedColsDataType()

timer = Timer()
startTime = timer.getTime()
print('Start Time : ', timer.getTime())  # Get the start time for tracking purposes

print('------------------------------------------------------------')
print('Reading files ... ')
print('------------------------------------------------------------')
# Note that this is a numpy structured array as the data set contains both int and float
# http://docs.scipy.org/doc/numpy/user/basics.rec.html
data = np.genfromtxt(filePath, delimiter = ',', skip_header = 1, dtype=dataType)
df = pd.DataFrame(data)

subj = df.ix[:,-2]
activity = df.ix[:,-1]
subj_activity = (100*subj) + activity
df = pd.concat([df,subj_activity],axis=1)
df.rename(columns={0:'activity_subj'}, inplace=True)

# split data set into test and train using K-Fold (for both subj and activity)
# ---------------------
skf = StratifiedKFold(n_splits=3, shuffle=False, random_state=2016)
readings = df.ix[:,:-3]

# Scale data
readings = scale(readings)

# K-Fold split based on subj_activity
for train_index, test_index in skf.split(readings,subj_activity):
    df_train, df_test = df.ix[train_index], df.ix[test_index]
    print('Size of data set: ', len(df))
    print('Size of training data set: ', len(train_index))
    print('Size of test data set: ', len(test_index))

print('Verifying distribution ...')
train_table = df_train.rename(index=str, columns={'subject':'training_count'})
test_table = df_test.rename(index=str, columns={'subject':'test_count'})
verify = pd.concat([train_table.ix[:,-2:].groupby('activity_subj').count(),
                    test_table.ix[:,-2:].groupby('activity_subj').count()],axis = 1)

pd.options.display.max_rows = 150

print(verify)

# ---------------------
# Subject and then Activity
# ---------------------
# step 1.1 - get the readings data (from data stratified using activity)
readings_train = df_train.ix[:,:-3]
subj_activity_train = df_train.ix[:,-1]

rbf_feature = RBFSampler(gamma=1, random_state=2016)
readings_train = rbf_feature.fit_transform(readings_train)

# step 1.2 - fit the model to predict subject
print('Fitting model to predict subject ...')
clf_both = SGDClassifier()
time_bgn = time.time()
clf_both.fit(readings_train, subj_activity_train)
dur_train_both = time.time() - time_bgn

# step 2.1 - get the readings data (from data stratified using subject)
readings_test = df_test.ix[:,:-3]

readings_test = rbf_feature.fit_transform(readings_test)

# step 2.2 - predict subject activity
print('Predicting subject activity ... ')
predicted_subj_activity = clf_both.predict(readings_test)

# step 3 - printing results
actual_subj_activity = df_test.ix[:,-1]

print(classification_report(actual_subj_activity, predicted_subj_activity))
print('accuracy score: ', accuracy_score(actual_subj_activity, predicted_subj_activity))

#ResultsWriter.write_to_file('results_thomas.txt',model='pca_gnb',
#                            y_actual=actual_subj_activity,y_predicted=predicted_subj_activity,
#                            dur_train_activity=0, dur_train_subj=0, dur_train_both=dur_train_both,
#                            method='both')