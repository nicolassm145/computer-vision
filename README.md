# 🤟 Sistema de Detecção de Linguagem de Sinais LIBRAS

## 📝 Descrição

Este projeto implementa um sistema **completo de detecção em tempo real** de linguagem de sinais brasileira (LIBRAS) usando **YOLOv11n** treinado especificamente para identificar 22 letras do alfabeto através da webcam.

### ✨ Principais Características

- **🎯 Modelo**: YOLOv11n otimizado para detecção de gestos LIBRAS
- **⚡ Performance**: Detecção em tempo real via webcam (15-60+ FPS)
- **🔤 Classes**: 22 letras do alfabeto LIBRAS (A-W, exceto H, J, X, Y, Z)
- **📝 Construtor de Frases**: Sistema inteligente que captura letras automaticamente e monta textos completos

## 🚀 Como Usar 

### Modo 1: Construtor de Frases (Recomendado) 📝

O sistema agora detecta letras automaticamente e monta frases completas!

```bash
python detector_libras.py
```

**Funcionalidades:**
- ✅ Detecção automática com confirmação por estabilidade
- ✅ Construção de frases letra por letra
- ✅ Salvamento em arquivo de texto
- ✅ Controles para edição (espaço, backspace, limpar)

**Controles:**
- `ESPAÇO` - Adicionar espaço
- `BACKSPACE` - Apagar última letra
- `C` - Limpar frase
- `S` - Salvar em arquivo
- `Q/ESC` - Sair

📖 [Documentação completa do Construtor de Frases](CONSTRUTOR_FRASES.md)

### Modo 2: Detector Avançado

Para uso com modelos ONNX ou configurações customizadas:

```bash
python sign_language_detector.py
```

---

### Instalação

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

## 📁 Estrutura do Projeto

```
computer-vision/
├── 📂 dataset/                    # Dataset LIBRAS original
│   ├── 📄 data.yaml              # Configuração das classes
│   ├── 📂 train/                 # Imagens de treinamento
│   ├── 📂 valid/                 # Imagens de validação
│   └── 📂 test/                  # Imagens de teste
├── 📄 detector_libras.py         # 🎯 CONSTRUTOR DE FRASES (usar este!)
├── 📄 sign_language_detector.py # Detector avançado (ONNX/PyTorch)
├── 📄 train_model.py            # Script de treinamento
├── 📄 export_model.py           # Exportação de modelos
├── 📄 requirements.txt          # Dependências Python
├── 📄 CONSTRUTOR_FRASES.md      # 📖 Documentação do construtor
└── 📄 README.md                # Este arquivo
```

## 🎨 Construtor de Frases - Interface

O modo **Construtor de Frases** oferece uma interface completa para criar textos:

### 📹 Elementos da Interface

**Topo da Tela:**
- **FPS**: Desempenho em tempo real
- **Progresso de Captura**: "Capturando: A [73%]" mostra letra sendo detectada
- **Flash Verde**: Confirmação visual quando letra é adicionada (✓ A)

**Centro:**
- **Vídeo ao vivo** com bounding boxes coloridos
- **Verde**: Alta confiança (>80%)
- **Amarelo**: Média confiança (60-80%)
- **Laranja**: Baixa confiança (<60%)

**Rodapé:**
- **Área da Frase**: Mostra o texto sendo construído em tempo real
- **Contador**: Quantidade de caracteres digitados
- **Controles**: Lista de atalhos sempre visível

### 🎯 Como Funciona a Detecção Automática

1. **Mantenha o gesto estável** por ~1 segundo
2. **Observe o progresso** no canto superior direito (0% → 100%)
3. **Aguarde o flash verde** de confirmação
4. **Letra é adicionada** automaticamente à frase
5. **Cooldown de 1.5s** antes da próxima captura

### ⌨️ Controles do Teclado

| Tecla | Função |
|-------|--------|
| **ESPAÇO** | Adicionar espaço entre palavras |
| **BACKSPACE** | Apagar último caractere |
| **C** | Limpar frase inteira |
| **S** | Salvar frase em arquivo .txt |
| **Q** ou **ESC** | Sair do programa |

### 💾 Salvamento de Frases

Ao pressionar **S**, o sistema:
- Cria arquivo com timestamp: `frase_libras_YYYYMMDD_HHMMSS.txt`
- Mostra confirmação visual na tela
- Exibe caminho do arquivo no console

**Exemplo:**
```
✓ Frase salva em: frase_libras_20251112_143025.txt
   Conteúdo: BOA TARDE
```

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

## ⚙️ Configurações e Personalização

### Ajustar Velocidade de Captura

No arquivo `detector_libras.py`, você pode modificar a sensibilidade:

**Captura Mais Rápida (menos precisa):**
```python
phrase_builder = PhraseBuilder(
    stability_frames=10,      # Padrão: 15
    min_confidence=0.6        # Padrão: 0.7
)
```

**Captura Mais Precisa (mais lenta):**
```python
phrase_builder = PhraseBuilder(
    stability_frames=25,      # Padrão: 15
    min_confidence=0.8        # Padrão: 0.7
)
```

### Modificar Resolução da Webcam

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Largura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Altura
```

### Parâmetros do Detector

```python
detector = LibrasDetector(model_path, conf_threshold=0.6)
```
- **0.5**: Mais sensível (mais detecções)
- **0.7**: Balanceado (padrão)
- **0.8**: Mais seletivo (apenas gestos muito claros)

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

## 🆘 Solução de Problemas

### ❌ "Modelo não encontrado"
**Solução**: Execute `python train_model.py` primeiro para treinar o modelo

### ❌ "Webcam não encontrada"
**Soluções**:
- Verifique se a webcam está conectada
- Teste com outras aplicações (Skype, Teams)
- Mude o índice da câmera: `cv2.VideoCapture(1)` ou `cv2.VideoCapture(2)`

### ❌ "Letra não é confirmada" (Construtor de Frases)
**Soluções**:
- Mantenha o gesto mais tempo (>1 segundo)
- Melhore a iluminação do ambiente
- Reduza `min_confidence` para 0.6
- Use fundo contrastante com a pele

### ❌ "Letra errada é capturada"
**Soluções**:
- Pressione **BACKSPACE** para corrigir
- Aumente `min_confidence` para 0.8
- Refaça o gesto de forma mais clara
- Aguarde o progresso chegar a 100%

### ❌ "Captura muito lenta"
**Soluções**:
- Reduza `stability_frames` para 10
- Reduza `cooldown_time` para 1.0 segundo
- Use gestos bem definidos

### ❌ "Letras duplicadas"
**Soluções**:
- Aumente `cooldown_time` para 2.0 segundos
- Mova a mão para fora do quadro entre letras
- Aumente `stability_frames` para 20

### ❌ "Import Error"
**Solução**: Reinstale as dependências
```bash
pip install --upgrade ultralytics opencv-python numpy torch torchvision
```

## 💡 Como Funciona (Explicação Técnica)

### 🧠 Arquitetura do Sistema

**Modelo YOLOv11n:**
- **Backbone**: CSPDarknet otimizado para eficiência
- **Neck**: Feature Pyramid Network (FPN) para detecção multi-escala
- **Head**: Detecção de objetos com classificação simultânea
- **Parâmetros**: 2.6M (modelo compacto e rápido)

**Construtor de Frases (Sistema de Confirmação):**
1. Mantém histórico dos últimos 15 frames
2. Aplica votação por maioria (letra que aparece em ≥80% dos frames)
3. Confirma letra automaticamente quando estável
4. Aplica cooldown de 1.5s para evitar duplicação

### 🔄 Pipeline de Processamento

```
Webcam → Captura Frame → Espelhamento → Detecção YOLO
    ↓
Filtragem por Confiança → Votação por Estabilidade
    ↓
Confirmação Automática → Adicionar à Frase → Flash Verde
    ↓
Cooldown 1.5s → Pronto para próxima letra
```

### 📊 Formato das Detecções

```python
detection = {
    'letter': 'A',           # Letra detectada
    'confidence': 0.85,      # Confiança (0-1)
    'bbox': (x1, y1, x2, y2) # Coordenadas da caixa
}
```

### ⚡ Performance

- **FPS esperado**: 15-25 em CPU comum, 30-60 com GPU
- **Latência de inferência**: 40-70ms por frame
- **Tempo de confirmação**: ~1 segundo por letra
- **Tempo total por letra**: ~2.5 segundos (inclui cooldown)

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
