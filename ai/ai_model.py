# This is the AI model that uses the data about water quality to predict next weeks
from datetime import datetime
import csv
import numpy as np
import argparse
import tensorflow as tf


def convert_item_from_string(item):

    try:
        return float(item)
    except ValueError:
        return datetime.strptime(item, '%Y-%m-%d').date()

def read_training_data_s_r(file_path):
    """
    This function pre
    :return:
    """
    # the data for model is taken from here:
    data_rows = []
    places = []
    column_labels = []
    # Open the CSV file
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        row_i = 0
        for row in reader:
            if (row_i == 0):
                cities = row
            if (row_i == 1):
                places = row
            if (row_i == 2):
                column_labels = row
            if (row_i >= 3):
                row = [e.replace('"', '').replace(',', '.') for e in row]
                row = [(e if e != '<2' else 0.05) for e in row]
                row = [(e if e != '' else '-1.0') for e in row]
                row = [convert_item_from_string(e) for e in row]
                if (row[1] != -1):
                    data_rows = data_rows + [row]
            row_i = row_i + 1

    return (data_rows, column_labels, places, cities)

def read_training_data_d(file_path):
    """
    This function pre
    :return:
    """
    # the data for model is taken from here:
    data_rows = []
    places = []
    column_labels = []
    table_label = '<<undefined>>'
    # Open the CSV file
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        row_i = 0
        for row in reader:
            if (row_i == 0):
                table_label = row[1]
            if (row_i == 2):
                places = row
            if (row_i == 4):
                column_labels = row
            if (row_i >= 6):
                row = [e.replace('"', '').replace(',', '.') for e in row]
                row = [(e if e != '<2' else 0.05) for e in row]
                row = [(e if e != '' else '-1.0') for e in row]
                row = [convert_item_from_string(e) for e in row]
                if (row[1] != -1):
                    while (len(row) < len (places)):
                        row = row + [-1]
                    data_rows = data_rows + [row]
            row_i = row_i + 1
    return (data_rows, column_labels, places, table_label)


def create_model(input_data_row, output_data_row):
    print(input_data_row, output_data_row)
    print(len(input_data_row), len(output_data_row))
    layers = [
        tf.keras.layers.Input(shape=(len(input_data_row),)),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(len(output_data_row), activation='linear')]
    model = tf.keras.Sequential(layers)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mean_absolute_error')
    # model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'])
    return model

def train_model(x_train, y_train):
    """
    trains predictie model for timeseries
    :return: trained model
    """

    logdir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

    x_train = np.array([ np.asarray(np.reshape(x, -1)).astype('float32') for x in x_train ], dtype=np.float32)
    y_train = np.array([ np.asarray(y).astype('float32') for y in y_train ], dtype=np.float32)

    model = create_model(x_train[0], y_train[0])

    history = model.fit(x_train, y_train, epochs=1000, callbacks=[tensorboard_callback])

    return model

def generate_x_y(data_rows):
    columns = len(data_rows[0])
    rows = len(data_rows)
    window_size = 3
    training_x = []
    training_y = []
    print(rows)
    for i in range(window_size, rows):
        training_x_item = []
        for j in range(i-window_size, i):
            training_x_item = training_x_item + [data_rows[j]]
        training_x = training_x + [training_x_item]
        training_y = training_y+[data_rows[i]]
    # data_rows = np.array(data_rows)
    # print (data_rows)
    # data_rows = data_rows[:1:columns]
    training_x = np.array(training_x)[:,:,1:columns]
    training_y = np.array(training_y)[:,1:columns]
    return (training_x, training_y)

def fill_unknown_values_if_possible(data_rows):
    # for each column, we should see if there are some holes in data
    for x in range(1,len(data_rows[0])):
        for y in range(1,len(data_rows)-1):
            data_rows[y][x] = data_rows[y][x] if (data_rows[y][x] >= 0) else (data_rows[y-1][x]+data_rows[y+1][x])/2.0
        data_rows[len(data_rows)-1][x] = data_rows[len(data_rows)-1][x] if (data_rows[len(data_rows)-1][x] >= 0) else data_rows[len(data_rows)-2][x]
        data_rows[0][x] = data_rows[0][x] if (data_rows[0][x] >= 0) else data_rows[1][x]
    return data_rows
def main():

    parser = argparse.ArgumentParser(description="AI Model Genertor for predicting water pollution")
    parser.add_argument('--predict', type=bool, default=False, help='Predict next data row based on the previous data.')
    args = parser.parse_args()

    #data_rows, column_labels, places, cities = read_training_data_s_r('data/stavanger-randaberg-data.csv')
    #print(data_rows)
    data_rows, column_labels, places, table_label = read_training_data_d('data/datapoints2023.csv')
    inputs_table = np.array(data_rows)
    print(data_rows)
    data_rows = fill_unknown_values_if_possible(data_rows)
    data_x, data_y = generate_x_y(data_rows)
    print(data_x)
    print(data_y)

    train_model(data_x, data_y)
#

if __name__ == '__main__':
    main()
