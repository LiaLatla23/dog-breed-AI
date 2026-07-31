import os
import shutil
import random

source = "Images"

breeds = {
    "n02088364-beagle": "beagle",
    "n02099601-golden_retriever": "golden_retriever",
    "n02099712-Labrador_retriever": "labrador",
    "n02106550-Rottweiler": "rottweiler",
    "n02106662-German_shepherd": "german_shepherd",
    "n02110185-Siberian_husky": "husky"
}

splits = {
    "train": 0.70,
    "validation": 0.15,
    "test": 0.15
}

random.seed(42)

for split in splits:
    for breed in breeds.values():
        os.makedirs(f"dataset/{split}/{breed}", exist_ok=True)

for original_breed, new_breed in breeds.items():

    source_folder = os.path.join(source, original_breed)

    images = [
        file for file in os.listdir(source_folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    random.shuffle(images)

    total = len(images)

    train_end = int(total * 0.70)
    validation_end = int(total * 0.85)

    train_images = images[:train_end]
    validation_images = images[train_end:validation_end]
    test_images = images[validation_end:]

    groups = {
        "train": train_images,
        "validation": validation_images,
        "test": test_images
    }

    for split, split_images in groups.items():

        for image in split_images:

            source_file = os.path.join(source_folder, image)
            destination_file = os.path.join(
                "dataset",
                split,
                new_breed,
                image
            )

            shutil.copy2(source_file, destination_file)

    print(
        f"{new_breed}: "
        f"{len(train_images)} train, "
        f"{len(validation_images)} validation, "
        f"{len(test_images)} test"
    )

print("\nDataset preparado correctamente.")