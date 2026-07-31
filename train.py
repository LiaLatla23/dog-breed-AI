import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# 1. Configuración
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Usando:", device)

# 2. Transformaciones de las imágenes
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 3. Cargar datasets
train_dataset = datasets.ImageFolder(
    "dataset/train",
    transform=transform
)

validation_dataset = datasets.ImageFolder(
    "dataset/validation",
    transform=transform
)

# 4. Crear DataLoaders
train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=16,
    shuffle=False
)

print("Clases:", train_dataset.classes)

# 5. Cargar ResNet18 preentrenada
model = models.resnet18(weights="DEFAULT")

# 6. Cambiar la última capa para nuestras 6 razas
model.fc = nn.Linear(model.fc.in_features, 6)

model = model.to(device)

# 7. Función de pérdida y optimizador
criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

# 8. Entrenamiento
epochs = 10

for epoch in range(epochs):

    model.train()

    running_loss = 0.0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    # 9. Validation
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in validation_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total

    print(
        f"Epoch {epoch + 1}/{epochs} "
        f"- Loss: {running_loss / len(train_loader):.4f} "
        f"- Validation Accuracy: {accuracy:.2f}%"
    )

# 10. Guardar modelo
torch.save(model.state_dict(), "dog_breed_model.pth")

print("Modelo guardado como dog_breed_model.pth")