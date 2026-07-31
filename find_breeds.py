import os

dataset_path = "Images"

breeds = [
    "Beagle",
    "Golden_retriever",
    "German_shepherd",
    "Siberian_husky",
    "Labrador_retriever",
    "Rottweiler"
]

print("Razas encontradas:\n")

for folder in os.listdir(dataset_path):
    for breed in breeds:
        if breed.lower() in folder.lower():
            print(folder)