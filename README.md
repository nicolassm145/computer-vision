# 🤟 Sistema de Detecção de Linguagem de Sinais LIBRAS

## 📝 Descrição

Este projeto implementa um sistema **completo de detecção em tempo real** de linguagem de sinais brasileira (LIBRAS) usando **YOLOv11n** treinado especificamente para identificar 22 letras do alfabeto através da webcam.

### ✨ Principais Características

- **🎯 Modelo**: YOLOv11n otimizado para detecção de gestos LIBRAS
- **⚡ Performance**: Detecção em tempo real via webcam (15-60+ FPS)
- **🔤 Classes**: 22 letras do alfabeto LIBRAS (A-W, exceto H, J, X, Y, Z)

## 🚀 Como Usar 

### Usar o Detector
1. **Posicione** sua mão em frente à webcam
2. **Faça** gestos das letras do alfabeto LIBRAS
3. **Veja** a detecção em tempo real na tela
4. **Pressione** 'q' ou ESC para sair


#### 1. Clone ou baixe o projeto
```bash
cd computer-vision
```

#### 2. Crie ambiente virtual (recomendado)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

#### 3. Instale dependências
```bash
pip install -r requirements.txt
```

#### 4. Execute o sistema
```bash
python detector_libras.py
```

## � Estrutura do Projeto

```
computer-vision/
├── 📂 dataset/                    # Dataset LIBRAS original
│   ├── 📄 data.yaml              # Configuração das classes
│   ├── 📂 train/                 # Imagens de treinamento
│   ├── 📂 valid/                 # Imagens de validação
│   └── 📂 test/                  # Imagens de teste
├── 📄 detector_libras.py         # 🎯 SCRIPT PRINCIPAL (usar este!)
├── 📄 train_model.py            # Script de treinamento
├── 📄 sign_language_detector.py # Detector avançado
├── 📄 export_model.py           # Exportação de modelos
├── 📄 requirements.txt          # Dependências Python
└── 📄 README.md                # Este arquivo
```

## 🎨 Interface do Usuário

Durante a execução, você verá:

### 📹 Janela Principal
- **Bounding Boxes**: Retângulos coloridos ao redor das mãos
- **Labels**: Nome da letra + confiança da detecção
- **Cores**: Verde (alta confiança), Amarelo (média), Laranja (baixa)

### 📊 Informações na Tela
- **FPS**: Frames por segundo em tempo real
- **Tempo**: Latência de inferência em ms
- **Detecções**: Número de letras detectadas

### 🎯 Destaque das Letras
- **Parte Inferior**: Letras detectadas em destaque amarelo
- **Formato**: "LETRAS: A | B | C"

### ⌨️ Controles
- **'q'**: Sair do programa
- **ESC**: Sair do programa

## � Classes Detectadas

| ID | Letra | ID | Letra | ID | Letra | ID | Letra |
|----|-------|----| ------|----| ------|----| ------|
| 0  | A     | 6  | F     | 12 | N     | 18 | T     |
| 1  | B     | 7  | G     | 13 | O     | 19 | U     |
| 2  | C     | 8  | I     | 14 | P     | 20 | V     |
| 3  | D1    | 9  | K     | 15 | Q     | 21 | W     |
| 4  | D2    | 10 | L     | 16 | R     |    |       |
| 5  | E     | 11 | M     | 17 | S     |    |       |

**Nota**: D1 e D2 são variações da letra D em LIBRAS.

## ⚙️ Configurações Avançadas

### Ajustar Sensibilidade
No arquivo `detector_libras.py`, linha ~25:
```python
detector = LibrasDetector(model_path, conf_threshold=0.5)
```
- **0.3**: Mais sensível (mais detecções, menos precisas)
- **0.7**: Menos sensível (menos detecções, mais precisas)

### Modificar Resolução da Webcam
Linhas ~120-121:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Largura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Altura
```

## � Treinamento Personalizado

### Para treinar com seus próprios dados:

#### 1. Preparar Dataset
- Organize imagens em `train/`, `valid/`, `test/`
- Crie labels em formato YOLO (.txt)
- Atualize `data.yaml` com suas classes

#### 2. Treinar Modelo
```bash
python train_model.py
```

#### 3. Usar Novo Modelo
O modelo treinado será salvo como `best.pt` e usado automaticamente.

## � Solução de Problemas

### ❌ "Modelo não encontrado"
**Solução**: Execute `python train_model.py` primeiro

### ❌ "Webcam não encontrada"
**Soluções**:
- Verifique se a webcam está conectada
- Teste com outras aplicações (Skype, Teams)
- Mude o índice da câmera: `cv2.VideoCapture(1)`


### ❌ Detecções incorretas
**Soluções**:
- Melhore iluminação
- Aumente `conf_threshold` para 0.7
- Faça gestos mais claros

### ❌ "Import Error"
**Solução**: Reinstale dependências
```bash
pip install --upgrade ultralytics opencv-python numpy
```

## � Como Funciona (Explicação Técnica)

### 🧠 Arquitetura YOLOv11n
1. **Backbone**: CSPDarknet otimizado para eficiência
2. **Neck**: Feature Pyramid Network (FPN) para multi-escala
3. **Head**: Detecção de objetos com classificação simultânea

### 🔄 Pipeline de Processamento
1. **Captura**: Frame da webcam (BGR, 1280x720)
2. **Pré-processamento**: Resize para 640x640, normalização
3. **Inferência**: Modelo produz 8400 predições por imagem
4. **Pós-processamento**: NMS, filtragem por confiança
5. **Visualização**: Desenho de bounding boxes e labels

### 📊 Formato das Detecções
```python
detection = {
    'letter': 'A',           # Letra detectada
    'confidence': 0.85,      # Confiança (0-1)
    'bbox': (x1, y1, x2, y2) # Coordenadas da caixa
}
```

### ⚡ Otimizações Implementadas
- **Inferência eficiente**: Modelo compacto (2.6M parâmetros)
- **Pré-processamento otimizado**: OpenCV acelerado
- **NMS otimizada**: Remoção de detecções duplicadas
- **Visualização rápida**: Desenho direto no frame

## 📚 Dataset e Treinamento

### 📂 Dataset LIBRAS
- **Fonte**: Elaine Silva - Alfabeto em LIBRAS
- **Licença**: CC BY 4.0
- **Imagens**: ~1000 imagens anotadas
- **Divisão**: 70% treino, 20% validação, 10% teste

### 🎯 Configurações de Treinamento
```python
# Parâmetros utilizados
epochs = 100           # Número de épocas
batch_size = 16        # Tamanho do batch
img_size = 640         # Resolução de entrada
patience = 20          # Early stopping
device = 'cpu'         # CPU/CUDA
```
