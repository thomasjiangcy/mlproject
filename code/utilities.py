import csv, os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import precision_score,recall_score, accuracy_score, classification_report

class Plotter:
    def __init__(self):
        pass

<<<<<<< HEAD
    def plot_correlation(dataframe, title=''):
        pass
=======
    def plot_correlation(self,dataframe, title=''):
        lang_names = dataframe.columns.tolist()
        tick_indices = np.arange(0.5, len(lang_names) + 0.5)
        plt.figure(figsize=(12, 12))
        plt.pcolor(dataframe.values, cmap='RdBu', vmin=-1, vmax=1)
        colorbar = plt.colorbar()
        colorbar.set_label('Correlation')
        plt.title(title)
        plt.xticks(tick_indices, lang_names, rotation='vertical')
        plt.yticks(tick_indices, lang_names)
        plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
>>>>>>> refs/remotes/origin/master

    def plot_scree(self,explainedVarianceRatio, colsNumber, title=''):
        pc = np.arange(colsNumber) + 1
        plt.figure(figsize=(12, 9))
        plt.title(title)
        plt.xlabel('Principal Component')
        plt.ylabel('% of Variance Explained')
        plt.plot(pc, explainedVarianceRatio)


class Timer:
    def __init__(self):
        pass

    def getTimeString(self, mydate):
        return str(mydate.strftime('%Y-%m-%d %H:%M:%S'))

    def getTime(self):
        return datetime.now()

    def getFormattedTime():
        return str(datetime.now().strftime('%Y-%m-%d %H:%M'))

class ResultsWriter:

    _methods_dict = {'sa':'subject then activity',
               'as':'activity then subject',
               'both':'both at the same time'}

    def write_to_file(results_file, model, y_actual, y_predicted,
                      dur_train_activity, dur_train_subj, dur_train_both, method):
        precision = precision_score(y_actual, y_predicted, average='weighted')
        recall = recall_score(y_actual, y_predicted, average='weighted')
        accuracy = accuracy_score(y_actual, y_predicted)

        method = ResultsWriter._methods_dict[method]

        dur_train_activity = '{0:.2f}'.format(dur_train_activity)
        dur_train_subj = '{0:.2f}'.format(dur_train_subj)
        dur_train_both = '{0:.2f}'.format(dur_train_both)
        precision = '{0:.2f}'.format(precision)
        recall = '{0:.2f}'.format(recall)
        accuracy = '{0:.2f}'.format(accuracy)

        record = [Timer.getFormattedTime(), model, dur_train_activity, dur_train_subj, dur_train_both,
                  precision, recall, accuracy, method]

        if not os.path.isfile('../result/'+results_file):
            output_file = open('../result/' + results_file, 'a')
            data_writer = csv.writer(output_file, delimiter=",", quoting=csv.QUOTE_NONE)

            header = ['record_time','model','dur_train_activity','dur_train_subj','dur_train_both',
                      'precision','recall','accuracy','method']
            data_writer.writerow(header)
            data_writer.writerow(record)

        else:
            output_file = open('../result/' + results_file, 'a')
            data_writer = csv.writer(output_file, delimiter=",", quoting=csv.QUOTE_NONE)
            data_writer.writerow(record)

        output_file.close()

        print(classification_report(y_actual, y_predicted))
        print('accuracy score: ', accuracy)
        print('duration train activity: ', dur_train_activity,'seconds')
        print('duration train subject: ', dur_train_subj,'seconds')
        print('duration train both: ', dur_train_both ,'seconds')



class MetaData:
    def __init__(self):
        self.activityCol = 1
        self.activities = [1,2,3,4,5,6,7,12,13,16,17]

        # 1 – lying (# subj - 8)
        # 2 – sitting (# subj - 8)
        # 3 – standing (# subj - 8)
        # 4 – walking (# subj - 8)
        # 5 – running (# subj - 6)
        # 6 – cycling (# subj - 7)
        # 7 – Nordic walking (# subj - 7)
        # 9 – watching TV (# subj - 1)
        # 10 – computer work  (# subj - 4)
        # 11 – car driving (# subj - 1)
        # 12 – ascending stairs  (# subj - 8)
        # 13 – descending stairs  (# subj - 8)
        # 16 – vacuum cleaning  (# subj - 8)
        # 17 – ironing (# subj - 8)
        # 18 – folding laundry  (# subj - 4)
        # 19 – house cleaning  (# subj - 5)
        # 20 – playing soccer (# subj - 2)
        # 24 – rope jumping (# subj - 6)

    def getRawColumnNames(self):
        columnNames = ['timestamp', 'activity_id', 'heartrate_bpm']

        imuColumns = ['%s_temp_c', '%s_3d_accel_16_1', '%s_3d_accel_16_2', '%s_3d_accel_16_3',
                      '%s_3d_accel_6_1', '%s_3d_accel_6_2', '%s_3d_accel_6_3',
                      '%s_3d_gyroscope_1', '%s_3d_gyroscope_2', '%s_3d_gyroscope_3',
                      '%s_3d_magnetometer_1', '%s_3d_magnetometer_2', '%s_3d_magnetometer_3',
                      '%s_orientation_1', '%s_orientation_2', '%s_orientation_3', '%s_orientation_4']

        # Prefixes to be appended to imuColumns
        prefix = ['hand', 'chest', 'ankle']

        # Append prefixes to columns
        for l in range(0, 3):
            for imu in imuColumns:
                imu = str(imu) % prefix[l]
                columnNames.append(imu)

        columnNames.append('subject')

        return columnNames

    def getOriginalColsDataType(self):
        dataType = [('timestamp', 'float'), ('activity_id', 'float'), ('heartrate_bpm', 'float'),
                    # imu hand - accel
                    ('hand_temp_c', 'float'),
                    ('hand_3d_accel_16g_1', 'float'), ('hand_3d_accel_16g_2', 'float'),
                    ('hand_3d_accel_16g_3', 'float'),
                    ('hand_3d_accel_6g_1', 'float'), ('hand_3d_accel_6g_2', 'float'), ('hand_3d_accel_6g_3', 'float'),
                    # imu hand - gyro, magneto
                    ('hand_3d_gyroscope_1', 'float'), ('hand_3d_gyroscope_2', 'float'),
                    ('hand_3d_gyroscope_3', 'float'),
                    ('hand_3d_magnetometer_1', 'float'), ('hand_3d_magnetometer_2', 'float'),
                    ('hand_3d_magnetometer_3', 'float'),
                    # imu hand - orientation
                    ('hand_orientation_1', 'float'), ('hand_orientation_2', 'float'), ('hand_orientation_3', 'float'),
                    ('hand_orientation_4', 'float'),
                    # imu chest - accel
                    ('chest_temp_c', 'float'),
                    ('chest_3d_accel_16g_1', 'float'), ('chest_3d_accel_16g_2', 'float'),
                    ('chest_3d_accel_16g_3', 'float'),
                    ('chest_3d_accel_6g_1', 'float'), ('chest_3d_accel_6g_2', 'float'),
                    ('chest_3d_accel_6g_3', 'float'),
                    # imu chest - gyro, magneto
                    ('chest_3d_gyroscope_1', 'float'), ('chest_3d_gyroscope_2', 'float'),
                    ('chest_3d_gyroscope_3', 'float'),
                    ('chest_3d_magnetometer_1', 'float'), ('chest_3d_magnetometer_2', 'float'),
                    ('chest_3d_magnetometer_3', 'float'),
                    # imu chest - orientation
                    ('chest_orientation_1', 'float'), ('chest_orientation_2', 'float'),
                    ('chest_orientation_3', 'float'),
                    ('chest_orientation_4', 'float'),
                    # imu ankle - accel
                    ('ankle_temp_c', 'float'),
                    ('ankle_3d_accel_16g_1', 'float'), ('ankle_3d_accel_16g_2', 'float'),
                    ('ankle_3d_accel_16g_3', 'float'),
                    ('ankle_3d_accel_6g_1', 'float'), ('ankle_3d_accel_6g_2', 'float'),
                    ('ankle_3d_accel_6g_3', 'float'),
                    # imu ankle - gyro, magneto
                    ('ankle_3d_gyroscope_1', 'float'), ('ankle_3d_gyroscope_2', 'float'),
                    ('ankle_3d_gyroscope_3', 'float'),
                    ('ankle_3d_magnetometer_1', 'float'), ('ankle_3d_magnetometer_2', 'float'),
                    ('ankle_3d_magnetometer_3', 'float'),
                    # imu ankle - orientation
                    ('ankle_orientation_1', 'float'), ('ankle_orientation_2', 'float'),
                    ('ankle_orientation_3', 'float'),
                    ('ankle_orientation_4', 'float'),
                    ('subject', 'int')
                    ]
        return dataType
    def getProcessedColsDataType(self):
        dataType = [('heartrate_bpm', 'float'),
                    # imu hand - accel
                    ('hand_temp_c', 'float'),
                    ('hand_3d_accel_16g_1', 'float'), ('hand_3d_accel_16g_2', 'float'),
                    ('hand_3d_accel_16g_3', 'float'),
                    # imu hand - gyro, magneto
                    ('hand_3d_gyroscope_1', 'float'), ('hand_3d_gyroscope_2', 'float'),
                    ('hand_3d_gyroscope_3', 'float'),
                    ('hand_3d_magnetometer_1', 'float'), ('hand_3d_magnetometer_2', 'float'),
                    ('hand_3d_magnetometer_3', 'float'),
                    # imu chest - accel
                    ('chest_temp_c', 'float'),
                    ('chest_3d_accel_16g_1', 'float'), ('chest_3d_accel_16g_2', 'float'),
                    ('chest_3d_accel_16g_3', 'float'),
                    # imu chest - gyro, magneto
                    ('chest_3d_gyroscope_1', 'float'), ('chest_3d_gyroscope_2', 'float'),
                    ('chest_3d_gyroscope_3', 'float'),
                    ('chest_3d_magnetometer_1', 'float'), ('chest_3d_magnetometer_2', 'float'),
                    ('chest_3d_magnetometer_3', 'float'),
                    # imu ankle - accel
                    ('ankle_temp_c', 'float'),
                    ('ankle_3d_accel_16g_1', 'float'), ('ankle_3d_accel_16g_2', 'float'),
                    ('ankle_3d_accel_16g_3', 'float'),
                    # imu ankle - gyro, magneto
                    ('ankle_3d_gyroscope_1', 'float'), ('ankle_3d_gyroscope_2', 'float'),
                    ('ankle_3d_gyroscope_3', 'float'),
                    ('ankle_3d_magnetometer_1', 'float'), ('ankle_3d_magnetometer_2', 'float'),
                    ('ankle_3d_magnetometer_3', 'float'),
                    ('subject', 'float'),
                    ('activity_id', 'float')
                    ]
        return dataType

    def getResultColsDataType(self):
        dataType = [('heartrate_bpm', 'float'),
                    # imu hand - accel
                    ('hand_temp_c', 'float'),
                    ('hand_3d_accel_16g_1', 'float'), ('hand_3d_accel_16g_2', 'float'),
                    ('hand_3d_accel_16g_3', 'float'),
                    # imu hand - gyro, magneto
                    ('hand_3d_gyroscope_1', 'float'), ('hand_3d_gyroscope_2', 'float'),
                    ('hand_3d_gyroscope_3', 'float'),
                    ('hand_3d_magnetometer_1', 'float'), ('hand_3d_magnetometer_2', 'float'),
                    ('hand_3d_magnetometer_3', 'float'),
                    # imu chest - accel
                    ('chest_temp_c', 'float'),
                    ('chest_3d_accel_16g_1', 'float'), ('chest_3d_accel_16g_2', 'float'),
                    ('chest_3d_accel_16g_3', 'float'),
                    # imu chest - gyro, magneto
                    ('chest_3d_gyroscope_1', 'float'), ('chest_3d_gyroscope_2', 'float'),
                    ('chest_3d_gyroscope_3', 'float'),
                    ('chest_3d_magnetometer_1', 'float'), ('chest_3d_magnetometer_2', 'float'),
                    ('chest_3d_magnetometer_3', 'float'),
                    # imu ankle - accel
                    ('ankle_temp_c', 'float'),
                    ('ankle_3d_accel_16g_1', 'float'), ('ankle_3d_accel_16g_2', 'float'),
                    ('ankle_3d_accel_16g_3', 'float'),
                    # imu ankle - gyro, magneto
                    ('ankle_3d_gyroscope_1', 'float'), ('ankle_3d_gyroscope_2', 'float'),
                    ('ankle_3d_gyroscope_3', 'float'),
                    ('ankle_3d_magnetometer_1', 'float'), ('ankle_3d_magnetometer_2', 'float'),
                    ('ankle_3d_magnetometer_3', 'float'),
                    ('subject', 'float'),
                    ('activity_id', 'float'),
                    ('actual_subj_activity', 'float'),
                    ('predicted_subj_activity','float')
                    ]
        return dataType