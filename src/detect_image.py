"""
Script de Detecção em Imagens
Autor: Nicolas
Data: 2025-11-11

Este script permite testar o modelo treinado em imagens individuais
ou em um diretório de imagens.
"""

from ultralytics import YOLO
import cv2
from pathlib import Path
import argparse

def detect_image(model_path=None, image_path=None, confidence=0.5, save=True):
    """
    Detecta letras LIBRAS em uma imagem ou diretório de imagens
    
    Args:
        model_path: Caminho para o modelo treinado
        image_path: Caminho para imagem ou diretório
        confidence: Threshold de confiança
        save: Se deve salvar as imagens com detecções
    """
    print("=" * 60)
    print("DETECÇÃO EM IMAGENS - LIBRAS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    
    # Definir caminhos padrão
    if model_path is None:
        model_path = project_root / "runs" / "train" / "libras_yolo11n" / "weights" / "best.pt"
    
    if image_path is None:
        # Usar imagens de teste por padrão
        image_path = project_root / "dataset" / "test" / "images"
    
    print(f"\n💾 Modelo: {model_path}")
    print(f"📁 Imagens: {image_path}")
    print(f"🎯 Confiança: {confidence}")
    
    # Verificar se o modelo existe
    if not Path(model_path).exists():
        print(f"\n❌ ERRO: Modelo não encontrado em {model_path}")
        return
    
    # Carregar modelo
    print("\n🔄 Carregando modelo...")
    model = YOLO(str(model_path))
    
    # Fazer predições
    print("\n🔍 Processando imagens...")
    results = model.predict(
        source=str(image_path),
        conf=confidence,
        save=save,
        project=str(project_root / 'runs' / 'detect'),
        name='libras_predictions',
        exist_ok=True,
        show_labels=True,
        show_conf=True,
        line_width=2
    )
    
    print("\n" + "=" * 60)
    print("✅ DETECÇÃO CONCLUÍDA")
    print("=" * 60)
    print(f"\n📊 Total de imagens processadas: {len(results)}")
    
    if save:
        save_path = project_root / 'runs' / 'detect' / 'libras_predictions'
        print(f"💾 Resultados salvos em: {save_path}")
    
    # Estatísticas
    total_detections = sum(len(r.boxes) for r in results)
    print(f"🎯 Total de detecções: {total_detections}")
    
    if total_detections > 0:
        print("\n📋 Classes detectadas:")
        class_counts = {}
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls.cpu().numpy())
                class_name = model.names[class_id]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        for class_name, count in sorted(class_counts.items()):
            print(f"   {class_name}: {count}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detectar letras LIBRAS em imagens')
    parser.add_argument('--image', type=str, help='Caminho para imagem ou diretório')
    parser.add_argument('--model', type=str, help='Caminho para o modelo')
    parser.add_argument('--conf', type=float, default=0.5, help='Confiança mínima (0-1)')
    parser.add_argument('--no-save', action='store_true', help='Não salvar resultados')
    
    args = parser.parse_args()
    
    try:
        detect_image(
            model_path=args.model,
            image_path=args.image,
            confidence=args.conf,
            save=not args.no_save
        )
        print("\n🎉 Processo finalizado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
