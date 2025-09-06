import argparse
import numpy as np
import json
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def predict(img_path, model_path, image_size=128):
    # Load model
    model = load_model(model_path)

    # Load class names
    with open("models/class_names.json", "r") as f:
        class_names = json.load(f)

    # Preprocess image
    img = image.load_img(img_path, target_size=(image_size, image_size))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    # Predict
    preds = model.predict(x)
    class_id = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))

    return class_names[class_id], confidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to an image file")
    parser.add_argument("--model-path", default="models/cnn_model.keras")
    parser.add_argument("--image-size", type=int, default=128)
    args = parser.parse_args()

    label, conf = predict(args.image, args.model_path, args.image_size)
    print(f"Prediction: {label} (confidence={conf:.2f})")
