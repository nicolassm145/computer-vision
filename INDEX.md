# 📚 ÍNDICE COMPLETO DO PROJETO

## 🎯 Comece Aqui

**Novo no projeto? Leia nesta ordem:**

1. 🚀 **START_HERE.md** ← Você está pronto! Comece aqui
2. 📖 **QUICK_START.md** ← Guia rápido (5 minutos)
3. 🇧🇷 **GUIA_PT.md** ← Guia completo em português
4. 📘 **README.md** ← Documentação técnica detalhada
5. 📊 **SUMMARY.md** ← Resumo técnico do projeto

---

## 📂 ESTRUTURA COMPLETA

### 📄 Documentação (5 arquivos)

```
├── START_HERE.md           ← COMECE AQUI! Status e próximos passos
├── QUICK_START.md          ← Guia rápido de comandos
├── GUIA_PT.md             ← Explicação detalhada em português
├── README.md               ← Documentação técnica completa
└── SUMMARY.md              ← Resumo executivo do projeto
```

### 💻 Scripts Python (8 arquivos)
```
src/
├── check_environment.py       ← Verificar se tudo está OK
├── analyze_dataset.py         ← Estatísticas do dataset
├── train.py                   ← PRINCIPAL: Treinar o modelo
├── validate.py                ← Validar modelo treinado
├── detect_webcam.py           ← Detecção em tempo real (webcam)
├── detect_webcam_phrases.py   ← ⭐ NOVO: Formar frases automaticamente!
├── detect_image.py            ← Detecção em imagens/fotos
└── export_model.py            ← Exportar para outros formatos
```

```
src/
├── check_environment.py    ← Verificar se tudo está OK
├── analyze_dataset.py      ← Estatísticas do dataset
├── train.py               ← PRINCIPAL: Treinar o modelo
├── validate.py            ← Validar modelo treinado
├── detect_webcam.py       ← Detecção em tempo real (webcam)
├── detect_image.py        ← Detecção em imagens/fotos
└── export_model.py        ← Exportar para outros formatos
```

### ⚙️ Configuração (3 arquivos)

```
├── config/data.yaml        ← Configuração do dataset YOLO
├── requirements.txt        ← Dependências Python
└── .gitignore             ← Arquivos ignorados pelo Git
```

### 🚀 Executáveis (1 arquivo)

```
└── run.bat                ← Menu interativo Windows
```

---

## 📚 GUIA DE USO POR SITUAÇÃO

### 🆕 Primeira Vez Usando o Projeto

1. Leia: `START_HERE.md`
2. Execute: `python src/check_environment.py`
3. Execute: `python src/analyze_dataset.py`
4. Leia: `QUICK_START.md`

### 🚀 Quero Começar Rapidamente

1. Leia: `QUICK_START.md` (5 min)
2. Execute: `python src/train.py`
3. Aguarde 2-4 horas
4. Execute: `python src/detect_webcam.py`

### 📖 Quero Entender Tudo (Recomendado)

1. Leia: `START_HERE.md`
2. Leia: `GUIA_PT.md` (explicação completa)
3. Leia: `README.md` (documentação técnica)
4. Execute os scripts na ordem

### 🔧 Tenho um Problema

1. Execute: `python src/check_environment.py`
2. Leia seção "Troubleshooting" em `README.md`
3. Leia seção "Problemas Comuns" em `GUIA_PT.md`

### 📊 Quero Ver Estatísticas do Dataset

1. Execute: `python src/analyze_dataset.py`
2. Abra: `dataset_distribution.png`

### 🎯 Quero Treinar o Modelo

1. Leia: "Treinamento" em `GUIA_PT.md`
2. Execute: `python src/train.py`
3. Aguarde conclusão
4. Verifique resultados em `runs/train/`

### 📹 Quero Usar com Webcam

1. Certifique-se que treinou o modelo
2. Execute: `python src/detect_webcam.py`
3. Leia controles em `QUICK_START.md`

### 📸 Quero Testar em Fotos

1. Execute: `python src/detect_image.py`
2. Ou: `python src/detect_image.py --image foto.jpg`
3. Resultados em `runs/detect/`

### 📱 Quero Exportar para Mobile

1. Execute: `python src/export_model.py --formats tflite`
2. Modelo exportado em `models/exported/`

---

## 📄 DESCRIÇÃO DETALHADA DOS ARQUIVOS

### 📚 Documentação

#### START_HERE.md

- **O que é:** Ponto de partida do projeto
- **Quando usar:** Primeira coisa a ler
- **Conteúdo:** Status, checklist, próximos passos
- **Tempo de leitura:** 3 minutos

#### QUICK_START.md

- **O que é:** Guia de comandos rápidos
- **Quando usar:** Referência rápida
- **Conteúdo:** Comandos essenciais, troubleshooting
- **Tempo de leitura:** 5 minutos

#### GUIA_PT.md

- **O que é:** Tutorial completo em português
- **Quando usar:** Quer entender tudo em detalhes
- **Conteúdo:** Explicação de cada script, fluxo, dicas
- **Tempo de leitura:** 15-20 minutos

#### README.md

- **O que é:** Documentação técnica oficial
- **Quando usar:** Referência técnica, parâmetros
- **Conteúdo:** API, configurações, métricas
- **Tempo de leitura:** 10-15 minutos

#### SUMMARY.md

- **O que é:** Resumo executivo técnico
- **Quando usar:** Visão geral rápida do projeto
- **Conteúdo:** Estrutura, configurações, métricas
- **Tempo de leitura:** 5 minutos

---

### 💻 Scripts Python

#### check_environment.py

```python
# O que faz
Verifica instalação de bibliotecas, dataset, estrutura de pastas

# Quando usar
- Primeira execução
- Após problemas
- Antes de treinar

# Como usar
python src/check_environment.py

# Tempo de execução
5-10 segundos
```

#### analyze_dataset.py

```python
# O que faz
Analisa distribuição de classes, balanceamento, estatísticas

# Quando usar
- Antes de treinar
- Para entender o dataset
- Identificar classes desbalanceadas

# Como usar
python src/analyze_dataset.py

# Tempo de execução
10-30 segundos

# Saída
- Estatísticas no terminal
- Gráfico: dataset_distribution.png
```

#### train.py ⭐ PRINCIPAL

```python
# O que faz
Treina o modelo YOLOv11n com seus dados

# Quando usar
- Após verificar ambiente
- Primeira vez: teste com 10 epochs
- Produção: 100+ epochs

# Como usar
python src/train.py

# Tempo de execução
CPU: 2-4 horas (100 epochs)
GPU: 30-60 minutos (100 epochs)

# Saída
runs/train/libras_yolo11n/
├── weights/best.pt         ← Modelo principal
├── results.png            ← Gráficos
└── confusion_matrix.png   ← Matriz de confusão

# Parâmetros editáveis
epochs=100      # Número de épocas
batch=16        # Tamanho do batch
imgsz=640       # Tamanho da imagem
device='cpu'    # 'cpu' ou 0 para GPU
```

#### validate.py

```python
# O que faz
Valida o modelo no conjunto de teste

# Quando usar
- Após treinar
- Para avaliar qualidade
- Comparar diferentes modelos

# Como usar
python src/validate.py

# Tempo de execução
5-10 minutos

# Métricas geradas
- mAP50 (precisão média)
- mAP50-95
- Precisão por classe
- Recall por classe
```

#### detect_webcam.py ⭐ DEMO

```python
# O que faz
Detecção em tempo real via webcam

# Quando usar
- Após treinar e validar
- Demo do sistema
- Teste prático

# Como usar
python src/detect_webcam.py

# Controles
Q  - Sair
S  - Salvar frame
+  - Aumentar confiança
-  - Diminuir confiança

# Requisitos
- Modelo treinado
- Webcam funcionando
- Boa iluminação
```

#### detect_image.py

```python
# O que faz
Detecta letras em imagens/fotos

# Quando usar
- Testar em fotos específicas
- Processar lote de imagens
- Avaliar detecções

# Como usar
# Todas as imagens de teste
python src/detect_image.py

# Imagem específica
python src/detect_image.py --image foto.jpg

# Ajustar confiança
python src/detect_image.py --conf 0.7

# Não salvar resultados
python src/detect_image.py --no-save

# Saída
runs/detect/libras_predictions/
└── Imagens com detecções desenhadas
```

#### export_model.py

```python
# O que faz
Exporta modelo para outros formatos

# Quando usar
- Deploy em produção
- Apps mobile
- Otimização de performance

# Como usar
# ONNX (universal)
python src/export_model.py --formats onnx

# TensorFlow Lite (mobile)
python src/export_model.py --formats tflite

# Múltiplos formatos
python src/export_model.py --formats onnx tflite torchscript

# Formatos disponíveis
- onnx        # Universal, deployment geral
- tflite      # Android/iOS
- torchscript # C++, PyTorch
- coreml      # iOS nativo
- openvino    # Intel hardware

# Saída
models/exported/
└── Modelos nos formatos escolhidos
```

---

### ⚙️ Configuração

#### config/data.yaml

```yaml
# O que é
Arquivo de configuração do dataset para YOLO

# Conteúdo
- Caminhos para train/val/test
- Número de classes (22)
- Nomes das classes (A, B, C, ...)

# Quando editar
- Mudar caminhos do dataset
- Adicionar/remover classes
- Trocar dataset
```

#### requirements.txt

```txt
# O que é
Lista de dependências Python

# Quando usar
pip install -r requirements.txt

# Conteúdo
ultralytics    # YOLOv11
opencv-python  # Processamento de imagem
numpy         # Computação científica
matplotlib    # Visualização
pillow        # Manipulação de imagem
```

#### .gitignore

```
# O que é
Arquivos ignorados pelo Git

# Conteúdo
- venv/
- __pycache__/
- runs/
- *.pt (modelos)
- Outputs (imagens, vídeos)
```

---

### 🚀 Executáveis

#### run.bat

```batch
# O que é
Menu interativo para Windows

# Como usar
Duplo clique em run.bat
ou
No terminal: run.bat

# Funcionalidades
1. Verificar ambiente
2. Analisar dataset
3. Treinar modelo
4. Validar modelo
5. Usar webcam
6. Detectar em imagens
7. Exportar modelo
8. Sair
```

---

## 🎯 FLUXO DE TRABALHO RECOMENDADO

```
FASE 1: PREPARAÇÃO (5-10 minutos)
├── 1. Ler START_HERE.md
├── 2. Ler QUICK_START.md
├── 3. python src/check_environment.py
└── 4. python src/analyze_dataset.py

FASE 2: TREINAMENTO (2-4 horas)
├── 1. Ler seção "Treinamento" em GUIA_PT.md
├── 2. python src/train.py
├── 3. Aguardar conclusão
└── 4. Verificar runs/train/libras_yolo11n/

FASE 3: VALIDAÇÃO (10 minutos)
├── 1. python src/validate.py
├── 2. Analisar métricas (mAP50)
├── 3. Ver confusion_matrix.png
└── 4. Decidir se precisa retreinar

FASE 4: USO (imediato)
├── 1. python src/detect_webcam.py
├── 2. Testar todas as letras
├── 3. Ajustar confiança (+/-)
└── 4. Salvar exemplos (S)

FASE 5: DEPLOY (opcional)
├── 1. python src/export_model.py
├── 2. Integrar em app/sistema
└── 3. Monitorar performance
```

---

## 📊 MÉTRICAS E SAÍDAS

### Durante Treinamento

```
Terminal: Progresso época por época
runs/train/libras_yolo11n/
├── weights/
│   ├── last.pt          # Atualizado a cada época
│   └── best.pt          # Melhor modelo (atualizado quando melhora)
├── results.csv          # Métricas em CSV
└── results.png          # Gráficos (gerado no final)
```

### Após Validação

```
Terminal: Métricas finais (mAP, Precisão, Recall)
runs/val/libras_yolo11n_validation/
├── predictions.json     # Predições em JSON
└── Gráficos de validação
```

### Detecções

```
Webcam: Detecções em tempo real na tela
Imagens: runs/detect/libras_predictions/
         └── Imagens com bounding boxes e labels
```

---

## 🆘 TROUBLESHOOTING RÁPIDO

| Problema       | Arquivo de Ajuda     | Seção            |
| -------------- | -------------------- | ---------------- |
| Instalação     | START_HERE.md        | Checklist        |
| Comandos       | QUICK_START.md       | Comandos         |
| Erro no script | GUIA_PT.md           | Troubleshooting  |
| Parâmetros     | README.md            | Configuração     |
| Métricas       | SUMMARY.md           | Métricas         |
| Dataset        | analyze_dataset.py   | Execute o script |
| Ambiente       | check_environment.py | Execute o script |

---

## 📱 REFERÊNCIA RÁPIDA

### Comandos Essenciais

```powershell
# Ativar ambiente
.\venv\Scripts\Activate.ps1

# Verificar
python src/check_environment.py

# Treinar
python src/train.py

# Validar
python src/validate.py

# Webcam
python src/detect_webcam.py
```

### Arquivos Importantes

```
Modelo treinado:
runs/train/libras_yolo11n/weights/best.pt

Resultados:
runs/train/libras_yolo11n/results.png
runs/train/libras_yolo11n/confusion_matrix.png

Dataset:
dataset_distribution.png
```

### Links Internos

- 🚀 Início: [START_HERE.md](START_HERE.md)
- ⚡ Rápido: [QUICK_START.md](QUICK_START.md)
- 🇧🇷 Português: [GUIA_PT.md](GUIA_PT.md)
- 📘 Técnico: [README.md](README.md)
- 📊 Resumo: [SUMMARY.md](SUMMARY.md)

---

## 📈 TEMPO ESTIMADO POR TAREFA

| Tarefa                | Tempo     |
| --------------------- | --------- |
| Ler START_HERE.md     | 3 min     |
| Ler QUICK_START.md    | 5 min     |
| Ler GUIA_PT.md        | 15-20 min |
| check_environment.py  | 10 seg    |
| analyze_dataset.py    | 30 seg    |
| train.py (10 epochs)  | 15-20 min |
| train.py (100 epochs) | 2-4 horas |
| validate.py           | 5-10 min  |
| detect_webcam.py      | Imediato  |
| detect_image.py       | 1-5 min   |
| export_model.py       | 1-2 min   |

---

## 🎓 NÍVEIS DE CONHECIMENTO

### Iniciante

- Leia: START_HERE.md, QUICK_START.md
- Execute: check_environment.py, train.py
- Use: detect_webcam.py

### Intermediário

- Leia: GUIA_PT.md, README.md
- Ajuste: Parâmetros em train.py
- Analise: Métricas e gráficos

### Avançado

- Leia: README.md, SUMMARY.md, código fonte
- Otimize: Hiperparâmetros, arquitetura
- Deploy: export_model.py, integração

---

## 📞 SUPORTE

1. **Primeira linha:** Leia START_HERE.md
2. **Comandos:** Consulte QUICK_START.md
3. **Explicação:** Leia GUIA_PT.md
4. **Técnico:** Consulte README.md
5. **Diagnóstico:** Execute check_environment.py

---

**Última atualização:** 11/11/2025  
**Versão:** 1.0  
**Total de arquivos:** 16  
**Status:** ✅ Completo e funcional

---

**🎯 Lembre-se: Comece pelo START_HERE.md!**
