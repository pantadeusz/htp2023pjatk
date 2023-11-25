# This is the AI model that uses the data about water quality to predict next weeks
import argparse
import csv
from datetime import datetime

import numpy as np
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


def read_training_data_d(file_path, exclude_places=set(['5b', '5c'])):
    """
    This function pre
    :return:
    """
    # the data for model is taken from here:
    data_rows = []
    places = []
    column_labels = []
    units = []
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
                last_e = ''
                for e in row:
                    if e != '': last_e = e
                    column_labels.append(last_e)
                for i in range(len(row), len(places)): column_labels.append(last_e)
            if (row_i == 5):
                units = row
            if (row_i >= 6):
                row = [e.replace('"', '').replace(',', '.') for e in row]
                row = [(e if e != '<2' else 0.05) for e in row]
                row = [(e if e != '' else '-1.0') for e in row]
                row = [convert_item_from_string(e) for e in row]
                if (row[1] != -1):
                    while (len(row) < len(places)):
                        row = row + [-1]
                    real_row = []
                    for i in range(0, len(row)):
                        if not (places[i] in exclude_places): real_row.append(row[i])
                    data_rows = data_rows + [row]
            row_i = row_i + 1
    return (data_rows, column_labels, places, table_label, units)


def create_model(input_data_row, output_data_row):
    layers = [
        tf.keras.layers.Input(shape=(len(input_data_row),)),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(len(output_data_row), activation='linear')]
    model = tf.keras.Sequential(layers)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mean_absolute_error')
    return model


def train_model(x_train, y_train):
    """
    trains predictie model for timeseries
    :return: trained model
    """

    logdir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

    x_train = np.array([np.asarray(np.reshape(x, -1)).astype('float32') for x in x_train], dtype=np.float32)
    y_train = np.array([np.asarray(y).astype('float32') for y in y_train], dtype=np.float32)

    model = create_model(x_train[0], y_train[0])

    history = model.fit(x_train, y_train, epochs=200, callbacks=[tensorboard_callback])
    print(history)
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
        for j in range(i - window_size, i):
            training_x_item = training_x_item + [data_rows[j]]
        training_x = training_x + [training_x_item]
        training_y = training_y + [data_rows[i]]

    training_x = np.array(training_x)[:, :, 1:columns]
    training_y = np.array(training_y)[:, 1:columns]
    return (training_x, training_y)


def fill_unknown_values_if_possible(data_rows):
    # for each column, we should see if there are some holes in data
    for x in range(1, len(data_rows[0])):
        for y in range(1, len(data_rows) - 1):
            data_rows[y][x] = data_rows[y][x] if (data_rows[y][x] >= 0) else (data_rows[y - 1][x] + data_rows[y + 1][
                x]) / 2.0
        data_rows[len(data_rows) - 1][x] = data_rows[len(data_rows) - 1][x] if (
                    data_rows[len(data_rows) - 1][x] >= 0) else data_rows[len(data_rows) - 2][x]
        data_rows[0][x] = data_rows[0][x] if (data_rows[0][x] >= 0) else data_rows[1][x]
    return data_rows


def predict_for_data(model, input_rows):
    print(input_rows)
    x_input = []
    for i in input_rows: x_input = x_input + i
    x_input = np.array([x_input], dtype=np.float32)
    print(x_input)
    prediction = model.predict([x_input])
    return prediction


def augment_data(x_train, y_train, n=5, noise=0.01):
    augmented_x = []
    augmented_y = []

    for i in range(len(x_train)):
        for _ in range(n):
            data = x_train[i]
            augmented_x.append(data + noise * np.random.randn(*data.shape))
            augmented_y.append(y_train[i])

    return np.array(augmented_x), np.array(augmented_y)





def do_the_prediction(steps_back=0, input_datapoints='data/datapoints2023.csv', model_path='keras_predict_model',
                      exclude_places=set(['5b', '5c'])):
    """
    This function generates the prediction about future water quality based on the historical data provided in the
    file. The example is provided in data/datapoints2023.csv
    :param steps_back: how old the prediction should be. If 0, then it predicts next data point unknown to the model
    :param input_datapoints: the file where the data for prediction is located.
    :param model_path: where to save the prediction model
    :param exclude_places: what places should be excluded. For example, there are almost no data for 5b and 5c
    :return: the prediction for each place except for the excluded ones
    """
    # load the data
    data_rows, column_labels, places, table_label, units = read_training_data_d(input_datapoints, exclude_places)
    # fix unknowns
    data_rows = fill_unknown_values_if_possible(data_rows)

    model = None
    try:
        model = tf.keras.models.load_model(model_path)
    except:
        data_x, data_y = generate_x_y(data_rows)
        data_x, data_y = augment_data(data_x, data_y, n=500, noise=0.01)
        model = train_model(data_x, data_y)
        model.save(model_path)

    how_old_the_data_should_be = steps_back
    row_index = len(data_rows) - how_old_the_data_should_be
    prediction = predict_for_data(model, [data_rows[row_index - 3][1:], data_rows[row_index - 2][1:],
                                          data_rows[row_index - 1][1:]])
    #print(prediction[0])
    #if (len(data_rows) > row_index): print(data_rows[row_index][1:])

    ret = []
    j = 0
    for i in range(1, len(places)):
        if not (places[i] in exclude_places):
            ret.append({
                "type": column_labels[i],
                "unit": units[i],
                "value": float(prediction[0][j]),
                "sensor": places[i]
            })
            j = j + 1
    return {
        'description': {
            'Tot-P': 'Total Phosphorus',
            'PO4': 'Phosphate',
            'Tot-N': 'Total Nitrogen',
            'SS': 'Suspended Solids'
        },
        'values': ret
    }


def main():
    parser = argparse.ArgumentParser(description="AI Model Genertor for predicting water pollution")
    parser.add_argument('--predict', type=bool, default=False, help='Predict next data row based on the previous data.')
    args = parser.parse_args()
    print(do_the_prediction(1, exclude_places=set(['5b', '5c'])))


if __name__ == '__main__':
    main()
