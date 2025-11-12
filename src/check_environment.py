"""
Script de Verificação do Ambiente
Autor: Nicolas
Data: 2025-11-11

Verifica se todas as dependências estão instaladas corretamente
e se o ambiente está pronto para treinar e usar o modelo.
"""

import sys
from pathlib import Path

def check_environment():
    """
    Verifica o ambiente e as dependências
    """
    print("=" * 60)
    print("VERIFICAÇÃO DO AMBIENTE")
    print("=" * 60)
    
    all_ok = True
    
    # Verificar versão do Python
    print(f"\n🐍 Python: {sys.version}")
    if sys.version_info < (3, 8):
        print("   ⚠️  Recomendado Python 3.8 ou superior")
        all_ok = False
    else:
        print("   ✅ Versão OK")
    
    # Verificar bibliotecas
    print("\n📦 Verificando bibliotecas...")
    
    libraries = {
        'ultralytics': 'YOLOv11',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'PIL': 'Pillow'
    }
    
    for lib, name in libraries.items():
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'desconhecida')
            print(f"   ✅ {name}: {version}")
        except ImportError:
            print(f"   ❌ {name}: NÃO INSTALADO")
            all_ok = False
    
    # Verificar estrutura de pastas
    print("\n📁 Verificando estrutura de pastas...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        'dataset',
        'dataset/train',
        'dataset/valid',
        'dataset/test',
        'config',
        'src',
        'runs'
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - NÃO ENCONTRADO")
            all_ok = False
    
    # Verificar arquivo de configuração
    print("\n📄 Verificando arquivos de configuração...")
    
    config_file = project_root / "config" / "data.yaml"
    if config_file.exists():
        print(f"   ✅ config/data.yaml")
        
        # Ler e verificar conteúdo
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'train:' in content and 'val:' in content and 'nc: 22' in content:
                print("   ✅ Configuração válida")
            else:
                print("   ⚠️  Configuração pode estar incompleta")
    else:
        print(f"   ❌ config/data.yaml - NÃO ENCONTRADO")
        all_ok = False
    
    # Verificar dataset
    print("\n📊 Verificando dataset...")
    
    train_images = project_root / "dataset" / "train" / "images"
    train_labels = project_root / "dataset" / "train" / "labels"
    
    if train_images.exists() and train_labels.exists():
        num_images = len(list(train_images.glob('*')))
        num_labels = len(list(train_labels.glob('*.txt')))
        print(f"   ✅ Imagens de treino: {num_images}")
        print(f"   ✅ Labels de treino: {num_labels}")
        
        if num_images == 0 or num_labels == 0:
            print("   ⚠️  Dataset parece estar vazio")
            all_ok = False
    else:
        print("   ❌ Diretórios de dataset não encontrados")
        all_ok = False
    
    # Verificar GPU (opcional)
    print("\n🎮 Verificando GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   ✅ GPU disponível: {torch.cuda.get_device_name(0)}")
            print(f"   ℹ️  CUDA version: {torch.version.cuda}")
        else:
            print("   ℹ️  GPU não disponível (treinamento será em CPU)")
    except ImportError:
        print("   ℹ️  PyTorch não instalado (GPU não será usada)")
    
    # Resultado final
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ AMBIENTE PRONTO!")
        print("=" * 60)
        print("\n🚀 Próximos passos:")
        print("   1. Execute: python src/train.py")
        print("   2. Após treinar: python src/validate.py")
        print("   3. Teste com webcam: python src/detect_webcam.py")
    else:
        print("⚠️  PROBLEMAS ENCONTRADOS")
        print("=" * 60)
        print("\n🔧 Ações recomendadas:")
        print("   1. Instale as dependências: pip install -r requirements.txt")
        print("   2. Verifique se o dataset está completo")
        print("   3. Execute este script novamente")
    
    return all_ok

if __name__ == "__main__":
    try:
        check_environment()
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {str(e)}")
        import traceback
        traceback.print_exc()
