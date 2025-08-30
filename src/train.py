import argparse
import tensorflow as tf
from src.model import build_model

def main(args):
    # Load dataset
    train_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(args.image_size, args.image_size),
        batch_size=args.batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(args.image_size, args.image_size),
        batch_size=args.batch_size
    )

    class_names = train_ds.class_names
    print(f"✅ Classes found: {class_names}")

    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Build model
    model = build_model(len(class_names), args.image_size)

    # Compile model
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Train model
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs
    )

    # Save model
    model.save(args.save_path)
    print(f"✅ Model saved at {args.save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, required=True, help="Path to dataset directory")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--image-size", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--save-path", type=str, default="models/cnn_model.keras")

    args = parser.parse_args()
    main(args)
