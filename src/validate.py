"""
Script de Validação do Modelo YOLOv11n
Autor: Nicolas
Data: 2025-11-11

Este script valida o modelo treinado no conjunto de teste
e gera métricas de desempenho.
"""

from ultralytics import YOLO
from pathlib import Path
import os

def validate_model(model_path=None):
    """
    Valida o modelo treinado
    
    Args:
        model_path: Caminho para o modelo. Se None, usa o último treinado.
    """
    print("=" * 60)
    print("VALIDAÇÃO DO MODELO YOLOV11N - LIBRAS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    data_yaml = project_root / "config" / "data.yaml"
    
    # Se não foi especificado um modelo, usar o melhor modelo do último treinamento
    if model_path is None:
        model_path = project_root / "runs" / "train" / "libras_yolo11n" / "weights" / "best.pt"
    
    print(f"\n📁 Diretório do projeto: {project_root}")
    print(f"💾 Modelo: {model_path}")
    print(f"📄 Dados: {data_yaml}")
    
    # Verificar se o modelo existe
    if not Path(model_path).exists():
        print(f"\n❌ ERRO: Modelo não encontrado em {model_path}")
        print("   Execute primeiro o script train.py para treinar o modelo.")
        return
    
    print("\n🔄 Carregando modelo...")
    model = YOLO(str(model_path))
    
    print("\n📊 Iniciando validação no conjunto de teste...")
    
    # Validar o modelo
    metrics = model.val(
        data=str(data_yaml),
        split='test',                   # Usar conjunto de teste
        batch=16,
        imgsz=640,
        device='cpu',                   # Use 0 para GPU
        plots=True,                     # Gerar gráficos
        save_json=True,                 # Salvar resultados em JSON
        project=str(project_root / 'runs' / 'val'),
        name='libras_yolo11n_validation'
    )
    
    print("\n" + "=" * 60)
    print("📈 RESULTADOS DA VALIDAÇÃO")
    print("=" * 60)
    print(f"\n🎯 mAP50: {metrics.box.map50:.4f}")
    print(f"🎯 mAP50-95: {metrics.box.map:.4f}")
    print(f"📊 Precisão: {metrics.box.mp:.4f}")
    print(f"📊 Recall: {metrics.box.mr:.4f}")
    
    print(f"\n📁 Resultados salvos em: {project_root}/runs/val/libras_yolo11n_validation")
    
    return metrics

if __name__ == "__main__":
    try:
        metrics = validate_model()
        print("\n✅ Validação concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante a validação: {str(e)}")
        import traceback
        traceback.print_exc()
