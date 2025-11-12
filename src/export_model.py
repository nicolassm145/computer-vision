"""
Script de Exportação de Modelo
Autor: Nicolas
Data: 2025-11-11

Exporta o modelo treinado para diferentes formatos:
- ONNX (para deployment em produção)
- TensorFlow Lite (para mobile)
- TorchScript (para C++)
"""

from ultralytics import YOLO
from pathlib import Path
import argparse

def export_model(model_path=None, formats=['onnx']):
    """
    Exporta o modelo para diferentes formatos
    
    Args:
        model_path: Caminho para o modelo treinado
        formats: Lista de formatos para exportar
    """
    print("=" * 60)
    print("EXPORTAÇÃO DE MODELO YOLOV11N")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    
    # Se não foi especificado um modelo, usar o melhor modelo do treinamento
    if model_path is None:
        model_path = project_root / "runs" / "train" / "libras_yolo11n" / "weights" / "best.pt"
    
    print(f"\n💾 Modelo: {model_path}")
    print(f"📦 Formatos: {', '.join(formats)}")
    
    # Verificar se o modelo existe
    if not Path(model_path).exists():
        print(f"\n❌ ERRO: Modelo não encontrado!")
        print(f"   Execute train.py primeiro para treinar o modelo.")
        return
    
    # Carregar modelo
    print("\n🔄 Carregando modelo...")
    model = YOLO(str(model_path))
    
    # Exportar para cada formato
    export_dir = project_root / "models" / "exported"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    for fmt in formats:
        print(f"\n📤 Exportando para {fmt.upper()}...")
        try:
            if fmt == 'onnx':
                # ONNX - Melhor para deployment geral
                export_path = model.export(
                    format='onnx',
                    imgsz=640,
                    simplify=True,
                    dynamic=False
                )
                print(f"   ✅ ONNX exportado")
                results['onnx'] = export_path
                
            elif fmt == 'tflite':
                # TensorFlow Lite - Para mobile (Android/iOS)
                export_path = model.export(
                    format='tflite',
                    imgsz=640
                )
                print(f"   ✅ TFLite exportado")
                results['tflite'] = export_path
                
            elif fmt == 'torchscript':
                # TorchScript - Para C++
                export_path = model.export(
                    format='torchscript',
                    imgsz=640
                )
                print(f"   ✅ TorchScript exportado")
                results['torchscript'] = export_path
                
            elif fmt == 'coreml':
                # CoreML - Para iOS
                export_path = model.export(
                    format='coreml',
                    imgsz=640
                )
                print(f"   ✅ CoreML exportado")
                results['coreml'] = export_path
                
            elif fmt == 'openvino':
                # OpenVINO - Para Intel hardware
                export_path = model.export(
                    format='openvino',
                    imgsz=640
                )
                print(f"   ✅ OpenVINO exportado")
                results['openvino'] = export_path
                
            else:
                print(f"   ⚠️  Formato {fmt} não suportado")
                
        except Exception as e:
            print(f"   ❌ Erro ao exportar para {fmt}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ EXPORTAÇÃO CONCLUÍDA")
    print("=" * 60)
    
    if results:
        print("\n📁 Arquivos exportados:")
        for fmt, path in results.items():
            print(f"   {fmt.upper()}: {path}")
    
    print("\n💡 Uso dos formatos exportados:")
    print("   - ONNX: Deployment geral (ONNX Runtime)")
    print("   - TFLite: Apps mobile Android/iOS")
    print("   - TorchScript: Integração C++")
    print("   - CoreML: Apps iOS nativos")
    print("   - OpenVINO: Hardware Intel (CPU/GPU/VPU)")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exportar modelo YOLOv11n')
    parser.add_argument('--model', type=str, help='Caminho para o modelo')
    parser.add_argument('--formats', nargs='+', 
                       default=['onnx'],
                       choices=['onnx', 'tflite', 'torchscript', 'coreml', 'openvino'],
                       help='Formatos para exportar')
    
    args = parser.parse_args()
    
    try:
        export_model(
            model_path=args.model,
            formats=args.formats
        )
        print("\n🎉 Exportação finalizada com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
