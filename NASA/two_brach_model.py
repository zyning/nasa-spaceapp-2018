from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, Input, LSTM, RepeatVector, Dense, Dropout,concatenate,Conv2D,UpSampling2D,MaxPooling2D,BatchNormalization,Activation,Add,GlobalMaxPool2D,Flatten
from keras.models import Model
import keras.backend as K
from keras.utils import plot_model
from IPython.display import Image
import pandas as pd
import cv2
from word2vecReader import Word2Vec
import numpy as np
from keras.utils import to_categorical
import keras

df = pd.read_csv('/home/pengyuan/PycharmProjects/NASA_2018/train.csv')
df_2 = pd.read_csv('/home/pengyuan/PycharmProjects/NASA_2018/test.csv')

label = to_categorical(df['labels'].values)
print(label.shape)
label_2  = to_categorical(df_2['labels'].values)
def process_images(df, final_shape=(158, 158)):
    # Set up array.
    X = []

    # Get each filename, read, resize, and append to X.
    for file in df.image:
        try:
            image = cv2.resize(cv2.imread(file), final_shape)
        except:
            print(file)
        X.append(image)
    # Normalize the array as a float.
    X = np.asarray(X)
    X = X.reshape(X.shape[0],158,158,3)
    X = X / 255.

    return X

text = []
text_ = []

text_test = []
text_test_ = [ ]
text.append(df['text'].values)
for tweet in text:
    for t in tweet:
        text_.append(t)
print(text_)

text_test.append(df_2['text'].values)
for tweet in text_test:
    for t in tweet:
        text_test_.append(t)
print(text_test_)

all_sentences_test = text_test_
tokenizer_test = Tokenizer()  # nb_words=MAX_NB_WORDS
tokenizer_test.fit_on_texts(all_sentences_test)
sequences_test = tokenizer_test.texts_to_sequences(all_sentences_test)
word_index_test = tokenizer_test.word_index
print('Found %s unique tokens.' % len(word_index_test))
x_test = pad_sequences(sequences_test,maxlen=12)
print(x_test.shape)

all_sentences = text_
tokenizer = Tokenizer()  # nb_words=MAX_NB_WORDS
tokenizer.fit_on_texts(all_sentences)
sequences = tokenizer.texts_to_sequences(all_sentences)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

x_train = pad_sequences(sequences)
print(x_train.shape)
model = Word2Vec.load_word2vec_format("/home/pengyuan/PycharmProjects/Multimodal_Study/Twitter_word2vec/word2vec_twitter_model.bin",binary=True)
pretrained_weights = model.syn0
vocab_size, emdedding_size = pretrained_weights.shape
print(vocab_size, emdedding_size)
embedding_matrix = np.zeros((len(word_index) + 1, 400))
for word, i in word_index.items():
    if word in model:
        embedding_matrix[i] = model[word]
    else:
        embedding_matrix[i] = np.random.rand(1, 400)[0]

image_data = process_images(df)
print(image_data.shape)
image_data_test = process_images(df_2)



Input_text = Input(shape=(12,))
Input_image = Input(shape=(158,158,3))

embedding_layer = Embedding(len(word_index) + 1,
                                400,
                                weights=[embedding_matrix],
                                input_length=12,
                                trainable=False)
embedded_sequences = embedding_layer(Input_text)

encoded_text = LSTM(32)(embedded_sequences)

encoded_img = Conv2D(128,(3,3),activation='relu',padding='same')(Input_image)
encoded_img = MaxPooling2D((2,2),padding='same')(encoded_img)
encoded_img = Conv2D(64,(3,3),activation='relu',padding='same')(encoded_img)
encoded_img = MaxPooling2D((2,2),padding='same')(encoded_img)
encoded_img = Conv2D(32,(3,3),activation='relu',padding='same')(encoded_img)
encoded_img = MaxPooling2D((2,2),padding='same')(encoded_img)

combined_features = Add(name="add")([encoded_text,encoded_img])

combined_features = Flatten()(combined_features)
combined_features= Dense(512)(combined_features)
output = Dense(4,activation='softmax')(combined_features)


two_branch = Model([Input_text,Input_image],output)

two_branch.compile(loss='categorical_crossentropy',
              optimizer='adadelta', metrics=['accuracy'])

print(two_branch.summary())

plot_model(two_branch,to_file='./model_image/two_branch.png',show_shapes=True)
Image(filename='./model_image/two_branch.png')

two_branch.fit([x_train,image_data],label,batch_size=32,epochs=100,validation_data=([x_test,image_data_test],label_2),shuffle=True)
two_branch.save_weights("./weights_saved/two_branch.h5")

# image = cv2.resize(cv2.imread('./WIldfire/fire_scecne/images (33).jpg'), (158,158))
# X = np.asarray(image)
# X = X.reshape(1, 158, 158, 3)
# X = X / 255.
#
# text=['Big fire in forest']
# tokenizer_1 = Tokenizer()  # nb_words=MAX_NB_WORDS
# tokenizer_1.fit_on_texts(text)
# sequences_1 = tokenizer_1.texts_to_sequences(text)
# text = pad_sequences(sequences_1,maxlen=12)
#
# print(two_branch.predict([text,X]))
