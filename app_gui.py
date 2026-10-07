"""
=============================================================================
SISTEMA DE AGENDAMENTO MÉDICO INTELIGENTE - INTERFACE GRÁFICA (TKINTER)
Disciplina: Chatbots e Inteligência Artificial
Projeto Prático Colaborativo

Interface gráfica moderna, profissional e intuitiva desenvolvida em Tkinter/ttk.
Compatível nativamente com Windows, sem necessidade de bibliotecas externas.
=============================================================================
"""

import os
import sys
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
from typing import Any, Dict, List, Optional

# Importa as regras de negócio e camada de dados já consolidadas
import main as core


class SistemaAgendamentoGUI:
    """Interface Gráfica Profissional para o Sistema de Agendamento Médico."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"🏥 {core.NOME_CLINICA} - Painel de Atendimento Inteligente")
        self.root.minsize(960, 640)
        self.root.configure(bg="#f1f5f9")

        # Dados em memória
        self.agendamentos: List[Dict[str, Any]] = core.carregar_agendamentos()

        # Configuração de Estilo ttk
        self.setup_estilo()

        # Construção dos Componentes Visuais
        self.criar_cabecalho()
        self.criar_notebook_abas()
        self.criar_barra_status()

        # Carregamento inicial da tabela
        self.atualizar_tabela_consultas()
        self.atualizar_contador_badge()

        # Posiciona e exibe a janela com destaque em primeiro plano
        self.centralizar_e_destacar_janela()

    def centralizar_e_destacar_janela(self, largura: int = 1060, altura: int = 700) -> None:
        """Centraliza o painel na tela e força a abertura no primeiro plano do Windows."""
        self.root.update_idletasks()
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = max(0, (largura_tela - largura) // 2)
        pos_y = max(0, (altura_tela - altura) // 2)
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Traz a janela para frente de outros aplicativos (como o VS Code)
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(300, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

    def setup_estilo(self) -> None:
        """Configura temas e estilos visuais para os componentes ttk."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cores corporativas
        self.COR_PRIMARIA = "#0f766e"    # Verde Petróleo / Teal Hospitalar
        self.COR_SECUNDARIA = "#0284c7"  # Azul Médico
        self.COR_FUNDO = "#f1f5f9"       # Cinza Claro
        self.COR_CARD = "#ffffff"        # Branco Puro
        self.COR_TEXTO = "#0f172a"       # Cinza Chumbo Escuro
        self.COR_SUCESSO = "#16a34a"     # Verde Sucesso
        self.COR_PERIGO = "#dc2626"      # Vermelho Alerta

        # Estilo das Abas (Notebook)
        self.style.configure(
            "TNotebook",
            background=self.COR_FUNDO,
            borderwidth=0,
        )
        self.style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 11, "bold"),
            padding=[16, 8],
            background="#e2e8f0",
            foreground="#475569",
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.COR_PRIMARIA)],
            foreground=[("selected", "#ffffff")],
        )

        # Estilo de Tabelas (Treeview)
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.COR_TEXTO,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#e2e8f0",
            foreground="#1e293b",
            padding=[6, 6],
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#bae6fd")],
            foreground=[("selected", "#0c4a6e")],
        )

    def criar_cabecalho(self) -> None:
        """Cria a barra superior de identificação da clínica."""
        header_frame = tk.Frame(self.root, bg=self.COR_PRIMARIA, height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Informações da Clínica
        titulo_frame = tk.Frame(header_frame, bg=self.COR_PRIMARIA)
        titulo_frame.pack(side="left", padx=20, pady=10)

        lbl_icone = tk.Label(
            titulo_frame,
            text="🏥",
            font=("Segoe UI Emoji", 26),
            bg=self.COR_PRIMARIA,
            fg="#ffffff",
        )
        lbl_icone.pack(side="left", padx=(0, 10))

        textos_frame = tk.Frame(titulo_frame, bg=self.COR_PRIMARIA)
        textos_frame.pack(side="left")

        lbl_titulo = tk.Label(
            textos_frame,
            text=core.NOME_CLINICA.upper(),
            font=("Segoe UI", 16, "bold"),
            bg=self.COR_PRIMARIA,
            fg="#ffffff",
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = tk.Label(
            textos_frame,
            text="Agendamento Inteligente com UX Design e WhatsApp",
            font=("Segoe UI", 9),
            bg=self.COR_PRIMARIA,
            fg="#ccfbf1",
        )
        lbl_sub.pack(anchor="w")

        # Badge lateral com total de consultas
        self.badge_frame = tk.Frame(header_frame, bg="#115e59", padx=14, pady=8)
        self.badge_frame.pack(side="right", padx=20, pady=15)

        self.lbl_badge_num = tk.Label(
            self.badge_frame,
            text="0",
            font=("Segoe UI", 14, "bold"),
            bg="#115e59",
            fg="#ffffff",
        )
        self.lbl_badge_num.pack(side="left", padx=(0, 6))

        lbl_badge_desc = tk.Label(
            self.badge_frame,
            text="consultas ativas",
            font=("Segoe UI", 9),
            bg="#115e59",
            fg="#e0f2fe",
        )
        lbl_badge_desc.pack(side="left")

    def criar_notebook_abas(self) -> None:
        """Cria as abas de navegação principal da aplicação."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(15, 10))

        # Abas do sistema
        self.aba_agendamento = tk.Frame(self.notebook, bg=self.COR_FUNDO)
        self.aba_consultas = tk.Frame(self.notebook, bg=self.COR_FUNDO)
        self.aba_whatsapp = tk.Frame(self.notebook, bg=self.COR_FUNDO)

        self.notebook.add(self.aba_agendamento, text="  📅 Novo Agendamento  ")
        self.notebook.add(self.aba_consultas, text="  📋 Consultas Marcadas  ")
        self.notebook.add(self.aba_whatsapp, text="  💬 Mensagem WhatsApp  ")

        # Renderização do conteúdo de cada aba
        self.construir_aba_agendamento()
        self.construir_aba_consultas()
        self.construir_aba_whatsapp()

    # =========================================================================
    # ABA 1: FORMULÁRIO DE NOVO AGENDAMENTO
    # =========================================================================

    def construir_aba_agendamento(self) -> None:
        """Constrói o formulário de cadastro de nova consulta com UX amigável."""
        container = tk.Frame(self.aba_agendamento, bg=self.COR_FUNDO)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Card do Formulário (Lado Esquerdo)
        card_form = tk.Frame(container, bg=self.COR_CARD, bd=1, relief="ridge", padx=25, pady=20)
        card_form.pack(side="left", fill="both", expand=True, padx=(0, 15))

        lbl_sec = tk.Label(
            card_form,
            text="Preencha os dados do paciente e da consulta:",
            font=("Segoe UI", 12, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
        )
        lbl_sec.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # 1. Nome do Paciente
        tk.Label(card_form, text="Nome Completo do Paciente *", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_paciente = tk.Entry(card_form, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        self.ent_paciente.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 2. Telefone / WhatsApp
        tk.Label(card_form, text="Telefone / WhatsApp com DDD *", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_telefone = tk.Entry(card_form, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        self.ent_telefone.insert(0, "(11) 9")
        self.ent_telefone.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 3. Médico e Especialidade
        tk.Label(card_form, text="Especialidade & Profissional *", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").grid(row=5, column=0, sticky="w", pady=4)
        opcoes_medicos = [
            f"{v['especialidade']} - {v['medico']}" for v in core.CATALOGO_MEDICOS.values()
        ]
        self.combo_medicos = ttk.Combobox(card_form, values=opcoes_medicos, font=("Segoe UI", 10), state="readonly")
        if opcoes_medicos:
            self.combo_medicos.current(0)
        self.combo_medicos.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 4. Data e Horário (Grid lado a lado)
        data_hora_frame = tk.Frame(card_form, bg=self.COR_CARD)
        data_hora_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Data
        sub_data = tk.Frame(data_hora_frame, bg=self.COR_CARD)
        sub_data.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(sub_data, text="Data da Consulta (DD/MM/AAAA) *", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").pack(anchor="w", pady=2)
        
        data_input_sub = tk.Frame(sub_data, bg=self.COR_CARD)
        data_input_sub.pack(fill="x")
        data_sugerida = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.ent_data = tk.Entry(data_input_sub, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        self.ent_data.insert(0, data_sugerida)
        self.ent_data.pack(side="left", fill="x", expand=True)

        btn_hoje = tk.Button(
            data_input_sub,
            text="Hoje",
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            relief="flat",
            command=lambda: self.definir_data(datetime.now().strftime("%d/%m/%Y")),
        )
        btn_hoje.pack(side="right", padx=(4, 0))

        # Horário
        sub_hora = tk.Frame(data_hora_frame, bg=self.COR_CARD)
        sub_hora.pack(side="right", fill="x", expand=True)
        tk.Label(sub_hora, text="Horário de Atendimento *", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").pack(anchor="w", pady=2)
        
        horarios_disp = [
            f"{h:02d}:{m:02d}" for h in range(7, 19) for m in (0, 30)
        ]
        self.combo_horario = ttk.Combobox(sub_hora, values=horarios_disp, font=("Segoe UI", 10), state="readonly")
        self.combo_horario.set("09:00")
        self.combo_horario.pack(fill="x")

        # 5. Sintomas / Observações
        tk.Label(card_form, text="Observações / Sintomas (Opcional)", font=("Segoe UI", 10, "bold"), bg=self.COR_CARD, fg="#334155").grid(row=8, column=0, sticky="w", pady=4)
        self.ent_obs = tk.Entry(card_form, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        self.ent_obs.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Botões de Ação
        botoes_frame = tk.Frame(card_form, bg=self.COR_CARD)
        botoes_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        btn_salvar = tk.Button(
            botoes_frame,
            text="  ✅ Confirmar Agendamento  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_SUCESSO,
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.acao_confirmar_agendamento,
        )
        btn_salvar.pack(side="left", padx=(0, 10))

        btn_limpar = tk.Button(
            botoes_frame,
            text="Limpar Campos",
            font=("Segoe UI", 10),
            bg="#e2e8f0",
            fg="#475569",
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.limpar_formulario,
        )
        btn_limpar.pack(side="left")

        card_form.columnconfigure(0, weight=1)
        card_form.columnconfigure(1, weight=1)

        # Card de Diretrizes e Informações (Lado Direito)
        card_info = tk.Frame(container, bg=self.COR_CARD, bd=1, relief="ridge", padx=20, pady=20, width=320)
        card_info.pack(side="right", fill="y")
        card_info.pack_propagate(False)

        tk.Label(
            card_info,
            text="📌 Diretrizes do Atendimento",
            font=("Segoe UI", 12, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_PRIMARIA,
        ).pack(anchor="w", pady=(0, 10))

        diretrizes_texto = (
            "• Atendimento: Seg a Sex, das 07:00 às 19:00.\n\n"
            "• Prevenção de Conflitos: O sistema impede agendamentos duplos para o mesmo médico no mesmo horário.\n\n"
            "• Persistência Segura: Ao confirmar, o agendamento é salvo imediatamente no arquivo 'agendamentos.json'.\n\n"
            "• WhatsApp Inteligente: Após salvar, você pode gerar a mensagem pronta para enviar ao paciente."
        )

        tk.Label(
            card_info,
            text=diretrizes_texto,
            font=("Segoe UI", 9),
            bg=self.COR_CARD,
            fg="#475569",
            justify="left",
            wraplength=280,
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(
            card_info,
            text="📍 Endereço da Unidade:\n" + core.ENDERECO_CLINICA,
            font=("Segoe UI", 8, "italic"),
            bg="#f8fafc",
            fg="#64748b",
            padx=10,
            pady=10,
            relief="solid",
            bd=1,
            wraplength=260,
            justify="center",
        ).pack(fill="x", side="bottom")

    def definir_data(self, data_str: str) -> None:
        """Preenche o campo de data rapidamente com um valor."""
        self.ent_data.delete(0, tk.END)
        self.ent_data.insert(0, data_str)

    def limpar_formulario(self) -> None:
        """Limpa todos os campos editáveis do formulário."""
        self.ent_paciente.delete(0, tk.END)
        self.ent_telefone.delete(0, tk.END)
        self.ent_telefone.insert(0, "(11) 9")
        self.ent_obs.delete(0, tk.END)
        self.combo_medicos.current(0)
        self.combo_horario.set("09:00")
        self.ent_paciente.focus_set()

    def acao_confirmar_agendamento(self) -> None:
        """Valida e processa o agendamento a partir do formulário."""
        paciente = self.ent_paciente.get().strip().title()
        telefone_bruto = self.ent_telefone.get().strip()
        data_digitada = self.ent_data.get().strip()
        horario = self.combo_horario.get().strip()
        obs = self.ent_obs.get().strip() or "Consulta de rotina"

        # 1. Validação de Nome
        if len(paciente) < 3 or not any(c.isalpha() for c in paciente):
            messagebox.showwarning(
                "Atenção - Nome Inválido",
                "Por favor, informe o nome completo do paciente contendo letras válidas (mínimo 3 caracteres).",
                parent=self.root,
            )
            self.ent_paciente.focus_set()
            return

        # 2. Validação de Telefone
        apenas_digitos = "".join(filter(str.isdigit, telefone_bruto))
        if len(apenas_digitos) not in (10, 11):
            messagebox.showwarning(
                "Atenção - Telefone Inválido",
                "Informe um telefone com DDD válido (10 ou 11 dígitos, ex: 11987654321).",
                parent=self.root,
            )
            self.ent_telefone.focus_set()
            return

        ddd = apenas_digitos[:2]
        if len(apenas_digitos) == 11:
            tel_fmt = f"({ddd}) {apenas_digitos[2:7]}-{apenas_digitos[7:]}"
        else:
            tel_fmt = f"({ddd}) {apenas_digitos[2:6]}-{apenas_digitos[6:]}"

        # 3. Validação de Médico
        sel_medico_str = self.combo_medicos.get()
        partes = sel_medico_str.split(" - ", 1)
        especialidade = partes[0]
        medico = partes[1] if len(partes) > 1 else partes[0]

        # 4. Validação de Data
        try:
            dt_obj = datetime.strptime(data_digitada, "%d/%m/%Y")
            hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if dt_obj < hoje:
                messagebox.showwarning(
                    "Atenção - Data Passada",
                    "Não é possível agendar consultas para datas que já passaram.",
                    parent=self.root,
                )
                self.ent_data.focus_set()
                return
            data_fmt = dt_obj.strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showwarning(
                "Atenção - Formato de Data",
                "A data deve estar no padrão DD/MM/AAAA (ex: 15/10/2026).",
                parent=self.root,
            )
            self.ent_data.focus_set()
            return

        # 5. Verificação de Conflito de Horário
        if core.verificar_conflito_horario(self.agendamentos, medico, data_fmt, horario):
            messagebox.showerror(
                "Conflito de Horário",
                f"O profissional {medico} já possui consulta marcada no dia {data_fmt} às {horario}!\n\n"
                f"Por favor, escolha outro horário ou outra data.",
                parent=self.root,
            )
            return

        # 6. Criação do Agendamento
        novo_id = core.obter_proximo_id(self.agendamentos)
        novo_agendamento: Dict[str, Any] = {
            "id": novo_id,
            "paciente": paciente,
            "telefone": tel_fmt,
            "especialidade": especialidade,
            "medico": medico,
            "data": data_fmt,
            "horario": horario,
            "observacoes": obs,
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "Confirmada",
        }

        self.agendamentos.append(novo_agendamento)
        if core.salvar_agendamentos(self.agendamentos):
            self.atualizar_tabela_consultas()
            self.atualizar_contador_badge()
            self.limpar_formulario()

            resposta = messagebox.askyesno(
                "Sucesso!",
                f"Consulta #{novo_id} agendada com sucesso para {paciente}!\n\n"
                f"Deseja visualizar a mensagem de confirmação para WhatsApp agora?",
                parent=self.root,
            )
            if resposta:
                self.exibir_mensagem_whatsapp(novo_agendamento)
                self.notebook.select(self.aba_whatsapp)
        else:
            messagebox.showerror(
                "Erro de Salvamento",
                "Não foi possível salvar o agendamento no arquivo JSON.",
                parent=self.root,
            )

    # =========================================================================
    # ABA 2: LISTAGEM E GERENCIAMENTO DE CONSULTAS
    # =========================================================================

    def construir_aba_consultas(self) -> None:
        """Constrói a tabela de visualização com busca dinâmica e botões de ação."""
        container = tk.Frame(self.aba_consultas, bg=self.COR_FUNDO)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Barra de Pesquisa e Ferramentas
        top_bar = tk.Frame(container, bg=self.COR_FUNDO)
        top_bar.pack(fill="x", pady=(0, 10))

        lbl_busca = tk.Label(top_bar, text="🔍 Buscar:", font=("Segoe UI", 10, "bold"), bg=self.COR_FUNDO, fg=self.COR_TEXTO)
        lbl_busca.pack(side="left", padx=(0, 8))

        self.ent_busca = tk.Entry(top_bar, font=("Segoe UI", 10), bg="#ffffff", relief="solid", bd=1, width=32)
        self.ent_busca.pack(side="left", padx=(0, 10))
        self.ent_busca.bind("<KeyRelease>", lambda event: self.filtrar_tabela())

        btn_atualizar = tk.Button(
            top_bar,
            text="🔄 Atualizar Lista",
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            relief="flat",
            cursor="hand2",
            command=self.recarregar_dados_disco,
        )
        btn_atualizar.pack(side="left")

        # Botões de Ação Selecionada (Lado Direito)
        btn_cancelar = tk.Button(
            top_bar,
            text="❌ Cancelar Consulta",
            font=("Segoe UI", 9, "bold"),
            bg="#fee2e2",
            fg=self.COR_PERIGO,
            activebackground=self.COR_PERIGO,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.acao_cancelar_selecionada,
        )
        btn_cancelar.pack(side="right")

        btn_ver_wpp = tk.Button(
            top_bar,
            text="💬 Gerar WhatsApp",
            font=("Segoe UI", 9, "bold"),
            bg="#dcfce7",
            fg=self.COR_SUCESSO,
            activebackground=self.COR_SUCESSO,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.acao_gerar_wpp_selecionada,
        )
        btn_ver_wpp.pack(side="right", padx=(0, 10))

        # Tabela Treeview com Barra de Rolagem
        tabela_frame = tk.Frame(container, bg=self.COR_CARD, bd=1, relief="ridge")
        tabela_frame.pack(fill="both", expand=True)

        colunas = ("id", "data_hora", "paciente", "telefone", "especialidade", "medico", "status")
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("data_hora", text="Data & Horário")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("especialidade", text="Especialidade")
        self.tree.heading("medico", text="Profissional Médico")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("data_hora", width=120, anchor="center")
        self.tree.column("paciente", width=160, anchor="w")
        self.tree.column("telefone", width=110, anchor="center")
        self.tree.column("especialidade", width=120, anchor="w")
        self.tree.column("medico", width=200, anchor="w")
        self.tree.column("status", width=90, anchor="center")

        scrollbar_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Duplo clique abre WhatsApp da consulta
        self.tree.bind("<Double-1>", lambda event: self.acao_gerar_wpp_selecionada())

    def atualizar_tabela_consultas(self, lista_dados: Optional[List[Dict[str, Any]]] = None) -> None:
        """Renderiza os dados na tabela ttk.Treeview."""
        dados = lista_dados if lista_dados is not None else self.agendamentos

        # Limpa dados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ag in dados:
            data_hora = f"{ag.get('data', '')} às {ag.get('horario', '')}"
            self.tree.insert(
                "",
                "end",
                iid=str(ag.get("id")),
                values=(
                    f"#{ag.get('id')}",
                    data_hora,
                    ag.get("paciente", ""),
                    ag.get("telefone", ""),
                    ag.get("especialidade", ""),
                    ag.get("medico", ""),
                    ag.get("status", "Agendada"),
                ),
            )

    def filtrar_tabela(self) -> None:
        """Filtra as consultas na tabela em tempo real com base no texto de busca."""
        termo = self.ent_busca.get().strip().lower()
        if not termo:
            self.atualizar_tabela_consultas(self.agendamentos)
            return

        filtrados = [
            ag for ag in self.agendamentos
            if termo in ag.get("paciente", "").lower()
            or termo in ag.get("medico", "").lower()
            or termo in ag.get("especialidade", "").lower()
            or termo in ag.get("data", "").lower()
        ]
        self.atualizar_tabela_consultas(filtrados)

    def recarregar_dados_disco(self) -> None:
        """Recarrega os dados diretamente do arquivo agendamentos.json."""
        self.agendamentos = core.carregar_agendamentos()
        self.ent_busca.delete(0, tk.END)
        self.atualizar_tabela_consultas()
        self.atualizar_contador_badge()
        messagebox.showinfo("Atualizado", "Base de dados sincronizada com sucesso!", parent=self.root)

    def acao_cancelar_selecionada(self) -> None:
        """Cancela e exclui a consulta selecionada na tabela."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção Necessária", "Selecione uma consulta na tabela para cancelar.", parent=self.root)
            return

        id_selecionado = int(selecionado[0])
        ag = next((a for a in self.agendamentos if a.get("id") == id_selecionado), None)

        if not ag:
            return

        confirma = messagebox.askyesno(
            "Confirmação de Cancelamento",
            f"Tem certeza que deseja cancelar a consulta de:\n\n"
            f"Paciente: {ag.get('paciente')}\n"
            f"Profissional: {ag.get('medico')}\n"
            f"Data: {ag.get('data')} às {ag.get('horario')}\n\n"
            f"Esta operação removerá o agendamento permanentemente.",
            parent=self.root,
        )

        if confirma:
            if core.excluir_agendamento(self.agendamentos, id_selecionado):
                self.atualizar_tabela_consultas()
                self.atualizar_contador_badge()
                messagebox.showinfo("Sucesso", f"Consulta #{id_selecionado} cancelada com sucesso!", parent=self.root)
            else:
                messagebox.showerror("Erro", "Não foi possível remover o registro do arquivo.", parent=self.root)

    def acao_gerar_wpp_selecionada(self) -> None:
        """Gera a mensagem do WhatsApp para a consulta selecionada na tabela."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção Necessária", "Selecione uma consulta na tabela para gerar a mensagem.", parent=self.root)
            return

        id_selecionado = int(selecionado[0])
        ag = next((a for a in self.agendamentos if a.get("id") == id_selecionado), None)
        if ag:
            self.exibir_mensagem_whatsapp(ag)
            self.notebook.select(self.aba_whatsapp)

    # =========================================================================
    # ABA 3: GERADOR DE MENSAGEM WHATSAPP
    # =========================================================================

    def construir_aba_whatsapp(self) -> None:
        """Constrói o painel de visualização e cópia de mensagem do WhatsApp."""
        container = tk.Frame(self.aba_whatsapp, bg=self.COR_FUNDO)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        card_wpp = tk.Frame(container, bg=self.COR_CARD, bd=1, relief="ridge", padx=20, pady=20)
        card_wpp.pack(fill="both", expand=True)

        lbl_topo = tk.Label(
            card_wpp,
            text="💬 Mensagem de Confirmação para Envio via WhatsApp",
            font=("Segoe UI", 12, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_PRIMARIA,
        )
        lbl_topo.pack(anchor="w", pady=(0, 8))

        lbl_instrucao = tk.Label(
            card_wpp,
            text="Esta mensagem foi gerada automaticamente com diretrizes humanizadas e detalhes da consulta. Clique em 'Copiar Mensagem' para enviá-la ao paciente:",
            font=("Segoe UI", 9),
            bg=self.COR_CARD,
            fg="#64748b",
            wraplength=850,
            justify="left",
        )
        lbl_instrucao.pack(anchor="w", pady=(0, 12))

        # Área de Texto com Rolagem
        texto_frame = tk.Frame(card_wpp, bg=self.COR_CARD)
        texto_frame.pack(fill="both", expand=True)

        self.txt_whatsapp = tk.Text(
            texto_frame,
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=12,
            pady=12,
            wrap="word",
        )
        scroll_wpp = ttk.Scrollbar(texto_frame, orient="vertical", command=self.txt_whatsapp.yview)
        self.txt_whatsapp.configure(yscrollcommand=scroll_wpp.set)

        self.txt_whatsapp.pack(side="left", fill="both", expand=True)
        scroll_wpp.pack(side="right", fill="y")

        # Barra de Ações do WhatsApp
        barra_botoes = tk.Frame(card_wpp, bg=self.COR_CARD)
        barra_botoes.pack(fill="x", pady=(15, 0))

        btn_copiar = tk.Button(
            barra_botoes,
            text="  📋 Copiar Mensagem para Área de Transferência  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_PRIMARIA,
            fg="#ffffff",
            activebackground="#115e59",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.copiar_mensagem_clipboard,
        )
        btn_copiar.pack(side="left", padx=(0, 10))

        self.lbl_feedback_copia = tk.Label(
            barra_botoes,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_SUCESSO,
        )
        self.lbl_feedback_copia.pack(side="left")

        # Texto padrão inicial
        if self.agendamentos:
            self.exibir_mensagem_whatsapp(self.agendamentos[0])
        else:
            self.txt_whatsapp.insert(
                "1.0",
                "Nenhum agendamento cadastrado no momento. Cadastre um novo agendamento para gerar a mensagem.",
            )

    def exibir_mensagem_whatsapp(self, agendamento: Dict[str, Any]) -> None:
        """Renderiza a mensagem gerada para o agendamento fornecido."""
        mensagem = core.gerar_mensagem_whatsapp(agendamento)
        self.txt_whatsapp.delete("1.0", tk.END)
        self.txt_whatsapp.insert("1.0", mensagem)
        self.lbl_feedback_copia.config(text="")

    def copiar_mensagem_clipboard(self) -> None:
        """Copia o conteúdo do campo de texto para o clipboard do sistema operacional."""
        conteudo = self.txt_whatsapp.get("1.0", tk.END).strip()
        if not conteudo:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(conteudo)
        self.lbl_feedback_copia.config(text="✅ Mensagem copiada com sucesso para o WhatsApp!")
        self.root.after(4000, lambda: self.lbl_feedback_copia.config(text=""))

    # =========================================================================
    # COMPONENTES AUXILIARES E BARRA DE STATUS
    # =========================================================================

    def atualizar_contador_badge(self) -> None:
        """Atualiza o contador de consultas ativas no cabeçalho."""
        total = len(self.agendamentos)
        self.lbl_badge_num.config(text=str(total))
        self.lbl_status_total.config(text=f"Total: {total} agendamentos registrados")

    def criar_barra_status(self) -> None:
        """Cria o rodapé informativo."""
        status_bar = tk.Frame(self.root, bg="#e2e8f0", height=26, padx=15)
        status_bar.pack(fill="x", side="bottom")

        lbl_arq = tk.Label(
            status_bar,
            text=f"💾 Base Local: {core.ARQUIVO_BANCO}  |  Status: Conectado e Sincronizado",
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            fg="#475569",
        )
        lbl_arq.pack(side="left")

        self.lbl_status_total = tk.Label(
            status_bar,
            text="Total: 0 agendamentos",
            font=("Segoe UI", 8, "bold"),
            bg="#e2e8f0",
            fg="#0f766e",
        )
        self.lbl_status_total.pack(side="right")


def iniciar_interface_grafica() -> None:
    """Inicia a aplicação gráfica Tkinter."""
    root = tk.Tk()
    app = SistemaAgendamentoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interface_grafica()
