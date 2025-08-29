# 🖥️ Interface Gráfica - CompactPDF

Interface gráfica moderna e intuitiva para o sistema CompactPDF.

## 📋 Visão Geral

A GUI do CompactPDF oferece uma experiência visual completa para compressão de PDFs, incluindo:

- 📁 **Seleção fácil de arquivos** - Arrastar e soltar ou navegador de arquivos
- ⚙️ **Configurações intuitivas** - Presets e configurações avançadas
- 📊 **Monitoramento em tempo real** - Barra de progresso e status detalhado
- 📈 **Resultados visuais** - Estatísticas e relatórios de compressão
- 🎨 **Interface moderna** - Design responsivo e acessível

## 🚀 Como Executar

### Método 1: Script Automático (Windows)
```bash
# Execute o arquivo batch
executar_gui.bat
```

### Método 2: Python Direto
```bash
# Versão de demonstração (funciona sem projeto completo)
python gui_simples.py

# Versão completa (requer projeto configurado)
python launch_gui.py
```

### Método 3: Importação em Python
```python
from gui_simples import CompactPDFGUISimples
import tkinter as tk

root = tk.Tk()
app = CompactPDFGUISimples(root)
root.mainloop()
```

## 📸 Capturas de Tela

### Interface Principal
```
┌─────────────────────────────────────────────────────────────┐
│ 🗜️ CompactPDF - Demo                                        │
│ Compressor Inteligente de PDFs (Versão Demonstração)       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📁 Seleção de Arquivos                                      │
│ ┌─────────────────┐ ┌──────────┐                           │
│ │ 📄 Selecionar   │ │ 🗑️ Limpar │                           │
│ │    PDFs         │ │          │                           │
│ └─────────────────┘ └──────────┘                           │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ documento1.pdf (2.5 MB)                                 │ │
│ │ relatorio.pdf (5.1 MB)                                  │ │
│ │ catalogo.pdf (12.3 MB)                                  │ │
│ └─────────────────────────────────────────────────────────┘ │
│ 3 arquivo(s) selecionado(s)                                │
│                                                             │
│ ⚙️ Configurações                                            │
│ Preset: [Balanced ▼]                                       │
│ Pasta de Destino: ./comprimidos [📁]                       │
│                                                             │
│ 🚀 Processamento                                            │
│        ┌─────────────────────────┐                         │
│        │ 🗜️ COMPRIMIR ARQUIVOS   │                         │
│        └─────────────────────────┘                         │
│                                                             │
│ [████████████████████████████████████████] 100%            │
│ Concluído!                                                  │
│                                                             │
│ 📊 Resultados                                               │
│ Arquivos processados: 3 | Espaço economizado: 4.2 MB      │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ✅ documento1.pdf: 28.5% redução (0.7 MB economizado)  │ │
│ │ ✅ relatorio.pdf: 31.2% redução (1.6 MB economizado)   │ │
│ │ ✅ catalogo.pdf: 25.8% redução (3.2 MB economizado)    │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎛️ Funcionalidades da Interface

### 📁 Seleção de Arquivos
- **Selecionar PDFs individuais** - Navegador de arquivos padrão
- **Seleção de pastas** - Processa todos os PDFs de uma pasta
- **Lista visual** - Mostra nome, tamanho e status de cada arquivo
- **Informações dinâmicas** - Contadores e estatísticas em tempo real

### ⚙️ Configurações
- **Presets prontos:**
  - 🌐 **Web** - Máxima compressão para uso online
  - ⚖️ **Balanced** - Equilíbrio entre qualidade e tamanho
  - ✨ **Quality** - Prioriza qualidade visual
  - 🗜️ **Maximum** - Compressão máxima possível

- **Configurações avançadas** (versão completa):
  - Controle de qualidade (0-100%)
  - DPI máximo para imagens
  - Opções de processamento paralelo
  - Cache inteligente

### 🚀 Processamento
- **Barra de progresso** - Visual em tempo real
- **Status detalhado** - Arquivo atual sendo processado
- **Processamento em background** - Interface não trava
- **Cancelamento** - Possibilidade de interromper

### 📊 Resultados
- **Estatísticas gerais** - Total processado e economia
- **Resultados por arquivo** - Detalhes de cada compressão
- **Indicadores visuais** - ✅ Sucesso, ❌ Erro
- **Exportação de relatórios** - Salvar resultados em arquivo

## 🔧 Configuração Avançada

### Personalizando a Interface

```python
# Exemplo de personalização
class MeuCompactPDFGUI(CompactPDFGUISimples):
    def configurar_estilos(self):
        super().configurar_estilos()
        
        # Tema escuro
        self.style.configure(".", background="#2c3e50", foreground="white")
        
        # Cores personalizadas
        self.style.configure(
            "Custom.TButton",
            background="#3498db",
            foreground="white"
        )
```

### Integrando com Sistema Existente

```python
# Integração com sistema próprio
from gui_simples import CompactPDFGUISimples

class IntegracaoSistema:
    def __init__(self):
        self.gui = None
    
    def abrir_compressor(self, arquivos_iniciais=None):
        """Abre GUI com arquivos pré-selecionados."""
        root = tk.Tk()
        self.gui = CompactPDFGUISimples(root)
        
        if arquivos_iniciais:
            self.gui.arquivos_selecionados = arquivos_iniciais
            self.gui.atualizar_lista_arquivos()
        
        root.mainloop()
    
    def comprimir_automatico(self, arquivos, pasta_saida):
        """Compressão automática sem GUI."""
        # Usar API diretamente
        pass
```

## 🎨 Temas e Customização

### Temas Disponíveis
- **Claro** (padrão) - Interface limpa e moderna
- **Escuro** - Para uso em ambientes com pouca luz
- **Sistema** - Segue tema do sistema operacional

### Customização de Cores
```python
# Personalizar cores
cores_personalizadas = {
    'primaria': '#3498db',      # Azul
    'sucesso': '#27ae60',       # Verde
    'erro': '#e74c3c',          # Vermelho
    'aviso': '#f39c12',         # Laranja
    'fundo': '#ecf0f1',         # Cinza claro
    'texto': '#2c3e50'          # Cinza escuro
}
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### Interface não abre
```bash
# Verificar Python
python --version

# Verificar tkinter
python -c "import tkinter; print('Tkinter OK')"

# No Linux/Ubuntu, instalar tkinter
sudo apt-get install python3-tk
```

#### Erro de importação
```bash
# Usar versão simples (não depende do projeto)
python gui_simples.py

# Ou configurar PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
python gui.py
```

#### Interface lenta
- Reduza o número de arquivos processados simultaneamente
- Use SSD ao invés de HD para melhor performance
- Feche outros programas que consomem memória

#### Resultados incorretos (versão demo)
- A versão `gui_simples.py` usa dados simulados
- Para resultados reais, configure o projeto completo
- Use `python launch_gui.py` para versão completa

### Logs e Diagnóstico

```python
# Habilitar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar dependências
python -c "
import sys
print('Python:', sys.version)
try:
    import tkinter
    print('Tkinter: OK')
except ImportError:
    print('Tkinter: ERRO - Não instalado')
"
```

## 🔄 Atualizações e Melhorias

### Versão Atual: 1.0 Demo
- ✅ Interface básica funcional
- ✅ Seleção de arquivos
- ✅ Simulação de compressão
- ✅ Barra de progresso
- ✅ Resultados visuais

### Próximas Versões
- 🔄 Integração completa com API
- 🔄 Drag & drop de arquivos
- 🔄 Preview de PDFs
- 🔄 Temas personalizáveis
- 🔄 Configurações salvas
- 🔄 Histórico de compressões
- 🔄 Notificações do sistema

## 🤝 Contribuindo

### Como Contribuir
1. **Fork** o repositório
2. **Clone** sua fork
3. **Crie** uma branch para sua feature
4. **Implemente** melhorias na GUI
5. **Teste** em diferentes sistemas
6. **Envie** pull request

### Áreas para Contribuição
- 🎨 Melhorias visuais e UX
- 🔧 Novas funcionalidades
- 🐛 Correção de bugs
- 📱 Responsividade
- 🌐 Internacionalização
- ♿ Acessibilidade

### Padrões de Código
```python
# Usar docstrings
def minha_funcao(parametro):
    """
    Descrição da função.
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        Descrição do retorno
    """
    pass

# Nomear widgets claramente
self.btn_comprimir = ttk.Button(...)
self.lbl_status = ttk.Label(...)
self.tree_arquivos = ttk.Treeview(...)
```

## 📄 Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para detalhes.

---

*🚀 Interface criada com Python + Tkinter • Compatível com Windows, Linux e macOS*
