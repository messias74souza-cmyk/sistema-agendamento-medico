# 🏥 Sistema de Agendamento Médico Inteligente

> Projeto prático desenvolvido para a disciplina de **Chatbots e Inteligência Artificial**.  
> Simulação de um sistema de recepção e agendamento de consultas médicas com foco em **Experiência do Usuário (UX no Terminal)**, validação robusta de entradas, persistência em arquivo JSON e geração de mensagens humanizadas para WhatsApp.

---

## 👥 Integrantes da Dupla e Divisão de Papéis

| Integrante | Papel no Projeto | Principais Responsabilidades |
| :--- | :--- | :--- |
| **Aluno A** | **Líder do Repositório & Especialista em UX/Validações** | Criação do repositório no GitHub, arquitetura base, design dos menus interativos no terminal (`exibir_menu()`), cabeçalhos estilizados, sanitização e validação de dados com tratamento preventivo de exceções (`try/except`). |
| **Aluno B** | **Engenheiro de Dados & Persistência** | Implementação das funções de I/O (`carregar_agendamentos`, `salvar_agendamentos`, `excluir_agendamento`), integridade dos dados e manipulação do banco em arquivo `agendamentos.json`. |
| **Dupla (A + B)**| **Engenharia de Prompt & Integração** | Construção do gerador de mensagens empáticas e estruturadas para WhatsApp (`gerar_mensagem_whatsapp`). |

---

## 📁 Estrutura do Projeto

```plaintext
sistema-agendamento-medico/
│── .gitignore             # Arquivos ignorados pelo controle de versão (Python, caches, etc.)
│── agendamentos.json      # Banco de dados em texto simples estruturado (JSON)
│── app_gui.py             # Interface Gráfica Profissional em Tkinter (Design Moderno & Intuitivo)
│── painel.pyw             # Launcher Desktop nativo (abre a janela do painel diretamente sem terminal)
│── Abrir_Painel.bat       # Atalho executável de 1 clique para abrir o painel gráfico no Windows
│── main.py                # Código principal do sistema (inicializador híbrido GUI/CLI e regras)
└── README.md              # Documentação técnica e guia colaborativo da aplicação
```

---

## 🚀 Funcionalidades Principais

1. **Interface Gráfica Profissional (Tkinter GUI)**:
   - Painel visual moderno em abas (*Tabs*): Novo Agendamento, Consultas Marcadas e WhatsApp.
   - Pesquisa dinâmica em tempo real por nome do paciente, médico ou data.
   - Botão de cópia direta da mensagem formatada para a área de transferência do Windows.
   - Contador de consultas ativas no cabeçalho em tempo real.

2. **Painel Visual e UX Amigável no Terminal (`Aluno A`)**:
   - Menus desenhados com divisores ASCII e emojis.
   - Navegação intuitiva com a opção de cancelar operações a qualquer momento digitando `0`.
   - Limpeza dinâmica de tela para transições suaves entre menus.

3. **Prevenção Ativa de Erros e Validações (`Aluno A`)**:
   - **Validação de Menus:** Bloqueia caracteres inválidos, espaços vazios ou números fora do intervalo sem encerrar a aplicação.
   - **Validação de Datas:** Impede datas passadas e formatos inválidos através de conversão com `datetime` (`DD/MM/AAAA`).
   - **Validação de Horários:** Restringe o atendimento ao horário comercial da clínica (07:00 às 19:00).
   - **Detecção de Conflitos:** Alerta em tempo real caso um médico já possua consulta agendada para o mesmo dia e horário.
   - **Validação de Telefone:** Formatação e conferência de dígitos com DDD para telefones brasileiros (`(XX) 9XXXX-XXXX`).
   - **Proteção contra Interrupções:** Captura de `KeyboardInterrupt` (`Ctrl+C`) e `EOFError` para encerramento elegante sem *stack traces* feios na tela.

4. **Banco de Dados em Arquivo JSON (`Aluno B`)**:
   - Leitura automática na inicialização e escrita a cada alteração com o módulo `json`.
   - Tratamento com `try/except` para arquivos não encontrados, vazios ou corrompidos (auto-recuperação com arquivo de contingência `.bak`).
   - Validação de integridade de schema para cada registro (`id`, `paciente`, `telefone`, `especialidade`, `medico`, `data`, `horario`).
   - Criação preventiva de cópia de segurança antes de operações de gravação e exclusão.
   - Exclusão e cancelamento de consultas com sincronização atômica no arquivo `agendamentos.json`.

5. **Gerador de Mensagem WhatsApp por IA (`Dupla`)**:
   - Geração automática de texto educado, claro e humanizado contendo identificador da consulta, profissional, horário, endereço da clínica e orientações pré-consulta.

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
- **Python 3.10** ou superior instalado no computador.
- Não requer instalação de nenhuma biblioteca externa (`tkinter` já vem embutido nativamente no Python).

### Passo a Passo

1. **Clone o repositório ou abra a pasta do projeto no VS Code:**
   ```bash
   git clone https://github.com/messias74souza-cmyk/sistema-agendamento-medico.git
   cd sistema-agendamento-medico
   ```

2. **Abrir o Painel Gráfico Diretamente (Desktop / Janela Própria):**
   - **Opção A (Atalho de 1 clique no Windows):** Dê um duplo clique no arquivo `Abrir_Painel.bat`.
   - **Opção B (Sem terminal de fundo):** Dê um duplo clique ou execute `painel.pyw`.
   - **Opção C (Pelo Terminal do VS Code):**
     ```bash
     python main.py
     ```

3. *(Opcional)* **Executar em modo Terminal / CLI (Para avaliação clássica):**
   ```bash
   python main.py --cli
   ```

---

## 🔄 Fluxo de Trabalho e Sincronização Git (Etapas 1 a 5)

Este repositório foi estruturado para atender rigorosamente ao roteiro prático da disciplina:

### 1. Etapa 1 - Configuração no GitHub (Aluno A):
- O **Aluno A** inicializa o repositório remoto `sistema-agendamento-medico`.
- Convida o **Aluno B** como colaborador em: `Settings` > `Collaborators` > `Add people`.
- O **Aluno B** aceita o convite enviado por e-mail ou no dashboard do GitHub.

### 2. Etapa 2 & 3 - Divisão de Branches e Responsabilidades:
- O **Aluno A** faz o commit inicial da estrutura de UX, menus e regras de fluxo.
- O **Aluno B** revisa e integra as rotinas de persistência e gravação de arquivos.

### 3. Etapa 4 - Prompts Utilizados no Desenvolvimento (Codex / IA):
- **Interface e UX (Aluno A):**
  > *"Atue como um especialista em UX Design para aplicações de terminal. Crie uma função em Python chamada exibir_menu() que mostre as opções de agendamento médico de forma organizada, usando divisores visuais e emojis. Garanta que ela valide a opção digitada pelo usuário."*
- **Banco de Dados JSON (Aluno B):**
  > *"Crie duas funções em Python: uma para salvar uma lista de agendamentos em um arquivo chamado agendamentos.json e outra para ler esse arquivo ao iniciar o programa, usando o módulo json e tratamento de erros try/except."*
- **Mensagem para WhatsApp (Dupla):**
  > *"Crie uma função em Python que receba os dados de um agendamento e monte uma mensagem amigável e educada de confirmação de consulta para ser enviada ao paciente via WhatsApp."*

### 4. Etapa 5 - Comandos de Sincronização no Git:
Para manter o repositório sempre alinhado entre a dupla:
```bash
# Antes de iniciar uma alteração, sempre puxe as novidades:
git pull origin main

# Após finalizar e testar sua função:
git add .
git commit -m "feat(ux): aprimora validacao de datas e fluxo de cancelamento"
git push origin main
```

---

## ✅ Checklist de Avaliação do Professor

- [x] Repositório no GitHub configurado para registrar commits de ambos os alunos da dupla.
- [x] O programa executa no terminal do VS Code através do comando `python main.py`.
- [x] As consultas cadastradas continuam salvas no arquivo `agendamentos.json` após fechar e reabrir a aplicação.
- [x] As mensagens de interface do terminal são claras, amigáveis e não fecham com erro se o usuário digitar dados incorretos.

---
*Desenvolvido com excelência técnica e boas práticas da Engenharia de Software.*
