# 🤟 Detector de LIBRAS com YOLOv11n

Sistema de detecção de letras do alfabeto em LIBRAS (Linguagem Brasileira de Sinais) usando YOLOv11n.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Resultados](#resultados)

## 🎯 Sobre o Projeto

Este projeto treina um modelo YOLOv11n para detectar e classificar 22 letras do alfabeto em LIBRAS a partir de imagens de mãos. O modelo pode ser usado em tempo real com webcam para reconhecimento de sinais.

### Classes Detectadas

A, B, C, D1, D2, E, F, G, I, K, L, M, N, O, P, Q, R, S, T, U, V, W (22 classes)

## 📁 Estrutura do Projeto

```
computer-vision/
├── venv/                      # Ambiente virtual Python
├── dataset/                   # Dataset com imagens e labels
│   ├── train/                 # Conjunto de treinamento
│   ├── valid/                 # Conjunto de validação
│   ├── test/                  # Conjunto de teste
│   └── data.yaml             # Configuração original do dataset
├── config/                    # Arquivos de configuração
│   └── data.yaml             # Configuração para treinamento
├── src/                       # Código fonte
│   ├── train.py              # Script de treinamento
│   ├── validate.py           # Script de validação
│   ├── detect_webcam.py      # Detecção em tempo real
│   └── detect_image.py       # Detecção em imagens
├── runs/                      # Resultados dos experimentos
│   ├── train/                # Resultados do treinamento
│   ├── val/                  # Resultados da validação
│   └── detect/               # Resultados das detecções
├── models/                    # Modelos salvos
└── README.md                 # Este arquivo
```

## 🔧 Requisitos

- Python 3.8+
- Webcam (para detecção em tempo real)
- GPU NVIDIA (opcional, mas recomendado para treinamento mais rápido)

### Bibliotecas Python

- ultralytics (YOLOv11)
- opencv-python
- numpy
- matplotlib
- pillow

## 🚀 Instalação

### 1. Criar e ativar ambiente virtual

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```powershell
pip install ultralytics opencv-python numpy matplotlib pillow
```

## 💻 Como Usar

### 1. Treinar o Modelo

Execute o script de treinamento:

```powershell
python src/train.py
```

**Parâmetros de treinamento (editáveis no código):**

- `epochs`: 100 (número de épocas)
- `batch`: 16 (tamanho do batch)
- `imgsz`: 640 (tamanho da imagem)
- `device`: 'cpu' (use 0 para GPU)

**O que acontece:**

- Download automático do modelo YOLOv11n pré-treinado
- Treinamento com early stopping (patience=20)
- Salvamento de checkpoints e gráficos
- Resultados em `runs/train/libras_yolo11n/`

**Tempo estimado:**

- CPU: 2-4 horas
- GPU: 30-60 minutos

### 2. Validar o Modelo

Após o treinamento, valide o modelo:

```powershell
python src/validate.py
```

**Métricas geradas:**

- mAP50 (Mean Average Precision @ IoU 0.5)
- mAP50-95 (mAP em diferentes IoU thresholds)
- Precisão e Recall
- Confusion matrix
- Gráficos de desempenho

### 3. Detecção em Tempo Real (Webcam)

Use a webcam para detectar letras LIBRAS em tempo real:

```powershell
python src/detect_webcam.py
```

**Controles:**

- `Q`: Sair
- `S`: Salvar frame atual
- `+`: Aumentar threshold de confiança
- `-`: Diminuir threshold de confiança

**Dicas para melhor detecção:**

- Use boa iluminação
- Mantenha a mão centralizada
- Fundo neutro ajuda
- Distância de ~50cm da câmera

### 4. Detecção em Imagens

Testar o modelo em imagens específicas:

```powershell
# Processar todas as imagens de teste
python src/detect_image.py

# Processar uma imagem específica
python src/detect_image.py --image "caminho/para/imagem.jpg"

# Ajustar confiança
python src/detect_image.py --conf 0.7

# Ver todas as opções
python src/detect_image.py --help
```

## 📊 Resultados

Após o treinamento, você encontrará:

### Em `runs/train/libras_yolo11n/`:

- `weights/best.pt` - Melhor modelo
- `weights/last.pt` - Último checkpoint
- `results.png` - Gráficos de métricas
- `confusion_matrix.png` - Matriz de confusão
- `F1_curve.png`, `PR_curve.png` - Curvas de desempenho

### Em `runs/val/`:

- Resultados da validação no conjunto de teste
- Métricas detalhadas por classe

### Em `runs/detect/`:

- Imagens com detecções
- Predições salvas

## 🎓 Interpretando os Resultados

### mAP (Mean Average Precision)

- **mAP50**: Precisão média com IoU > 0.5
  - > 0.9: Excelente
  - 0.7-0.9: Bom
  - < 0.7: Precisa melhorar

### Precisão vs Recall

- **Precisão alta**: Poucas detecções falsas
- **Recall alto**: Detecta a maioria dos objetos
- Ideal: Ambos altos

### Confusion Matrix

- Diagonal: Classificações corretas
- Fora da diagonal: Confusões entre classes

## 🔍 Troubleshooting

### Erro: "Modelo não encontrado"

→ Execute `train.py` primeiro para treinar o modelo

### Erro: "Não foi possível abrir a webcam"

→ Verifique se a webcam está conectada e funcionando
→ Teste com outros aplicativos (Camera, etc.)

### Treinamento muito lento

→ Use GPU: mude `device='cpu'` para `device=0` no train.py
→ Reduza `batch` para 8 ou 4
→ Reduza `epochs` para testes rápidos

### Baixa precisão

→ Aumente o número de `epochs`
→ Ajuste `confidence` threshold na detecção
→ Verifique se o dataset está balanceado
→ Considere data augmentation

## 🎯 Próximos Passos

1. **Otimizar hiperparâmetros**: Ajuste learning rate, batch size, etc.
2. **Data augmentation**: Adicione mais variações ao dataset
3. **Exportar modelo**: Converta para ONNX, TensorFlow Lite para mobile
4. **Interface gráfica**: Crie uma GUI com Tkinter ou PyQt
5. **Deploy**: Disponibilize como aplicação web com Flask/FastAPI

## 📚 Referências

- [Ultralytics YOLOv11 Documentation](https://docs.ultralytics.com/)
- [YOLO Paper](https://arxiv.org/abs/2304.00501)
- [LIBRAS - Língua Brasileira de Sinais](https://www.gov.br/governodigital/pt-br/acessibilidade-digital/libras)

## 📝 Licença

Dataset: CC BY 4.0 (Roboflow)
Código: Uso livre para fins educacionais

---