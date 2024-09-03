import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy
# Set parameters
vocab_size = 5000
embedding_dim = 64
max_length = 100
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"


processed_data=[['titulo'], [], ['son', '3', 'la', 'muertes', 'conocidas', 'en', 'el', 'día', 'de', 'hoy'], [], ['noticia'], [], ['hacer', 'balance', 'de', 'una', 'pandemia', 'e', 'algo', 'que', 'ni', 'los', 'expertos', 'se', 'atreven', 'todavía'], ['hacer', 'cuando', 'los', 'registros', 'diarios', 'siguen', 'arrojando', 'fallecidos', 'por', 'un', 'virus', 'que', 'seguirá'], ['mucho', 'tiempo', 'entre', 'nosotros', 'aunque', 'provoque', 'menos', 'daños', 'españa', 'atraviesa', 'en', 'estas', 'semanas'], ['el', 'final', 'de', 'la', 'fase', 'epidémica'], [], ['resumen'], [], ['se', 'ha', 'confirmado', 'el', 'mejor', 'registro', 'de', 'hospitalizados', 'de', 'la', 'serie', 'histórica', 'nunca', 'ante'], ['habíamos', 'tenido', 'menos', 'de', '2.100', 'persona', 'ingresadas', 'por', 'la', 'infección', 'desde', 'que', 'se', 'registra', 'la', 'capacidad', 'asistencial']]
training_size = len(processed_data)

# Create tokenizer
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(processed_data)
word_index = tokenizer.word_index

# Create sequences
sequences = tokenizer.texts_to_sequences(processed_data)
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

# Create training data
training_data = padded_sequences[:training_size]
training_labels = padded_sequences[:training_size]

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv1D(64, 5, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=4),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

# Compile model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
num_epochs = 50
history = model.fit(training_data, training_labels, epochs=num_epochs, verbose=2)

# Define function to predict answer
def predict_answer(model, tokenizer, question):
    # Preprocess question
    question = preprocess(question)
    # Convert question to sequence
    sequence = tokenizer.texts_to_sequences([question])
    # Pad sequence
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    # Predict answer
    pred = model.predict(padded_sequence)[0]
    # Get index of highest probability
    idx = np.argmax(pred)
    # Get answer
    answer = tokenizer.index_word[idx]
    return answer

# Start chatbot
while True:
    question = input('You: ')
    answer = predict_answer(model, tokenizer, question)
    print('Chatbot:', answer)