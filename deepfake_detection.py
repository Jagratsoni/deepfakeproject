import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import cv2
import os
from mtcnn import MTCNN
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Initialize MTCNN for face detection
detector = MTCNN()

def build_model():
    base_model = tf.keras.applications.Xception(weights='imagenet', include_top=False, input_shape=(299, 299, 3))
    
    # Unfreeze the last 10 layers for fine-tuning
    for layer in base_model.layers[:-10]:
        layer.trainable = False
    for layer in base_model.layers[-10:]:
        layer.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)  # Add dropout to prevent overfitting
    x = Dense(512, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
                  loss='binary_crossentropy', 
                  metrics=['accuracy'])
    return model

def detect_face(image):
    # Convert image to RGB for MTCNN
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(image_rgb)
    
    if faces:
        # Get the first detected face
        x, y, w, h = faces[0]['box']
        # Add padding to the face region
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        face = image[y:y+h, x:x+w]
        return face
    return image  # Return original image if no face is detected

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(299, 299))
    img_array = img_to_array(img)
    
    # Load image for face detection
    img_cv = cv2.imread(image_path)
    face = detect_face(img_cv)
    
    # Resize face to target size
    face = cv2.resize(face, (299, 299))
    face_array = img_to_array(face)
    
    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        brightness_range=[0.8, 1.2],
        zoom_range=0.1
    )
    face_array = face_array.reshape((1,) + face_array.shape)
    augmented = next(datagen.flow(face_array, batch_size=1))[0]
    
    augmented = augmented / 255.0
    return augmented

def preprocess_video(video_path, max_frames=10):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        # Detect face in frame
        face = detect_face(frame)
        face = cv2.resize(face, (299, 299))
        face = face / 255.0
        frames.append(face)
        frame_count += 1
    cap.release()
    return np.array(frames)

def detect_deepfake(model, file_path, is_video=False):
    if is_video:
        frames = preprocess_video(file_path)
        if len(frames) == 0:
            return 0.0, "No frames extracted"
        predictions = []
        for frame in frames:
            frame = np.expand_dims(frame, axis=0)
            pred = model.predict(frame, verbose=0)[0][0]
            predictions.append(pred)
        # Use majority voting instead of averaging
        fake_count = sum(1 for pred in predictions if pred >= 0.5)
        total_frames = len(predictions)
        confidence = fake_count / total_frames
        return confidence, f"Average deepfake confidence: {confidence:.2%}"
    else:
        img = preprocess_image(file_path)
        pred = model.predict(img, verbose=0)[0][0]
        return pred, f"Deepfake confidence: {pred:.2%}"