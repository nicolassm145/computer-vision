"""
Script de Treinamento YOLOv11n para Detecção de LIBRAS
Autor: Nicolas
Data: 2025-11-11

Este script treina um modelo YOLOv11n para detectar letras do alfabeto em LIBRAS
(Linguagem Brasileira de Sinais) usando imagens de mãos.
"""

from ultralytics import YOLO
import os
from pathlib import Path

def train_model():
    """
    Treina o modelo YOLOv11n com os parâmetros especificados
    """
    print("=" * 60)
    print("TREINAMENTO YOLOV11N - DETECÇÃO DE LIBRAS")
    print("=" * 60)
    
    # Definir caminhos
    project_root = Path(__file__).parent.parent
    data_yaml = project_root / "config" / "data.yaml"
    
    print(f"\n📁 Diretório do projeto: {project_root}")
    print(f"📄 Arquivo de dados: {data_yaml}")
    
    # Verificar se o arquivo data.yaml existe
    if not data_yaml.exists():
        print(f"\n❌ ERRO: Arquivo {data_yaml} não encontrado!")
        return
    
    print("\n🔄 Carregando modelo YOLOv11n...")
    # Carregar modelo pré-treinado YOLOv11n
    model = YOLO('yolo11n.pt')
    
    print("\n📊 Informações do modelo:")
    print(f"   - Modelo: YOLOv11n (nano)")
    print(f"   - Classes: 22 (letras LIBRAS)")
    print(f"   - Dataset: Alfabeto em LIBRAS")
    
    print("\n🚀 Iniciando treinamento...")
    print("⏱️  Isso pode levar alguns minutos/horas dependendo do hardware\n")
    
    # Treinar o modelo
    results = model.train(
        data=str(data_yaml),           # Caminho para o arquivo YAML
        epochs=100,                     # Número de épocas (ajuste conforme necessário)
        imgsz=640,                      # Tamanho da imagem
        batch=16,                       # Tamanho do batch (ajuste conforme sua GPU)
        name='libras_yolo11n',          # Nome do experimento
        project=str(project_root / 'runs' / 'train'),  # Diretório de saída
        patience=20,                    # Early stopping patience
        save=True,                      # Salvar checkpoints
        device='cpu',                   # Use 'cpu' ou 0 para GPU
        workers=4,                      # Número de workers para data loading
        pretrained=True,                # Usar pesos pré-treinados
        optimizer='auto',               # Otimizador automático
        verbose=True,                   # Modo verbose
        seed=42,                        # Seed para reprodutibilidade
        deterministic=True,             # Treinamento determinístico
        plots=True,                     # Gerar gráficos
        val=True,                       # Validar durante o treinamento
    )
    
    print("\n" + "=" * 60)
    print("✅ TREINAMENTO CONCLUÍDO!")
    print("=" * 60)
    print(f"\n📁 Resultados salvos em: {project_root}/runs/train/libras_yolo11n")
    print(f"💾 Melhor modelo salvo em: {project_root}/runs/train/libras_yolo11n/weights/best.pt")
    print(f"📊 Gráficos e métricas disponíveis no diretório de resultados")
    
    return results

if __name__ == "__main__":
    try:
        results = train_model()
        print("\n🎉 Processo finalizado com sucesso!")
        print("\n📝 Próximos passos:")
        print("   1. Verifique os gráficos de treinamento em runs/train/libras_yolo11n")
        print("   2. Use validate.py para validar o modelo")
        print("   3. Use detect_webcam.py para testar com a webcam")
    except Exception as e:
        print(f"\n❌ Erro durante o treinamento: {str(e)}")
        import traceback
        traceback.print_exc()
