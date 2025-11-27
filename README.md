# 🤟 Sistema de Reconhecimento de Libras com YOLOv8

Sistema completo de reconhecimento de sinais de Libras (Língua Brasileira de Sinais) utilizando YOLOv8, com interface gráfica e construção de frases em tempo real.

## 📋 Características

- ✅ **Detecção em tempo real** via webcam
- ✅ **Interface gráfica intuitiva** com Tkinter
- ✅ **Construção automática de frases** com sistema de confirmação
- ✅ **Normalização de sinais** (ex: d1, d2 → D)
- ✅ **Treinamento customizável** do modelo YOLOv8
- ✅ **Teste em imagens estáticas**
- ✅ **Suporte a GPU (CUDA)** para melhor performance
- ✅ **Atalhos de teclado** para controle rápido

## 🚀 Instalação

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

## 📁 Estrutura do Dataset

Organize seu dataset no seguinte formato:

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

### Exemplo de data.yaml
```yaml
path: /caminho/completo/para/dataset
train: train/images
val: valid/images
test: test/images  # opcional

nc: 26  # número de classes
names: ['A', 'B', 'C', 'D', ...]  # lista de classes
```

## 🎯 Uso

### Interface Gráfica (Recomendado)
```bash
python libras_gui.py
```

**Funcionalidades da GUI:**
- 📂 Carregar modelo treinado
- ▶️ Iniciar/parar câmera
- 🖼️ Testar em imagens
- ⎵ Adicionar espaço entre sinais
- ⌫ Apagar último caractere
- 🗑️ Limpar frase completa
- 💾 Salvar frase em arquivo

**Atalhos de Teclado:**
- `ESPAÇO` - Adicionar espaço
- `BACKSPACE` - Apagar último caractere
- `Ctrl+S` - Salvar frase
- `Ctrl+L` ou `Delete` - Limpar frase

### Linha de Comando
```bash
python libras_recognition.py
```

**Menu principal:**
1. Treinar novo modelo
2. Validar modelo treinado
3. Testar em imagem
4. Reconhecimento em tempo real (webcam)
5. Sair

### Controles da Webcam (Modo CLI)
- `q` - Sair
- `s` - Salvar screenshot
- `c` - Limpar frase
- `BACKSPACE` - Apagar último caractere
- `ESPAÇO` - Adicionar espaço
- `f` - Salvar frase em arquivo
- `+/-` - Ajustar tamanho de processamento

## ⚙️ Configurações

### Parâmetros de Confirmação (libras_gui.py)
```python
self.tempo_confirmacao = 8.0        # Segundos para confirmar sinal
self.deteccoes_necessarias = 15     # Número de detecções necessárias
self.confianca_minima = 0.75        # Confiança mínima (0-1)
```

### Otimização de Performance
- **GPU**: Muito mais rápido, recomendado para tempo real
- **CPU**: Funcional mas mais lento
- **imgsz**: Tamanho da imagem (160-640)
  - Menor = mais rápido, menos preciso
  - Maior = mais lento, mais preciso

## 🎓 Treinamento

### Parâmetros Recomendados

**Para começar:**
```python
epochs = 100
batch = 16
model_size = 'n'  # nano (mais rápido)
```

**Para melhor precisão:**
```python
epochs = 200-300
batch = 32
model_size = 's' ou 'm'  # small/medium
```

### Modelos Disponíveis
- `yolov8n.pt` - Nano (mais rápido, menor)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (mais preciso, maior)

## 📊 Métricas

O sistema avalia:
- **mAP50**: Mean Average Precision em IoU=0.5
- **mAP50-95**: mAP em IoU de 0.5 a 0.95
- **Precisão**: Taxa de acertos
- **Recall**: Taxa de detecção

## 📝 Saída de Dados

### Frases Salvas
As frases são salvas em `frases_libras.txt`:
```
[2025-01-15 14:30:22] OLA MUNDO
[2025-01-15 14:32:45] BOM DIA
```

### Resultados de Treinamento
```
runs/detect/libras_yolo/
├── weights/
│   ├── best.pt       # Melhor modelo
│   └── last.pt       # Último checkpoint
├── results.png       # Gráficos de treinamento
└── confusion_matrix.png
```

## 🔧 Solução de Problemas

### Câmera não abre
- Verifique se outra aplicação está usando a câmera
- Tente mudar `cv2.VideoCapture(0)` para `(1)` ou `(2)`

### Erro de memória durante treinamento
- Reduza o `batch_size`
- Use modelo menor (`yolov8n`)
- Reduza `imgsz`

### Detecções muito rápidas/lentas
Ajuste os parâmetros:
```python
self.tempo_confirmacao = 6.0  # Menor = mais rápido
self.deteccoes_necessarias = 10  # Menor = mais rápido
```

### GPU não detectada
```bash
# Instale CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas de melhoria:
- Novos sinais e gestos
- Melhorias na interface
- Otimizações de performance
- Documentação adicional

## 📄 Licença

[Adicione sua licença aqui]

## 👥 Autores

Nícolas de Souza Moreira
Leandro Rocha 

## 🙏 Agradecimentos

- Ultralytics YOLOv8
- Comunidade de Libras
- Contribuidores do projeto

## 📞 Contato

[Adicione informações de contato]

---

**Desenvolvido com ❤️ para acessibilidade e inclusão**