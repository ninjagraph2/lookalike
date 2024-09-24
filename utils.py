import os
import numpy as np
import torch
import torchvision.transforms as transforms
import gradio as gr
import pickle
import tempfile
import shutil

from PIL import Image

from sklearn.neighbors import KDTree

class Lookalike():
    def __init__(self, model_path='mobilenet_v3_small.pth'):
        self.indexed = []  # Инициализация как пустой список
        self.image_paths = []  # Список для хранения путей к изображениям
        self.load_index()  # Загружаем индекс из файла, если он существует
        
        self.cnn_model = torch.load(model_path)
        self.cnn_model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((244, 244)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def load_index(self):
        """Загрузка индекса из файла."""
        if os.path.exists('search_index.pkl'):
            with open('search_index.pkl', 'rb') as file:
                self.indexed, self.image_paths = pickle.load(file)

    def save_index(self):
        """Сохранение индекса в файл."""
        with open('search_index.pkl', 'wb') as file:
            pickle.dump((self.indexed, self.image_paths), file)

    def extract_features(self, file):
        """Извлечение признаков из изображения."""
        image = Image.open(file).convert('RGB')
        image = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            features = self.cnn_model(image)
            features = features.view(features.size(1), -1)
        return features.numpy().flatten()

    def find_similar_images(self, num_images, query_features):
        """Поиск похожих изображений."""
        if len(self.indexed) == 0:
            return [], []  # Если нет изображений в индексе
        
        kdtree = KDTree(self.indexed)  # Создание KDTree из индекса
        query_features = query_features.reshape(1, -1)
        distances, indices = kdtree.query(query_features, k=num_images)
        
        similar_image_paths = [self.image_paths[i] for i in indices[0]]
        
        return similar_image_paths

    def add_to_index(self, new_images):
        """Добавление новых изображений в индекс."""
        for image in new_images:
            new_feature = self.extract_features(image)
            self.indexed.append(new_feature)
            self.image_paths.append(image)  # Сохраняем путь к изображению
        self.save_index()  # Сохраняем индекс после добавления новых изображений

def create_temp_storage():
    """Создание временной директории для хранения загруженных изображений."""
    temp_dir = tempfile.mkdtemp()
    return temp_dir

def cleanup(temp_dir):
    """Удаление временной директории и индексного файла."""
    shutil.rmtree(temp_dir)  # Удаляем временную директорию
    if os.path.exists('search_index.pkl'):
        os.remove('search_index.pkl')  # Удаляем индексный файл