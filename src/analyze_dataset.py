"""
Script de Análise do Dataset
Autor: Nicolas
Data: 2025-11-11

Analisa o dataset e mostra estatísticas úteis
"""

from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

def analyze_dataset():
    """
    Analisa o dataset LIBRAS e gera estatísticas
    """
    print("=" * 60)
    print("ANÁLISE DO DATASET LIBRAS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    dataset_root = project_root / "dataset"
    
    # Classes
    classes = ['A', 'B', 'C', 'D1', 'D2', 'E', 'F', 'G', 'I', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    
    print(f"\n📊 Classes: {len(classes)}")
    print(f"   {', '.join(classes)}")
    
    # Analisar cada split
    splits = ['train', 'valid', 'test']
    stats = {}
    
    for split in splits:
        images_dir = dataset_root / split / "images"
        labels_dir = dataset_root / split / "labels"
        
        if not images_dir.exists() or not labels_dir.exists():
            print(f"\n⚠️  {split}: Diretório não encontrado")
            continue
        
        # Contar imagens e labels
        images = list(images_dir.glob('*'))
        labels = list(labels_dir.glob('*.txt'))
        
        num_images = len(images)
        num_labels = len(labels)
        
        # Contar classes
        class_counts = Counter()
        total_objects = 0
        
        for label_file in labels:
            try:
                with open(label_file, 'r') as f:
                    lines = f.readlines()
                    total_objects += len(lines)
                    for line in lines:
                        parts = line.strip().split()
                        if parts:
                            class_id = int(parts[0])
                            if 0 <= class_id < len(classes):
                                class_counts[classes[class_id]] += 1
            except Exception as e:
                print(f"   ⚠️  Erro ao ler {label_file.name}: {e}")
        
        stats[split] = {
            'images': num_images,
            'labels': num_labels,
            'objects': total_objects,
            'class_counts': class_counts
        }
        
        print(f"\n📁 {split.upper()}")
        print(f"   Imagens: {num_images}")
        print(f"   Labels: {num_labels}")
        print(f"   Objetos: {total_objects}")
        print(f"   Média de objetos por imagem: {total_objects/num_images:.2f}" if num_images > 0 else "   N/A")
    
    # Análise de balanceamento
    if 'train' in stats:
        print(f"\n📊 DISTRIBUIÇÃO DE CLASSES (TREINO)")
        print("=" * 60)
        
        class_counts = stats['train']['class_counts']
        total = sum(class_counts.values())
        
        # Ordenar por quantidade
        sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n{'Classe':<10} {'Quantidade':<12} {'Percentual':<12} {'Barra'}")
        print("-" * 60)
        
        for class_name, count in sorted_classes:
            percentage = (count / total * 100) if total > 0 else 0
            bar = '█' * int(percentage / 2)  # Escala: 2% = 1 barra
            print(f"{class_name:<10} {count:<12} {percentage:>5.1f}%       {bar}")
        
        # Verificar balanceamento
        if sorted_classes:
            max_count = sorted_classes[0][1]
            min_count = sorted_classes[-1][1]
            ratio = max_count / min_count if min_count > 0 else float('inf')
            
            print(f"\n📊 Balanceamento:")
            print(f"   Classe com mais exemplos: {sorted_classes[0][0]} ({max_count})")
            print(f"   Classe com menos exemplos: {sorted_classes[-1][0]} ({min_count})")
            print(f"   Razão (max/min): {ratio:.2f}")
            
            if ratio < 2:
                print("   ✅ Dataset bem balanceado!")
            elif ratio < 5:
                print("   ⚠️  Dataset moderadamente desbalanceado")
            else:
                print("   ⚠️  Dataset muito desbalanceado - considere balancear")
    
    # Totais
    print(f"\n📈 TOTAIS")
    print("=" * 60)
    total_images = sum(s['images'] for s in stats.values())
    total_labels = sum(s['labels'] for s in stats.values())
    total_objects = sum(s['objects'] for s in stats.values())
    
    print(f"Total de imagens: {total_images}")
    print(f"Total de labels: {total_labels}")
    print(f"Total de objetos: {total_objects}")
    
    # Gerar gráfico (opcional)
    try:
        if 'train' in stats:
            generate_plot(stats['train']['class_counts'], project_root)
    except Exception as e:
        print(f"\n⚠️  Não foi possível gerar gráfico: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 60)
    
    return stats

def generate_plot(class_counts, project_root):
    """
    Gera gráfico de distribuição de classes
    """
    if not class_counts:
        return
    
    # Ordenar por nome de classe
    sorted_items = sorted(class_counts.items())
    classes = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    
    # Criar gráfico
    plt.figure(figsize=(14, 6))
    bars = plt.bar(classes, counts, color='steelblue', edgecolor='black', alpha=0.7)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9)
    
    plt.xlabel('Classes (Letras LIBRAS)', fontsize=12, fontweight='bold')
    plt.ylabel('Quantidade de Exemplos', fontsize=12, fontweight='bold')
    plt.title('Distribuição de Classes no Dataset de Treino', fontsize=14, fontweight='bold')
    plt.xticks(rotation=0, fontsize=10)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Salvar
    output_path = project_root / 'dataset_distribution.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Gráfico salvo em: {output_path}")
    plt.close()

if __name__ == "__main__":
    try:
        analyze_dataset()
        print("\n💡 Dica: Use estas informações para entender seu dataset")
        print("   e identificar classes que podem precisar de mais exemplos.")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
