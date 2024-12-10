from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import numpy as np
import os

DATA_PATH = os.path.join('MP_Data')
actions = np.array([ 'Ndi', 'musanyufu',  'okubalaba'])
no_sequences = 30
sequence_length = 30

label_map ={label: num for num, label in enumerate(actions)}

sequences, labels = [], []

for action in actions:
    print(actions)
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), f'{frame_num}.npy'))
            if res.shape != (1662,):  # Replace with the actual expected shape
                print('shape: ', res.shape)
                raise ValueError(f"Unexpected shape {res.shape} in {action}/{sequence}/{frame_num}.npy")
            
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])




X = np.array(sequences)
y = to_categorical(labels).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)


model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))


model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])
print(model.summary())

print(model.predict(X_test))
model.save('action.h5')