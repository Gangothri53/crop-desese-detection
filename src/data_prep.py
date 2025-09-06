import tensorflow as tf

def get_data_generators(data_dir, img_size, batch_size):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_size, img_size),
        batch_size=batch_size
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_size, img_size),
        batch_size=batch_size
    )

    # ✅ Save class names before prefetch
    class_names = train_ds.class_names

    # 🔹 Data augmentation pipeline
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomTranslation(0.2, 0.2),
        tf.keras.layers.RandomContrast(0.2),
    ])

    # ✅ Apply normalization and augmentation only to training
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = (
        train_ds
        .map(lambda x, y: (data_augmentation(x, training=True) / 255.0, y), 
             num_parallel_calls=AUTOTUNE)
        .cache()
        .shuffle(1000)
        .prefetch(buffer_size=AUTOTUNE)
    )

    val_ds = (
        val_ds
        .map(lambda x, y: (x / 255.0, y), num_parallel_calls=AUTOTUNE)
        .cache()
        .prefetch(buffer_size=AUTOTUNE)
    )

    return train_ds, val_ds, class_names
