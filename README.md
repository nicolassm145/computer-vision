# Sistema de Reconhecimento de Libras com YOLOv8

Sistema completo de reconhecimento de sinais de Libras (Língua Brasileira de Sinais) utilizando YOLOv8, com interface gráfica e construção de frases em tempo real.

## Características

- ✅ **Detecção em tempo real** via webcam
- ✅ **Interface gráfica intuitiva** com Tkinter
- ✅ **Construção automática de frases** com sistema de confirmação robusto
- ✅ **Normalização de sinais** (ex: d1, d2 → D)
- ✅ **Treinamento customizável** do modelo YOLOv8
- ✅ **Teste em imagens estáticas**
- ✅ **Suporte a GPU (CUDA)** para melhor performance
- ✅ **Atalhos de teclado** para controle rápido

## Como Funciona

O sistema utiliza um pipeline de detecção e confirmação para garantir que apenas sinais intencionais sejam registrados na frase.

1.  **Detecção (YOLOv8)**: O modelo analisa cada frame da webcam e identifica possíveis sinais de mão com uma pontuação de confiança.
2.  **Buffer de Histórico**: As detecções recentes são armazenadas em um buffer temporário.
3.  **Validação Temporal**: Para um sinal ser confirmado, ele precisa:
    *   Ter uma confiança mínima (padrão: 75%).
    *   Aparecer consistentemente nos últimos segundos (padrão: 15 detecções em 2.5s).
4.  **Confirmação**: Se o sinal for estável, ele é adicionado à frase. O sistema aguarda um tempo de "resfriamento" (padrão: 8s) ou uma mudança clara de sinal para evitar repetições acidentais.

## Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd libras-recognition
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. (Opcional) Instale suporte a GPU
Para usar CUDA e acelerar o processamento:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Estrutura do Dataset

Organize seu dataset no seguinte formato para treinamento:

```
dataset/
├── data.yaml          # Arquivo de configuração
├── train/
│   ├── images/       # Imagens de treino
│   └── labels/       # Labels YOLO (.txt)
├── valid/
│   ├── images/       # Imagens de validação
│   └── labels/       # Labels YOLO (.txt)
└── test/ (opcional)
    ├── images/
    └── labels/
```

### Exemplo de `data.yaml`
```yaml
path: /caminho/completo/para/dataset
train: train/images
val: valid/images
test: test/images  # opcional

nc: 26  # número de classes
names: ['A', 'B', 'C', 'D', ...]  # lista de classes
```

## Uso

### Interface Gráfica (Recomendado)
Execute o comando abaixo para abrir a interface principal:
```bash
python libras_gui.py
```

**Funcionalidades da GUI:**
- 📂 **Carregar Modelo**: Selecione seu arquivo `.pt` treinado.
- ▶️ **Iniciar Câmera**: Começa a detecção em tempo real.
- 🖼️ **Testar Imagem**: Valide o modelo em arquivos estáticos.
- **Controles de Texto**: Espaço, Apagar e Limpar.
- 💾 **Salvar**: Exporta a frase atual para `frases_libras.txt`.

**Atalhos de Teclado:**
| Tecla | Ação |
| :--- | :--- |
| `ESPAÇO` | Adicionar espaço |
| `BACKSPACE` | Apagar último caractere |
| `Ctrl+S` | Salvar frase |
| `Ctrl+L` / `Delete` | Limpar frase |

### Linha de Comando (CLI)
Para opções avançadas e treinamento via terminal:
```bash
python libras_recognition.py
```

**Menu principal:**
1. Treinar novo modelo
2. Validar modelo treinado
3. Testar em imagem
4. Reconhecimento em tempo real (webcam)
5. Sair

## Configurações

### Parâmetros de Confirmação (`libras_gui.py`)
Você pode ajustar a sensibilidade do sistema alterando estas variáveis no código:

```python
self.tempo_confirmacao = 8.0        # Segundos para confirmar sinal
self.deteccoes_necessarias = 15     # Número de detecções necessárias
self.confianca_minima = 0.75        # Confiança mínima (0-1)
```

### Otimização de Performance
- **GPU**: Altamente recomendado para uso em tempo real.
- **Tamanho da Imagem (`imgsz`)**:
  - `320-416`: Mais rápido, menos preciso (bom para CPU).
  - `640`: Padrão, bom equilíbrio.
  - `1280`: Alta precisão, muito lento.

## Treinamento

### Parâmetros Recomendados

**Para começar (Rápido):**
```python
epochs = 100
batch = 16
model_size = 'n'  # nano
```

**Para produção (Preciso):**
```python
epochs = 200-300
batch = 32
model_size = 's' ou 'm'  # small/medium
```

### Modelos Disponíveis
- `yolov8n.pt` - Nano (Mais rápido)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (Mais preciso)

## Métricas

O sistema avalia automaticamente:
- **mAP50**: Precisão Média em IoU=0.5.
- **mAP50-95**: Métrica mais rigorosa de precisão.
- **Precisão**: Quantas detecções estavam corretas.
- **Recall**: Quantos objetos reais foram detectados.

## Saída de Dados

### Frases Salvas
As frases são salvas em `frases_libras.txt` com timestamp:
```text
[2025-01-15 14:30:22] OLA MUNDO
[2025-01-15 14:32:45] BOM DIA
```

### Resultados de Treinamento
Os artefatos de treinamento ficam em `runs/detect/`:
- `weights/best.pt`: O melhor modelo obtido.
- `results.png`: Gráficos de perda e métricas.
- `confusion_matrix.png`: Matriz de confusão.

## Solução de Problemas

| Problema | Solução Possível |
| :--- | :--- |
| **Câmera não abre** | Verifique se outro app está usando a câmera. Tente índices 0, 1 ou 2. |
| **Erro de Memória (OOM)** | Reduza o `batch_size` ou use um modelo menor (`nano`). |
| **Detecção Instável** | Aumente `deteccoes_necessarias` ou `confianca_minima`. |
| **GPU não detectada** | Reinstale o PyTorch com suporte a CUDA (veja Instalação). |

---

**Desenvolvido com ❤️ para acessibilidade e inclusão**