import tensorflow as tf
from tensorflow import ImageDataGenerator, load_img, img_to_array
from deepfake_detection import build_model
import os
import pandas as pd
import numpy as np

# Define dataset directories (for generating CSV)
base_dir = 'D:/Major Project/dataset'
train_real_dir = os.path.join(base_dir, 'train/real')
train_fake_dir = os.path.join(base_dir, 'train/fake')
val_real_dir = os.path.join(base_dir, 'val/real')
val_fake_dir = os.path.join(base_dir, 'val/fake')

# Generate CSV file
data = []
for dir_path, label in [(train_real_dir, 0), (train_fake_dir, 1), (val_real_dir, 0), (val_fake_dir, 1)]:
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(dir_path, file_name)
                data.append({'file_path': file_path, 'label': label})

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('deepfake_dataset.csv', index=False)
print("CSV file created: deepfake_dataset.csv")

# Load the CSV file
try:
    dataset = pd.read_csv('deepfake_dataset.csv')
except FileNotFoundError:
    raise FileNotFoundError("deepfake_dataset.csv not found. Ensure the CSV file was generated correctly.")

# Check if the CSV is empty
if dataset.empty:
    raise ValueError("The dataset CSV is empty. Ensure your dataset directories contain images and the CSV was generated correctly.")

# Split into train and validation sets
train_data = dataset[dataset['file_path'].str.contains('train')]
val_data = dataset[dataset['file_path'].str.contains('val')]

# Check if train and validation data are available
if train_data.empty:
    raise ValueError("No training data found in the CSV. Ensure 'train' directory contains images.")
if val_data.empty:
    raise ValueError("No validation data found in the CSV. Ensure 'val' directory contains images.")

# Custom data generator
def create_data_generator(data, batch_size=32, augment=True):
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20 if augment else 0,
        width_shift_range=0.2 if augment else 0,
        height_shift_range=0.2 if augment else 0,
        brightness_range=[0.8, 1.2] if augment else None,
        zoom_range=0.2 if augment else 0,
        horizontal_flip=True if augment else False
    )

    while True:
        for start in range(0, len(data), batch_size):
            batch_data = data[start:start + batch_size]
            images = []
            labels = []
            for _, row in batch_data.iterrows():
                try:
                    img = load_img(row['file_path'], target_size=(299, 299))
                    img_array = img_to_array(img)
                    images.append(img_array)
                    labels.append(row['label'])
                except Exception as e:
                    print(f"Warning: Could not load image {row['file_path']}: {e}")
                    continue
            if not images:  # Skip empty batches
                continue
            images = np.array(images)
            labels = np.array(labels)
            if augment:
                images = next(datagen.flow(images, batch_size=len(images), shuffle=False))
            else:
                images = images / 255.0
            yield images, labels

# Create generators
batch_size = 32
train_generator = create_data_generator(train_data, batch_size=batch_size, augment=True)
val_generator = create_data_generator(val_data, batch_size=batch_size, augment=False)

# Calculate steps per epoch
steps_per_epoch = len(train_data) // batch_size
validation_steps = len(val_data) // batch_size

# Ensure steps are at least 1
steps_per_epoch = max(1, steps_per_epoch)
validation_steps = max(1, validation_steps)

# Build and fine-tune the model
model = build_model()
model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps,
    verbose=1
)

# Save the fine-tuned model
model.save('fine_tuned_deepfake_model.h5')
print("Model saved as 'fine_tuned_deepfake_model.h5'")