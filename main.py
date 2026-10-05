"""
=============================================================================
SISTEMA DE AGENDAMENTO MÉDICO INTELIGENTE
Disciplina: Chatbots e Inteligência Artificial
Projeto Prático Colaborativo

Divisão de Responsabilidades:
- Aluno A: Arquitetura, UX Design de Terminal, Menus, Validações e Tratamento de Erros
- Aluno B: Camada de Dados, Persistência e Manipulação de Arquivo JSON
- Dupla: Engenharia de Prompt e Geração de Mensagem WhatsApp
=============================================================================
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# =============================================================================
# CONSTANTES E CONFIGURAÇÕES DO SISTEMA
# =============================================================================

ARQUIVO_BANCO: str = "agendamentos.json"
NOME_CLINICA: str = "Clínica Vida & Saúde"
ENDERECO_CLINICA: str = "Av. Paulista, 1500 - Bela Vista, São Paulo - SP"
TELEFONE_CLINICA: str = "(11) 3100-2020"

# Paleta de cores ANSI para UX aprimorada no terminal
class Cores:
    RESET = "\033[0m"
    NEGRITO = "\033[1m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIANO = "\033[96m"
    VERMELHO = "\033[91m"
    CINZA = "\033[90m"


# Catálogo de especialidades e médicos disponíveis
CATALOGO_MEDICOS: Dict[str, Dict[str, str]] = {
    "1": {"especialidade": "Clínica Geral", "medico": "Dra. Camila Silveira (CRM 12456-SP)"},
    "2": {"especialidade": "Cardiologia", "medico": "Dr. Roberto Albuquerque (CRM 98452-SP)"},
    "3": {"especialidade": "Dermatologia", "medico": "Dra. Beatriz Fontana (CRM 74125-SP)"},
    "4": {"especialidade": "Ortopedia", "medico": "Dr. Marcelo Guimarães (CRM 56321-SP)"},
    "5": {"especialidade": "Pediatria", "medico": "Dra. Juliana Prado (CRM 33890-SP)"},
    "6": {"especialidade": "Ginecologia", "medico": "Dra. Fernanda Rocha (CRM 65412-SP)"},
}


# =============================================================================
# MÓDULO DE UX, INTERFACE E VALIDAÇÕES (ALUNO A)
# =============================================================================

def limpar_tela() -> None:
    """Limpa a tela do terminal de acordo com o sistema operacional."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    """Pausa a execução aguardando que o usuário pressione ENTER para continuar."""
    print(f"\n{Cores.CINZA}Pressione [ENTER] para continuar...{Cores.RESET}", end="")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass


def exibir_cabecalho(subtitulo: str = "") -> None:
    """
    Exibe o cabeçalho padronizado da clínica com identidade visual limpa.
    
    Args:
        subtitulo: Texto opcional exibido como título da seção atual.
    """
    print(f"{Cores.CIANO}{'=' * 66}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}   🏥  {NOME_CLINICA.upper()}  🏥{Cores.RESET}")
    print(f"{Cores.CINZA}   Cuidado médico humanizado com tecnologia inteligente{Cores.RESET}")
    print(f"{Cores.CIANO}{'=' * 66}{Cores.RESET}")
    if subtitulo:
        print(f"\n{Cores.AMARELO}▶ {subtitulo.upper()}{Cores.RESET}")
        print(f"{Cores.CINZA}{'-' * 66}{Cores.RESET}")


def exibir_menu() -> str:
    """
    Exibe o menu principal de opções com divisores visuais e emojis,
    garantindo a validação robusta da opção selecionada pelo usuário.
    
    Prompt Original Aluno A:
    "Atue como um especialista em UX Design para aplicações de terminal.
    Crie uma função em Python chamada exibir_menu() que mostre as opções
    de agendamento médico de forma organizada, usando divisores visuais
    e emojis. Garanta que ela valide a opção digitada pelo usuário."

    Returns:
        str: Opção válida escolhida pelo usuário ('0' a '5').
    """
    opcoes_validas = {"1", "2", "3", "4", "5", "0"}

    while True:
        limpar_tela()
        exibir_cabecalho("Painel de Atendimento ao Paciente")

        print(f"\n{Cores.NEGRITO}┌{'─' * 62}┐{Cores.RESET}")
        print(f"{Cores.NEGRITO}│ {Cores.VERDE}📋 MENU PRINCIPAL{Cores.RESET}{' ' * 45}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}├{'─' * 62}┤{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [1] 📅  {Cores.NEGRITO}Agendar Nova Consulta{Cores.RESET}{' ' * 36}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [2] 📑  {Cores.NEGRITO}Listar Todas as Consultas{Cores.RESET}{' ' * 32}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [3] 🔍  {Cores.NEGRITO}Buscar Consultas (Paciente/Médico){Cores.RESET}{' ' * 23}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [4] 💬  {Cores.NEGRITO}Gerar Mensagem de Confirmação (WhatsApp){Cores.RESET}{' ' * 17}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [5] ❌  {Cores.NEGRITO}Cancelar / Excluir Consulta{Cores.RESET}{' ' * 30}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}│{Cores.RESET}  [0] 🚪  {Cores.CINZA}Sair do Sistema{Cores.RESET}{' ' * 42}{Cores.NEGRITO}│{Cores.RESET}")
        print(f"{Cores.NEGRITO}└{'─' * 62}┘{Cores.RESET}")

        try:
            escolha = input(f"\n{Cores.CIANO}👉 Digite a opção desejada [0-5]: {Cores.RESET}").strip()
            if escolha in opcoes_validas:
                return escolha
            
            # Feedback visual de erro de validação
            print(f"\n{Cores.VERMELHO}⚠️  [Erro de Validação]: Opção '{escolha}' inválida!{Cores.RESET}")
            print(f"{Cores.CINZA}Por favor, digite apenas um número entre 0 e 5.{Cores.RESET}")
            pausar()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Cores.AMARELO}Operação cancelada pelo usuário.{Cores.RESET}")
            return "0"


def obter_texto_valido(prompt: str, tamanho_minimo: int = 3, permitir_cancelar: bool = True) -> Optional[str]:
    """
    Solicita uma entrada de texto do usuário com validações de tamanho e conteúdo.
    
    Args:
        prompt: Mensagem exibida para o usuário.
        tamanho_minimo: Comprimento mínimo exigido para o texto.
        permitir_cancelar: Permite que o usuário digite '0' para cancelar a operação.
        
    Returns:
        Optional[str]: O texto validado ou None se o usuário optou por cancelar.
    """
    while True:
        try:
            entrada = input(f"{prompt}").strip()
            
            if permitir_cancelar and entrada == "0":
                print(f"{Cores.AMARELO}Operação cancelada pelo usuário.{Cores.RESET}")
                return None
            
            if len(entrada) < tamanho_minimo:
                print(f"{Cores.VERMELHO}⚠️  [Erro]: O campo deve conter ao menos {tamanho_minimo} caracteres.{Cores.RESET}")
                continue

            # Garante que não é apenas números ou pontuação para nomes
            if not any(c.isalpha() for c in entrada):
                print(f"{Cores.VERMELHO}⚠️  [Erro]: Por favor, digite um texto contendo letras válidas.{Cores.RESET}")
                continue

            return entrada.title()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Cores.AMARELO}Entrada interrompida.{Cores.RESET}")
            return None


def obter_telefone_valido(prompt: str) -> Optional[str]:
    """
    Solicita e valida um número de telefone/WhatsApp brasileiro com DDD.
    Formata automaticamente a saída no padrão (XX) 9XXXX-XXXX.
    
    Returns:
        Optional[str]: Telefone formatado ou None caso cancele.
    """
    while True:
        try:
            entrada = input(f"{prompt}").strip()
            if entrada == "0":
                return None

            # Remove caracteres não numéricos
            apenas_digitos = re.sub(r"\D", "", entrada)

            if len(apenas_digitos) not in (10, 11):
                print(f"{Cores.VERMELHO}⚠️  [Erro]: Telefone inválido! Digite o DDD + número (Ex: 11987654321).{Cores.RESET}")
                continue

            ddd = apenas_digitos[:2]
            if len(apenas_digitos) == 11:
                parte1 = apenas_digitos[2:7]
                parte2 = apenas_digitos[7:]
            else:
                parte1 = apenas_digitos[2:6]
                parte2 = apenas_digitos[6:]

            return f"({ddd}) {parte1}-{parte2}"
        except (KeyboardInterrupt, EOFError):
            return None


def obter_data_valida(prompt: str) -> Optional[str]:
    """
    Valida a entrada de data no formato DD/MM/AAAA, assegurando data de calendário
    válida e que não seja anterior ao dia de hoje.
    
    Returns:
        Optional[str]: Data no formato 'DD/MM/AAAA' ou None caso cancele.
    """
    while True:
        try:
            entrada = input(f"{prompt}").strip()
            if entrada == "0":
                return None

            data_digitada = datetime.strptime(entrada, "%d/%m/%Y")
            data_hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            if data_digitada < data_hoje:
                print(f"{Cores.VERMELHO}⚠️  [Erro]: Não é possível agendar consultas em datas passadas.{Cores.RESET}")
                continue

            return data_digitada.strftime("%d/%m/%Y")
        except ValueError:
            print(f"{Cores.VERMELHO}⚠️  [Erro]: Formato de data inválido! Utilize o padrão DD/MM/AAAA (ex: 15/10/2026).{Cores.RESET}")
        except (KeyboardInterrupt, EOFError):
            return None


def obter_horario_valido(prompt: str) -> Optional[str]:
    """
    Valida a entrada de horário no formato HH:MM dentro do horário de funcionamento
    da clínica (07:00 às 19:00).
    
    Returns:
        Optional[str]: Horário no formato 'HH:MM' ou None caso cancele.
    """
    while True:
        try:
            entrada = input(f"{prompt}").strip()
            if entrada == "0":
                return None

            horario_digitado = datetime.strptime(entrada, "%H:%M").time()
            abertura = datetime.strptime("07:00", "%H:%M").time()
            fechamento = datetime.strptime("19:00", "%H:%M").time()

            if not (abertura <= horario_digitado <= fechamento):
                print(f"{Cores.VERMELHO}⚠️  [Erro]: A clínica atende apenas entre 07:00 e 19:00.{Cores.RESET}")
                continue

            return horario_digitado.strftime("%H:%M")
        except ValueError:
            print(f"{Cores.VERMELHO}⚠️  [Erro]: Formato de hora inválido! Utilize o padrão HH:MM (ex: 14:30).{Cores.RESET}")
        except (KeyboardInterrupt, EOFError):
            return None


def selecionar_especialidade() -> Optional[Dict[str, str]]:
    """
    Apresenta ao usuário o catálogo de médicos e especialidades disponíveis,
    validando a escolha com total prevenção de falhas de digitação.
    
    Returns:
        Optional[Dict[str, str]]: Dados da especialidade e médico selecionados.
    """
    print(f"\n{Cores.NEGRITO}👨‍⚕️  ESPECIALIDADES E CORPO CLÍNICO DISPONÍVEIS:{Cores.RESET}")
    for chave, item in CATALOGO_MEDICOS.items():
        print(f"  [{chave}] {Cores.CIANO}{item['especialidade']:<22}{Cores.RESET} -> {item['medico']}")
    print(f"  [0] {Cores.CINZA}Cancelar agendamento{Cores.RESET}")

    while True:
        try:
            opcao = input(f"\n{Cores.CIANO}👉 Selecione a especialidade desejada [1-{len(CATALOGO_MEDICOS)}]: {Cores.RESET}").strip()
            if opcao == "0":
                return None
            if opcao in CATALOGO_MEDICOS:
                return CATALOGO_MEDICOS[opcao]
            print(f"{Cores.VERMELHO}⚠️  Opção inválida! Escolha um número entre 1 e {len(CATALOGO_MEDICOS)}.{Cores.RESET}")
        except (KeyboardInterrupt, EOFError):
            return None


# =============================================================================
# MÓDULO DE GERAÇÃO DE MENSAGENS POR IA / WHATSAPP (DUPLA)
# =============================================================================

def gerar_mensagem_whatsapp(agendamento: Dict[str, Any]) -> str:
    """
    Gera uma mensagem polida, acolhedora e altamente profissional para ser
    enviada ao paciente através do WhatsApp confirmando os dados da consulta.
    
    Prompt Original da Dupla:
    "Crie uma função em Python que receba os dados de um agendamento e monte
    uma mensagem amigável e educada de confirmação de consulta para ser enviada
    ao paciente via WhatsApp."
    
    Args:
        agendamento: Dicionário contendo os dados completos da consulta.
        
    Returns:
        str: Texto formatado pronto para envio.
    """
    id_cod = agendamento.get("id", "N/A")
    paciente = agendamento.get("paciente", "Paciente")
    especialidade = agendamento.get("especialidade", "Consulta Médica")
    medico = agendamento.get("medico", "Médico Responsável")
    data = agendamento.get("data", "")
    horario = agendamento.get("horario", "")
    observacoes = agendamento.get("observacoes", "Nenhuma observação informada.")

    mensagem = f"""*Olá, {paciente}!* 👋
Esperamos que este contato encontre você muito bem!

Confirmamos o recebimento e agendamento da sua consulta na *{NOME_CLINICA}*. Abaixo estão todas as informações detalhadas do seu atendimento:

────────────────────────────────────
📋 *DETALHES DO SEU AGENDAMENTO*
────────────────────────────────────
🔖 *Código de Identificação:* #{id_cod}
🩺 *Especialidade:* {especialidade}
👨‍⚕️ *Profissional:* {medico}
📅 *Data:* {data}
⏰ *Horário:* {horario}
📝 *Observações / Sintomas:* {observacoes}

📍 *Local de Atendimento:*
{ENDERECO_CLINICA}

────────────────────────────────────
💡 *RECOMENDAÇÕES IMPORTANTES:*
────────────────────────────────────
1️⃣ Solicitamos que chegue com *15 minutos de antecedência*.
2️⃣ Traga um documento oficial com foto e carteirinha do convênio (caso possua).
3️⃣ Se você tiver exames laboratoriais ou de imagem recentes, lembre-se de trazê-los!
4️⃣ Caso precise reagendar ou cancelar, pedimos a gentileza de nos avisar com antecedência pelo telefone *{TELEFONE_CLINICA}*.

Estamos à sua inteira disposição para melhor atendê-lo(a). Desejamos um excelente dia e até breve! 💙✨

*{NOME_CLINICA}*
_Tecnologia & Humanização a serviço da sua saúde._"""

    return mensagem


# =============================================================================
# MÓDULO DE DADOS E PERSISTÊNCIA EM JSON (RESPONSABILIDADE DO ALUNO B)
# =============================================================================

CAMPOS_OBRIGATORIOS: set = {"id", "paciente", "telefone", "especialidade", "medico", "data", "horario"}


def validar_estrutura_agendamento(agendamento: Dict[str, Any]) -> bool:
    """
    Valida se um registro de agendamento cumpre o contrato de dados (schema).
    Garante a integridade dos dados lidos ou salvos no JSON.
    
    Args:
        agendamento: Dicionário contendo os dados do agendamento.
        
    Returns:
        bool: True se o schema for válido, False caso contrário.
    """
    if not isinstance(agendamento, dict):
        return False
    return CAMPOS_OBRIGATORIOS.issubset(agendamento.keys())


def criar_backup_seguranca(caminho_arquivo: str = ARQUIVO_BANCO) -> bool:
    """
    Cria uma cópia de segurança preventiva da base de dados antes de operações críticas.
    
    Args:
        caminho_arquivo: Caminho do arquivo JSON a ser protegido.
        
    Returns:
        bool: True se o backup foi criado ou se o arquivo ainda não existia.
    """
    if not os.path.exists(caminho_arquivo):
        return True
    try:
        caminho_backup = f"{caminho_arquivo}.bak"
        with open(caminho_arquivo, "r", encoding="utf-8") as origem:
            conteudo = origem.read()
        with open(caminho_backup, "w", encoding="utf-8") as destino:
            destino.write(conteudo)
        return True
    except OSError as err:
        print(f"\n{Cores.AMARELO}⚠️  [Aviso de Backup]: Não foi possível criar snapshot de segurança: {err}{Cores.RESET}")
        return False


def carregar_agendamentos(caminho_arquivo: str = ARQUIVO_BANCO) -> List[Dict[str, Any]]:
    """
    Lê o arquivo JSON com a base de agendamentos e retorna uma lista de dicionários.
    Implementa tratamento preventivo contra arquivos ausentes, vazios ou corrompidos,
    além de higienização de integridade dos registros.
    
    Prompt Original Aluno B:
    "Crie duas funções em Python: uma para salvar uma lista de agendamentos em um
    arquivo chamado agendamentos.json e outra para ler esse arquivo ao iniciar o
    programa, usando o módulo json e tratamento de erros try/except."
    
    Args:
        caminho_arquivo: Caminho do arquivo JSON no disco.
        
    Returns:
        List[Dict[str, Any]]: Lista de agendamentos válidos cadastrados.
    """
    if not os.path.exists(caminho_arquivo):
        # Se não existe, inicializa um arquivo vazio seguro
        salvar_agendamentos([], caminho_arquivo)
        return []

    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return []
            dados = json.loads(conteudo)
            
            if not isinstance(dados, list):
                print(f"\n{Cores.VERMELHO}⚠️  [Aviso]: Base de dados em formato incorreto. Reiniciando.{Cores.RESET}")
                return []

            # Sanitização e validação de schema de cada registro
            agendamentos_validos = [
                ag for ag in dados if validar_estrutura_agendamento(ag)
            ]
            return agendamentos_validos

    except json.JSONDecodeError as err_json:
        print(f"\n{Cores.VERMELHO}⚠️  [Erro de Parse JSON]: O arquivo '{caminho_arquivo}' continha sintaxe inválida ({err_json}).{Cores.RESET}")
        print(f"{Cores.CINZA}Criando arquivo de contingência e reiniciando base limpa.{Cores.RESET}")
        try:
            os.rename(caminho_arquivo, f"{caminho_arquivo}.corrompido.bak")
        except OSError:
            pass
        salvar_agendamentos([], caminho_arquivo)
        return []
    except PermissionError:
        print(f"\n{Cores.VERMELHO}❌ [Permissão Negada]: Sem permissão de leitura para '{caminho_arquivo}'.{Cores.RESET}")
        return []
    except Exception as e:
        print(f"\n{Cores.VERMELHO}⚠️  [Erro Inesperado de Leitura]: Falha ao acessar {caminho_arquivo}: {e}{Cores.RESET}")
        return []


def salvar_agendamentos(agendamentos: List[Dict[str, Any]], caminho_arquivo: str = ARQUIVO_BANCO) -> bool:
    """
    Grava a lista de agendamentos de forma persistente e segura no arquivo JSON,
    com suporte a criação de backup prévio e formatação legível (indent=4).
    
    Args:
        agendamentos: Lista com os dicionários de agendamento a persistir.
        caminho_arquivo: Caminho do arquivo JSON no disco.
        
    Returns:
        bool: True caso tenha salvo com sucesso, False em caso de falha.
    """
    # Cria cópia de segurança antes de sobrescrever
    criar_backup_seguranca(caminho_arquivo)

    try:
        with open(caminho_arquivo, mode="w", encoding="utf-8") as f:
            json.dump(agendamentos, f, indent=4, ensure_ascii=False)
        return True
    except PermissionError:
        print(f"\n{Cores.VERMELHO}❌ [Erro de Permissão]: Sem permissão de escrita no arquivo '{caminho_arquivo}'.{Cores.RESET}")
        return False
    except OSError as err_io:
        print(f"\n{Cores.VERMELHO}❌ [Erro de Disco/IO]: Falha ao gravar dados em '{caminho_arquivo}': {err_io}{Cores.RESET}")
        return False
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ [Erro Crítico de Gravação]: Não foi possível salvar os dados: {e}{Cores.RESET}")
        return False


def excluir_agendamento(agendamentos: List[Dict[str, Any]], id_alvo: int, caminho_arquivo: str = ARQUIVO_BANCO) -> bool:
    """
    Remove um agendamento da lista pelo seu ID numérico e persiste imediatamente
    a exclusão no arquivo JSON.
    
    Args:
        agendamentos: Lista atual de agendamentos em memória.
        id_alvo: ID do agendamento que se deseja remover.
        caminho_arquivo: Caminho do arquivo JSON no disco.
        
    Returns:
        bool: True se o item foi encontrado e excluído com sucesso, False caso contrário.
    """
    for index, ag in enumerate(agendamentos):
        if ag.get("id") == id_alvo:
            agendamentos.pop(index)
            return salvar_agendamentos(agendamentos, caminho_arquivo)
    return False


def buscar_agendamento_por_id(agendamentos: List[Dict[str, Any]], id_alvo: int) -> Optional[Dict[str, Any]]:
    """
    Recupera um agendamento específico da lista a partir do seu ID.
    
    Args:
        agendamentos: Lista de agendamentos.
        id_alvo: ID numérico buscado.
        
    Returns:
        Optional[Dict[str, Any]]: Dicionário do agendamento ou None se não existir.
    """
    for ag in agendamentos:
        if ag.get("id") == id_alvo:
            return ag
    return None


# =============================================================================
# FLUXOS DE NEGÓCIO E CASOS DE USO (INTEGRAÇÃO E UX)
# =============================================================================

def verificar_conflito_horario(agendamentos: List[Dict[str, Any]], medico: str, data: str, horario: str) -> bool:
    """
    Verifica se já existe agendamento marcado para o mesmo médico no mesmo dia e horário.
    Evita sobreposição de consultas (Boa prática sênior de validação de negócio).
    """
    for ag in agendamentos:
        if ag.get("medico") == medico and ag.get("data") == data and ag.get("horario") == horario:
            return True
    return False


def obter_proximo_id(agendamentos: List[Dict[str, Any]]) -> int:
    """Gera o próximo ID sequencial seguro para novos agendamentos."""
    if not agendamentos:
        return 1
    maior_id = max(ag.get("id", 0) for ag in agendamentos)
    return maior_id + 1


def fluxo_agendar_consulta(agendamentos: List[Dict[str, Any]]) -> None:
    """Fluxo interativo de cadastro de nova consulta médica com validações passo a passo."""
    limpar_tela()
    exibir_cabecalho("Novo Agendamento de Consulta")
    print(f"{Cores.CINZA}(Dica: A qualquer momento digite '0' para cancelar e retornar ao menu){Cores.RESET}\n")

    # 1. Nome do Paciente
    paciente = obter_texto_valido(f"{Cores.CIANO}👤 Nome completo do paciente: {Cores.RESET}", tamanho_minimo=3)
    if not paciente:
        return

    # 2. Telefone / WhatsApp
    telefone = obter_telefone_valido(f"{Cores.CIANO}📱 Telefone / WhatsApp com DDD (Ex: 11987654321): {Cores.RESET}")
    if not telefone:
        return

    # 3. Especialidade e Médico
    escolha_medica = selecionar_especialidade()
    if not escolha_medica:
        return

    especialidade = escolha_medica["especialidade"]
    medico = escolha_medica["medico"]

    # 4. Data da Consulta
    print(f"\n{Cores.NEGRITO}📅 Seleção de Data e Horário:{Cores.RESET}")
    data = obter_data_valida(f"{Cores.CIANO}Data da consulta (DD/MM/AAAA): {Cores.RESET}")
    if not data:
        return

    # 5. Horário da Consulta com verificação de disponibilidade
    while True:
        horario = obter_horario_valido(f"{Cores.CIANO}Horário da consulta (07:00 às 19:00): {Cores.RESET}")
        if not horario:
            return

        if verificar_conflito_horario(agendamentos, medico, data, horario):
            print(f"\n{Cores.VERMELHO}⚠️  [Conflito de Horário]: O {medico} já possui consulta marcada em {data} às {horario}!{Cores.RESET}")
            print(f"{Cores.CINZA}Por favor, escolha outro horário ou outra data.{Cores.RESET}\n")
            continue
        break

    # 6. Observações ou Sintomas
    try:
        obs = input(f"{Cores.CIANO}📝 Observações/Sintomas (opcional - pressione ENTER para pular): {Cores.RESET}").strip()
        if not obs:
            obs = "Consulta de rotina / Não especificado"
    except (KeyboardInterrupt, EOFError):
        obs = "Consulta de rotina / Não especificado"

    # Resumo para confirmação
    print(f"\n{Cores.NEGRITO}┌{'─' * 62}┐{Cores.RESET}")
    print(f"{Cores.NEGRITO}│ {Cores.VERDE}🔍 CONFIRMAÇÃO DOS DADOS DO AGENDAMENTO{Cores.RESET}{' ' * 23}{Cores.NEGRITO}│{Cores.RESET}")
    print(f"{Cores.NEGRITO}├{'─' * 62}┤{Cores.RESET}")
    print(f"│ 👤 Paciente:      {paciente:<43} │")
    print(f"│ 📱 Telefone:      {telefone:<43} │")
    print(f"│ 🩺 Especialidade: {especialidade:<43} │")
    print(f"│ 👨‍⚕️ Médico:        {medico:<43} │")
    print(f"│ 📅 Data/Hora:     {data} às {horario:<33} │")
    print(f"│ 📝 Sintomas:      {obs[:40]:<43} │")
    print(f"{Cores.NEGRITO}└{'─' * 62}┘{Cores.RESET}")

    confirmacao = input(f"\n{Cores.AMARELO}❓ Confirmar agendamento desta consulta? (S/N): {Cores.RESET}").strip().upper()
    if confirmacao != "S":
        print(f"\n{Cores.VERMELHO}❌ Agendamento cancelado pelo usuário.{Cores.RESET}")
        pausar()
        return

    # Criação do objeto de agendamento
    novo_agendamento: Dict[str, Any] = {
        "id": obter_proximo_id(agendamentos),
        "paciente": paciente,
        "telefone": telefone,
        "especialidade": especialidade,
        "medico": medico,
        "data": data,
        "horario": horario,
        "observacoes": obs,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "status": "Confirmada",
    }

    agendamentos.append(novo_agendamento)
    if salvar_agendamentos(agendamentos):
        print(f"\n{Cores.VERDE}✅ SUCESSO! Consulta #{novo_agendamento['id']} agendada e salva com sucesso!{Cores.RESET}")
        
        # Pergunta de UX se deseja visualizar a mensagem do WhatsApp imediatamente
        ver_msg = input(f"\n{Cores.CIANO}Deseja gerar e visualizar a mensagem para WhatsApp agora? (S/N): {Cores.RESET}").strip().upper()
        if ver_msg == "S":
            limpar_tela()
            exibir_cabecalho(f"Mensagem WhatsApp - Consulta #{novo_agendamento['id']}")
            print(f"{Cores.VERDE}Copie e envie para o paciente no WhatsApp:{Cores.RESET}\n")
            print(f"{Cores.CINZA}{'-' * 66}{Cores.RESET}")
            print(gerar_mensagem_whatsapp(novo_agendamento))
            print(f"{Cores.CINZA}{'-' * 66}{Cores.RESET}")
    pausar()


def fluxo_listar_consultas(agendamentos: List[Dict[str, Any]]) -> None:
    """Exibe todas as consultas cadastradas em formato de tabela elegante."""
    limpar_tela()
    exibir_cabecalho("Relação de Consultas Agendadas")

    if not agendamentos:
        print(f"\n{Cores.AMARELO}ℹ️  Nenhuma consulta cadastrada no momento.{Cores.RESET}")
        print(f"{Cores.CINZA}Utilize a opção [1] do menu para agendar sua primeira consulta.{Cores.RESET}")
        pausar()
        return

    print(f"\n{Cores.NEGRITO}Total de consultas registradas: {len(agendamentos)}{Cores.RESET}\n")
    print(f"{Cores.CIANO}{'ID':<4} | {'DATA/HORA':<17} | {'PACIENTE':<20} | {'MÉDICO / ESPECIALIDADE':<30} | {'STATUS'}{Cores.RESET}")
    print(f"{'-' * 85}")

    for ag in agendamentos:
        id_str = f"#{ag.get('id', 0)}"
        data_hora = f"{ag.get('data', '')} {ag.get('horario', '')}"
        paciente = ag.get("paciente", "N/A")[:19]
        espec = f"{ag.get('especialidade', '')}"[:28]
        status = ag.get("status", "Agendada")
        
        cor_status = Cores.VERDE if status == "Confirmada" else Cores.AMARELO
        print(f"{id_str:<4} | {data_hora:<17} | {paciente:<20} | {espec:<30} | {cor_status}{status}{Cores.RESET}")

    print(f"{'-' * 85}")
    pausar()


def fluxo_buscar_consultas(agendamentos: List[Dict[str, Any]]) -> None:
    """Permite buscar consultas por nome de paciente, médico ou especialidade."""
    limpar_tela()
    exibir_cabecalho("Pesquisa Inteligente de Consultas")

    if not agendamentos:
        print(f"\n{Cores.AMARELO}ℹ️  Não existem consultas cadastradas para realizar buscas.{Cores.RESET}")
        pausar()
        return

    termo = input(f"{Cores.CIANO}🔍 Digite o nome do paciente, médico ou especialidade (ou '0' para voltar): {Cores.RESET}").strip().lower()
    if not termo or termo == "0":
        return

    encontrados = [
        ag for ag in agendamentos
        if termo in ag.get("paciente", "").lower()
        or termo in ag.get("medico", "").lower()
        or termo in ag.get("especialidade", "").lower()
    ]

    if not encontrados:
        print(f"\n{Cores.VERMELHO}❌ Nenhum agendamento encontrado para o termo: '{termo}'.{Cores.RESET}")
    else:
        print(f"\n{Cores.VERDE}✅ {len(encontrados)} agendamento(s) localizado(s):{Cores.RESET}\n")
        for ag in encontrados:
            print(f"{Cores.NEGRITO}• #{ag.get('id')} - {ag.get('paciente')} | {ag.get('data')} às {ag.get('horario')}{Cores.RESET}")
            print(f"  Médico: {ag.get('medico')} ({ag.get('especialidade')})")
            print(f"  Telefone: {ag.get('telefone')} | Status: {ag.get('status')}")
            print(f"  Obs: {ag.get('observacoes')}")
            print(f"{Cores.CINZA}{'-' * 60}{Cores.RESET}")

    pausar()


def fluxo_gerar_mensagem_whatsapp(agendamentos: List[Dict[str, Any]]) -> None:
    """Permite ao atendente selecionar uma consulta para gerar a mensagem de WhatsApp."""
    limpar_tela()
    exibir_cabecalho("Geração de Mensagem de Confirmação (WhatsApp)")

    if not agendamentos:
        print(f"\n{Cores.AMARELO}ℹ️  Não há consultas cadastradas.{Cores.RESET}")
        pausar()
        return

    print(f"{Cores.NEGRITO}Consultas disponíveis:{Cores.RESET}")
    for ag in agendamentos:
        print(f"  [{ag.get('id')}] Paciente: {ag.get('paciente')} - {ag.get('data')} às {ag.get('horario')} ({ag.get('especialidade')})")

    try:
        entrada = input(f"\n{Cores.CIANO}👉 Digite o número do ID da consulta desejada (ou '0' para voltar): {Cores.RESET}").strip()
        if entrada == "0":
            return
        
        id_selecionado = int(entrada)
        agendamento = next((ag for ag in agendamentos if ag.get("id") == id_selecionado), None)

        if not agendamento:
            print(f"\n{Cores.VERMELHO}⚠️  Nenhum agendamento encontrado com o ID #{id_selecionado}.{Cores.RESET}")
            pausar()
            return

        limpar_tela()
        exibir_cabecalho(f"Mensagem Gerada - Paciente: {agendamento.get('paciente')}")
        print(f"{Cores.VERDE}Copie o texto formatado abaixo para enviar via WhatsApp:{Cores.RESET}\n")
        print(f"{Cores.CINZA}{'=' * 66}{Cores.RESET}")
        print(gerar_mensagem_whatsapp(agendamento))
        print(f"{Cores.CINZA}{'=' * 66}{Cores.RESET}")
        pausar()
    except ValueError:
        print(f"\n{Cores.VERMELHO}⚠️  [Erro]: Digite apenas o número de ID válido.{Cores.RESET}")
        pausar()
    except (KeyboardInterrupt, EOFError):
        return


def fluxo_cancelar_consulta(agendamentos: List[Dict[str, Any]]) -> None:
    """Permite ao usuário cancelar e remover um agendamento do banco com dupla confirmação."""
    limpar_tela()
    exibir_cabecalho("Cancelamento de Consulta")

    if not agendamentos:
        print(f"\n{Cores.AMARELO}ℹ️  Não existem consultas registradas para cancelar.{Cores.RESET}")
        pausar()
        return

    print(f"{Cores.NEGRITO}Consultas ativas:{Cores.RESET}")
    for ag in agendamentos:
        print(f"  [{ag.get('id')}] {ag.get('paciente')} - {ag.get('especialidade')} ({ag.get('data')} às {ag.get('horario')})")

    try:
        entrada = input(f"\n{Cores.VERMELHO}👉 Digite o ID da consulta que deseja CANCELAR (ou '0' para voltar): {Cores.RESET}").strip()
        if entrada == "0":
            return

        id_selecionado = int(entrada)
        agendamento = next((ag for ag in agendamentos if ag.get("id") == id_selecionado), None)

        if not agendamento:
            print(f"\n{Cores.VERMELHO}⚠️  Nenhum agendamento encontrado com o ID #{id_selecionado}.{Cores.RESET}")
            pausar()
            return

        print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO: Você está prestes a remover o agendamento de:{Cores.RESET}")
        print(f"   Paciente: {agendamento.get('paciente')}")
        print(f"   Médico:   {agendamento.get('medico')}")
        print(f"   Data:     {agendamento.get('data')} às {agendamento.get('horario')}")

        certeza = input(f"\n{Cores.VERMELHO}Tem certeza que deseja cancelar esta consulta? (S/N): {Cores.RESET}").strip().upper()
        if certeza == "S":
            if excluir_agendamento(agendamentos, id_selecionado):
                print(f"\n{Cores.VERDE}✅ Consulta #{id_selecionado} cancelada e removida com sucesso!{Cores.RESET}")
            else:
                print(f"\n{Cores.VERMELHO}❌ Falha ao excluir consulta do arquivo.{Cores.RESET}")
        else:
            print(f"\n{Cores.CINZA}Operação de cancelamento abortada.{Cores.RESET}")

        pausar()
    except ValueError:
        print(f"\n{Cores.VERMELHO}⚠️  [Erro]: Digite um ID numérico válido.{Cores.RESET}")
        pausar()
    except (KeyboardInterrupt, EOFError):
        return


# =============================================================================
# PONTO DE ENTRADA PRINCIPAL DA APLICAÇÃO (MAIN)
# =============================================================================

def main() -> None:
    """
    Fluxo principal de controle do sistema de agendamento médico.
    Carrega os dados persistidos, executa o loop do menu e trata interrupções
    inesperadas para garantir que a aplicação nunca encerre abruptamente com erro.
    """
    try:
        # Inicializa o carregamento dos agendamentos (Módulo Aluno B)
        agendamentos = carregar_agendamentos(ARQUIVO_BANCO)

        while True:
            # Apresenta o menu validado (Módulo Aluno A)
            opcao = exibir_menu()

            if opcao == "1":
                fluxo_agendar_consulta(agendamentos)
            elif opcao == "2":
                fluxo_listar_consultas(agendamentos)
            elif opcao == "3":
                fluxo_buscar_consultas(agendamentos)
            elif opcao == "4":
                fluxo_gerar_mensagem_whatsapp(agendamentos)
            elif opcao == "5":
                fluxo_cancelar_consulta(agendamentos)
            elif opcao == "0":
                limpar_tela()
                exibir_cabecalho("Encerrando Aplicação")
                print(f"\n{Cores.VERDE}Obrigado por utilizar o Sistema de Agendamento Inteligente! 👋{Cores.RESET}")
                print(f"{Cores.CINZA}Todos os dados foram preservados em '{ARQUIVO_BANCO}'. Até logo!{Cores.RESET}\n")
                sys.exit(0)

    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{Cores.AMARELO}Encerrando aplicação com segurança... Até logo!{Cores.RESET}\n")
        sys.exit(0)
    except Exception as erro_inesperado:
        print(f"\n{Cores.VERMELHO}❌ Ocorreu um erro imprevisto: {erro_inesperado}{Cores.RESET}")
        print(f"{Cores.CINZA}Os dados existentes permanecem salvos em segurança.{Cores.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
