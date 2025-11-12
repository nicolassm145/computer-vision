# 🤟 Projeto LIBRAS - Detector com YOLOv11n

## 📌 RESUMO EXECUTIVO

✅ **Status:** Ambiente 100% Configurado e Pronto  
🎯 **Objetivo:** Detectar 22 letras do alfabeto em LIBRAS usando IA  
⏱️ **Tempo para treinar:** 2-4 horas (CPU) ou 30-60 min (GPU)  
📊 **Dataset:** 1,210+ imagens etiquetadas

---

## 🎬 COMEÇAR AGORA - 3 COMANDOS

```powershell
# 1. Ativar ambiente
.\venv\Scripts\Activate.ps1

# 2. Treinar modelo
python src/train.py

# 3. Testar com webcam
python src/detect_webcam.py
```

---

## 📖 EXPLICAÇÃO COMPLETA - PASSO A PASSO

### 🔍 O Que Foi Criado?

Um sistema completo de IA para reconhecer letras em linguagem de sinais através de:

- 🎥 Webcam em tempo real
- 📸 Análise de imagens
- 🤖 Modelo YOLOv11n (state-of-the-art)

### 🏗️ Estrutura do Projeto

```
computer-vision/
│
├── 📚 Documentação
│   ├── README.md          ← Documentação técnica completa
│   ├── QUICK_START.md     ← Guia rápido de uso
│   ├── SUMMARY.md         ← Resumo técnico
│   └── GUIA_PT.md         ← Este arquivo (guia em português)
│
├── 💻 Código Python (src/)
│   ├── train.py           ← PRINCIPAL: Treina o modelo
│   ├── validate.py        ← Valida o modelo treinado
│   ├── detect_webcam.py   ← Usa webcam para detectar
│   ├── detect_image.py    ← Detecta em fotos
│   ├── export_model.py    ← Exporta para mobile/web
│   └── check_environment.py ← Verifica se está tudo OK
│
├── ⚙️ Configuração (config/)
│   └── data.yaml          ← Configuração do dataset
│
├── 📊 Dados (dataset/)
│   ├── train/             ← 1,210 imagens para treinar
│   ├── valid/             ← Imagens para validar
│   └── test/              ← Imagens para testar
│
├── 📈 Resultados (runs/)
│   ├── train/             ← Resultados do treinamento
│   ├── val/               ← Resultados da validação
│   └── detect/            ← Detecções salvas
│
└── 🐍 Ambiente Python (venv/)
    └── Bibliotecas instaladas
```

---

## 🎓 ENTENDENDO CADA ARQUIVO

### 1. `train.py` - O Cérebro do Projeto

**O que faz:**

- Baixa o modelo YOLOv11n pré-treinado
- Ensina o modelo a reconhecer letras LIBRAS
- Salva o melhor modelo automaticamente
- Gera gráficos de performance

**Como usar:**

```powershell
python src/train.py
```

**O que acontece:**

1. ⏬ Download do YOLOv11n (~6MB)
2. 🔄 Treinamento por 100 epochs (~2-4 horas)
3. 💾 Salvamento automático do melhor modelo
4. 📊 Geração de gráficos e métricas
5. ✅ Conclusão com modelo pronto para uso

**Onde encontrar o resultado:**

- Modelo: `runs/train/libras_yolo11n/weights/best.pt`
- Gráficos: `runs/train/libras_yolo11n/results.png`

---

### 2. `detect_webcam.py` - Detecção em Tempo Real

**O que faz:**

- Abre sua webcam
- Detecta letras LIBRAS em tempo real
- Mostra a letra detectada na tela
- Permite ajustar sensibilidade

**Como usar:**

```powershell
python src/detect_webcam.py
```

**Controles:**

- `Q` - Sair do programa
- `S` - Salvar foto atual
- `+` - Aumentar sensibilidade (mais detecções)
- `-` - Diminuir sensibilidade (menos detecções)

**Dicas para melhor resultado:**

- Use luz natural ou boa iluminação
- Fundo claro e uniforme
- Mão a ~50cm da câmera
- Movimentos lentos e claros

---

### 3. `validate.py` - Verificar Qualidade

**O que faz:**

- Testa o modelo no conjunto de teste
- Calcula métricas de qualidade
- Gera relatórios de performance

**Como usar:**

```powershell
python src/validate.py
```

**Métricas geradas:**

- **mAP50**: Precisão média (quanto maior, melhor)
  - > 90% = Excelente 🟢
  - 70-90% = Bom 🟡
  - < 70% = Precisa melhorar 🔴
- **Precisão**: Quantas detecções estão corretas
- **Recall**: Quantas letras foram encontradas

---

### 4. `detect_image.py` - Análise de Fotos

**O que faz:**

- Detecta letras LIBRAS em fotos
- Pode processar múltiplas imagens
- Salva resultados automaticamente

**Como usar:**

```powershell
# Processar todas as imagens de teste
python src/detect_image.py

# Processar uma foto específica
python src/detect_image.py --image "foto.jpg"

# Ajustar sensibilidade
python src/detect_image.py --conf 0.7
```

---

### 5. `export_model.py` - Para Produção

**O que faz:**

- Converte o modelo para outros formatos
- Permite usar em apps mobile
- Otimiza para diferentes plataformas

**Como usar:**

```powershell
# Exportar para ONNX (universal)
python src/export_model.py --formats onnx

# Exportar para mobile
python src/export_model.py --formats tflite

# Múltiplos formatos
python src/export_model.py --formats onnx tflite
```

---

### 6. `check_environment.py` - Diagnóstico

**O que faz:**

- Verifica se tudo está instalado
- Testa o ambiente
- Diagnóstica problemas

**Como usar:**

```powershell
python src/check_environment.py
```

---

## 🎯 FLUXO DE TRABALHO COMPLETO

```
1️⃣ PREPARAÇÃO (1 vez)
   ├── Criar ambiente virtual ✅ (JÁ FEITO)
   ├── Instalar bibliotecas ✅ (JÁ FEITO)
   └── Verificar dataset ✅ (JÁ FEITO)

2️⃣ TREINAMENTO (2-4 horas)
   ├── python src/train.py
   ├── Aguardar conclusão
   └── Verificar gráficos em runs/train/

3️⃣ VALIDAÇÃO (5 minutos)
   ├── python src/validate.py
   └── Analisar métricas (mAP, precisão)

4️⃣ TESTE (imediato)
   ├── python src/detect_webcam.py
   └── Testar com suas mãos!

5️⃣ USO (contínuo)
   └── Usar o modelo para detectar LIBRAS
```

---

## 📊 O QUE ESPERAR DO TREINAMENTO

### Durante o Treinamento

```
Epoch   GPU_mem   box_loss   cls_loss   dfl_loss   Instances   Size
1/100      0.00G     1.234      2.345      1.456        425     640

🔄 Em andamento... (~2% por epoch)
```

### Depois do Treinamento

```
📁 runs/train/libras_yolo11n/
    ├── weights/
    │   ├── best.pt         ← MODELO PRINCIPAL (use este!)
    │   └── last.pt         ← Último checkpoint
    ├── results.png         ← Gráfico de métricas
    ├── confusion_matrix.png ← Onde o modelo erra
    ├── F1_curve.png        ← Curva F1
    └── PR_curve.png        ← Precision-Recall
```

---

## 🎨 INTERPRETANDO OS GRÁFICOS

### results.png

```
📈 Box Loss    ↘️ Deve diminuir (erro diminuindo)
📈 Class Loss  ↘️ Deve diminuir (aprendendo classes)
📈 mAP50       ↗️ Deve aumentar (ficando melhor)
📈 Precision   ↗️ Deve aumentar (mais preciso)
📈 Recall      ↗️ Deve aumentar (encontra mais)
```

### confusion_matrix.png

```
       A  B  C  D1 D2 ...
    A [95  2  1   0  1 ...]  ← 95% correto para A
    B [ 1 93  3   1  0 ...]  ← 93% correto para B
    C [ 2  1 94   0  2 ...]  ← 94% correto para C
    ...

Diagonal = Acertos ✅
Fora = Confusões ⚠️
```

---

## ⚡ TESTE RÁPIDO (10 Minutos)

Antes do treinamento completo, faça um teste:

1. **Edite** `src/train.py`
2. **Mude** `epochs=100` para `epochs=10`
3. **Execute** `python src/train.py`
4. **Aguarde** ~10-15 minutos
5. **Teste** `python src/detect_webcam.py`

Isso treina rapidamente mas com qualidade menor - apenas para testar se funciona!

---

## 🔧 AJUSTES E OTIMIZAÇÕES

### Se o Treinamento Está Lento

```python
# Edite src/train.py:
batch=16  →  batch=8   # Usa menos memória
workers=4  →  workers=2 # Menos processamento
```

### Se a Detecção Está Ruim

```python
# Edite src/train.py:
epochs=100  →  epochs=150  # Treina mais
patience=20 →  patience=30 # Mais paciência
```

### Se Quer Mais Velocidade

```python
# Se tiver GPU NVIDIA:
device='cpu'  →  device=0  # Usa GPU
# 10x mais rápido!
```

---

## 🆘 SOLUÇÕES PARA PROBLEMAS

### ❌ "Modelo não encontrado"

**Causa:** Você não treinou ainda  
**Solução:**

```powershell
python src/train.py
```

### ❌ "Webcam não abre"

**Causa:** Outra aplicação está usando  
**Solução:**

1. Feche Skype, Teams, Zoom
2. Reinicie o script
3. Verifique se a webcam funciona em outros apps

### ❌ "Script não roda"

**Causa:** Ambiente não ativado  
**Solução:**

```powershell
.\venv\Scripts\Activate.ps1
python src/check_environment.py
```

### ❌ "Memória insuficiente"

**Causa:** Batch size muito alto  
**Solução:** Edite `train.py`, mude `batch=16` para `batch=4`

### ❌ "Detecção não funciona bem"

**Causa:** Treinamento insuficiente ou condições ruins  
**Solução:**

1. Treine por mais epochs
2. Use melhor iluminação
3. Fundo neutro
4. Ajuste threshold: `+` ou `-` na webcam

---

## 📈 MÉTRICAS - O QUE SIGNIFICAM?

### mAP (Mean Average Precision)

```
🎯 Mede: Quão preciso é o modelo
📊 Escala: 0 a 1 (0% a 100%)
✅ Bom: > 0.8 (80%)
🌟 Ótimo: > 0.9 (90%)
```

### Precisão (Precision)

```
🎯 Mede: Das detecções feitas, quantas estão corretas
📊 Exemplo: 90% = 9 de 10 detecções estão certas
```

### Recall

```
🎯 Mede: De todas as letras, quantas foram encontradas
📊 Exemplo: 85% = encontrou 85 de 100 letras
```

### F1-Score

```
🎯 Mede: Balanço entre Precisão e Recall
📊 Fórmula: 2 × (Precisão × Recall) / (Precisão + Recall)
```

---

## 🎮 USANDO A WEBCAM - GUIA COMPLETO

### Preparação

1. ✅ Boa iluminação (janela ou luz artificial)
2. ✅ Fundo neutro (parede clara)
3. ✅ Webcam estável
4. ✅ Espaço livre (~1 metro)

### Execução

```powershell
python src/detect_webcam.py
```

### Testando Letras

1. 🤟 Faça a letra com a mão
2. 👀 Veja a detecção na tela
3. 📊 Veja a confiança (0-1)
4. 🎯 Ajuste com `+` ou `-`

### Salvando Exemplos

1. 🖐️ Faça a letra
2. ⌨️ Pressione `S`
3. 📸 Foto salva como `detection_0.jpg`

### Ajustando Sensibilidade

```
Threshold Baixo (0.3)  → Muitas detecções (algumas erradas)
Threshold Médio (0.5)  → Balanceado
Threshold Alto (0.8)   → Poucas detecções (muito confiantes)
```

---

## 🚀 PRÓXIMOS NÍVEIS

### Nível 1: Básico (Você está aqui!)

- ✅ Ambiente configurado
- ✅ Dataset pronto
- ⏳ Treinar modelo
- ⏳ Testar com webcam

### Nível 2: Intermediário

- [ ] Otimizar hiperparâmetros
- [ ] Adicionar mais dados
- [ ] Melhorar iluminação
- [ ] Criar interface gráfica

### Nível 3: Avançado

- [ ] Data augmentation
- [ ] Ensemble models
- [ ] Exportar para mobile
- [ ] Deploy em nuvem

### Nível 4: Profissional

- [ ] API REST
- [ ] App mobile
- [ ] Integração com sistemas
- [ ] Monitoramento em produção

---

## 📚 RECURSOS ADICIONAIS

### Arquivos de Ajuda

- `README.md` - Documentação técnica
- `QUICK_START.md` - Início rápido
- `SUMMARY.md` - Resumo técnico
- `GUIA_PT.md` - Este guia em português

### Comandos de Referência

```powershell
# Ambiente
.\venv\Scripts\Activate.ps1
python src/check_environment.py

# Treinamento
python src/train.py

# Validação
python src/validate.py

# Detecção
python src/detect_webcam.py
python src/detect_image.py

# Exportação
python src/export_model.py --formats onnx

# Ajuda
python src/detect_image.py --help
```

---

## 🎯 CHECKLIST DE PROGRESSO

### Configuração

- [x] Ambiente virtual criado
- [x] Bibliotecas instaladas
- [x] Dataset verificado
- [x] Estrutura criada

### Treinamento

- [ ] Modelo treinado (100 epochs)
- [ ] Gráficos analisados
- [ ] Métricas avaliadas
- [ ] Modelo salvo

### Validação

- [ ] Validação executada
- [ ] mAP calculado
- [ ] Confusion matrix analisada
- [ ] Performance OK

### Uso

- [ ] Testado com webcam
- [ ] Testado com imagens
- [ ] Sensibilidade ajustada
- [ ] Resultados satisfatórios

---

## 💡 DICAS PROFISSIONAIS

### Para Melhor Performance

1. 🌞 Use luz natural quando possível
2. 🎨 Fundo neutro (cinza, branco, preto)
3. 👕 Roupa contrastante com o fundo
4. 📏 Mantenha distância consistente (~50cm)
5. ⏱️ Movimentos lentos e deliberados

### Para Melhor Modelo

1. 📊 Mais dados = melhor modelo
2. ⚖️ Dados balanceados (mesma quantidade por classe)
3. 🔄 Data augmentation (variações nas imagens)
4. 🎯 Ajuste fino de hiperparâmetros
5. ⏳ Paciência no treinamento

### Para Debugging

1. 🔍 Use `check_environment.py` primeiro
2. 📊 Analise os gráficos sempre
3. 📈 Compare metrics entre epochs
4. 🎯 Teste incrementalmente
5. 📝 Documente mudanças e resultados

---

## 🎉 CONCLUSÃO

Você agora tem:

- ✅ Ambiente completo configurado
- ✅ 6 scripts Python prontos
- ✅ Dataset com 1,210+ imagens
- ✅ Documentação completa
- ✅ Guias de uso e troubleshooting

**Próximo passo:** Execute `python src/train.py` e aguarde!

**Tempo total estimado até primeira detecção:**

- ⏱️ Treinamento: 2-4 horas
- ⏱️ Validação: 5 minutos
- ⏱️ Teste: Imediato
- **Total: ~3-4 horas para ter o sistema funcionando!**

---

**🤟 Boa sorte com seu detector de LIBRAS!**

**Autor:** Nicolas  
**Data:** 11 de Novembro de 2025  
**Versão:** 1.0

---

**📞 Dúvidas?**

1. Leia `QUICK_START.md` para início rápido
2. Leia `README.md` para detalhes técnicos
3. Execute `python src/check_environment.py` para diagnóstico
4. Verifique os comentários nos scripts Python

**🚀 Vamos lá!**
