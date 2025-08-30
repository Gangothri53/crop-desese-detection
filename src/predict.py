import argparse
import numpy as np
from src.model import build_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def predict(img_path, model_path, image_size=128):
    model = load_model(model_path)
    img = image.load_img(img_path, target_size=(image_size, image_size))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    class_id = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))
    return f"class_{class_id}", confidence

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to an image file")
    parser.add_argument("--model-path", default="models/cnn_model.keras")
    parser.add_argument("--image-size", type=int, default=128)
    args = parser.parse_args()

    label, conf = predict(args.image, args.model_path, args.image_size)
    print(f"Prediction: {label} (confidence={conf:.2f})")
s