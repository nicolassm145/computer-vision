import os
import yaml
from ultralytics import YOLO

def export_model_to_onnx():
    """
    Exporta o modelo treinado para ONNX
    """
    # Caminho para o melhor modelo treinado
    model_path = "runs/detect/train/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"Erro: Modelo {model_path} não encontrado!")
        return None
    
    # Carregar modelo
    model = YOLO(model_path)
    
    try:
        # Exportar para ONNX
        print("Exportando modelo para ONNX...")
        onnx_path = model.export(format='onnx', imgsz=640)
        print(f"Modelo ONNX salvo em: {onnx_path}")
        return onnx_path
        
    except Exception as e:
        print(f"Erro durante exportação ONNX: {e}")
        # Tentar copiar o modelo .pt para usar diretamente
        import shutil
        try:
            shutil.copy2(model_path, "best.pt")
            print("Modelo PyTorch copiado como best.pt para uso direto")
            return "best.pt"
        except Exception as e2:
            print(f"Erro ao copiar modelo: {e2}")
            return None

if __name__ == "__main__":
    export_model_to_onnx()