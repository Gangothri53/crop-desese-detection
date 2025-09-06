import argparse, os, json
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from src.data_prep import get_data_generators
from src.model import build_model


def main(args):
    # Load data
    train_gen, val_gen, class_names = get_data_generators(args.data_dir, args.image_size, args.batch_size)
    print(f"✅ Classes found: {class_names}")

    # Build model
    model = build_model(len(class_names), args.image_size)

    # Make sure save folder exists
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)

    # Save class names to JSON
    with open("models/class_names.json", "w") as f:
        json.dump(class_names, f)
    print("📂 Class names saved at models/class_names.json")

    # Callbacks
    ckpt = ModelCheckpoint(args.save_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    early = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True, verbose=1)

    # Train
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=[ckpt, early]
    )

    print("✅ Training complete. Best model saved to:", args.save_path)
    return history


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="dataset")
    parser.add_argument("--image-size", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--save-path", type=str, default="models/cnn_model.keras")
    args = parser.parse_args()

    main(args)
import argparse, os, json
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from src.data_prep import get_data_generators
from src.model import build_model


def main(args):
    # Load data
    train_gen, val_gen, class_names = get_data_generators(args.data_dir, args.image_size, args.batch_size)
    print(f"✅ Classes found: {class_names}")

    # Build model
    model = build_model(len(class_names), args.image_size)

    # Make sure save folder exists
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)

    # Save class names to JSON
    with open("models/class_names.json", "w") as f:
        json.dump(class_names, f)
    print("📂 Class names saved at models/class_names.json")

    # Callbacks
    ckpt = ModelCheckpoint(args.save_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    early = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True, verbose=1)

    # Train
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=[ckpt, early]
    )

    print("✅ Training complete. Best model saved to:", args.save_path)
    return history


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="dataset")
    parser.add_argument("--image-size", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--save-path", type=str, default="models/cnn_model.keras")
    args = parser.parse_args()

    main(args)
