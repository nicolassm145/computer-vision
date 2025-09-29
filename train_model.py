import os
import yaml
from ultralytics import YOLO

def train_yolov11_model():
    """
    Treina um modelo YOLOv11n para detecção de linguagem de sinais
    """
    # Verificar se o arquivo de configuração existe
    config_path = "dataset/data.yaml"
    if not os.path.exists(config_path):
        print(f"Erro: Arquivo {config_path} não encontrado!")
        return None
    
    # Carregar configurações do dataset
    with open(config_path, 'r') as file:
        data_config = yaml.safe_load(file)
    
    print(f"Dataset carregado com {data_config['nc']} classes:")
    print(f"Classes: {data_config['names']}")
    
    # Inicializar modelo YOLOv11n
    model = YOLO('yolo11n.pt')  # Carrega modelo pré-treinado
    
    # Configurações de treinamento
    train_args = {
        'data': config_path,
        'epochs': 100,
        'imgsz': 640,
        'batch': 16,
        'device': 'cpu',  # Use 'cuda' se tiver GPU
        'workers': 4,
        'patience': 20,
        'save_period': 10,
        'val': True,
        'plots': True,
        'verbose': True
    }
    
    print("Iniciando treinamento do modelo YOLOv11n...")
    print("Isso pode levar algumas horas dependendo do hardware.")
    
    try:
        # Treinar o modelo
        results = model.train(**train_args)
        
        print("Treinamento concluído!")
        print(f"Melhor modelo salvo em: {model.trainer.best}")
        
        # Exportar para ONNX
        print("Exportando modelo para ONNX...")
        onnx_path = model.export(format='onnx', imgsz=640)
        print(f"Modelo ONNX salvo em: {onnx_path}")
        
        return onnx_path
        
    except Exception as e:
        print(f"Erro durante o treinamento: {e}")
        return None

if __name__ == "__main__":
    train_yolov11_model()