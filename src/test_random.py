import os
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def predict_random(dataset_dir, model_path, image_size, num_images=5):
    # Load model
    model = load_model(model_path)

    # Get class names directly from dataset folder
    class_names = sorted(os.listdir(dataset_dir))

    for i in range(num_images):
        # Pick random class and random image
        chosen_class = random.choice(class_names)
        class_dir = os.path.join(dataset_dir, chosen_class)
        img_file = random.choice(os.listdir(class_dir))
        img_path = os.path.join(class_dir, img_file)

        print(f"\n[{i+1}/{num_images}] Randomly selected image: {img_path}")

        # Load and preprocess image
        img = image.load_img(img_path, target_size=(image_size, image_size))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predict
        preds = model.predict(img_array, verbose=0)
        idx = np.argmax(preds[0])
        confidence = preds[0][idx]

        label = class_names[idx]

        print(f"Prediction: {label} (confidence={confidence:.2f})")

        # Show image with prediction
        plt.imshow(img)
        plt.title(f"Prediction: {label}\nConfidence: {confidence:.2f}")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset")
    parser.add_argument("--model-path", type=str, required=True, help="Path to trained model (.keras)")
    parser.add_argument("--image-size", type=int, default=128, help="Image size used for training")
    parser.add_argument("--num-images", type=int, default=5, help="Number of random images to test")
    args = parser.parse_args()

    predict_random(args.dataset, args.model_path, args.image_size, args.num_images)
