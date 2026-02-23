import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from sklearn.model_selection import train_test_split
import pickle


try:
    df = pd.read_csv("benign_vs_defacement_urls.csv", encoding='latin1', on_bad_lines='skip')
except Exception as e:
    print("❌ Error loading CSV:", e)
    exit()

df['label'] = df['type'].map({'benign': 0, 'defacement': 1})
df = df[['url', 'label']]


benign_df = df[df['label'] == 0]
deface_df = df[df['label'] == 1]

min_count = min(len(benign_df), len(deface_df))
benign_df = benign_df.sample(min_count)
deface_df = deface_df.sample(min_count)

df = pd.concat([benign_df, deface_df]).sample(frac=1)
df = df[df['url'].apply(lambda x: isinstance(x, str))]



tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(df['url'])
sequences = tokenizer.texts_to_sequences(df['url'])
X = pad_sequences(sequences, maxlen=200)
y = df['label'].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=200),
    Conv1D(filters=128, kernel_size=3, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.1)

# Evaluate on test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\n📊 Test Accuracy: {accuracy * 100:.2f}%")
print(f"📊 Test Loss: {loss:.4f}")


model.save("urlnet_model.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ Training complete. Model and tokenizer saved.")
