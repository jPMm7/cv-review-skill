# CV Review & ATS Auditor Skill (`cv-review`)

Uma **Agent Skill** aberta (compatível com o padrão [`agentskills.io`](https://agentskills.io)) para avaliar currículos de **0 a 100** em 8 secções e sub-métricas, detetar armadilhas reais de **ATS/OCR em PDFs**, sugerir correções práticas **"Antes → Depois"**, verificar alinhamentos visuais e recomendar o **Top 5 de Job Positions** mais enquadrados com o CV.

Compatível com **Antigravity**, **Claude Code**, **Codex CLI**, **Gemini CLI**, **Cursor**, **OpenClaw**, **Grok Build / Grok Bot** e qualquer agente que suporte `SKILL.md` (ou via `npx skills add`).

---

## O que esta Skill faz

1. **Score Global & Avaliação por Secção (0–100):**
   - Avalia **Header & Contactos (8%)**, **Summary (12%)**, **Technical Skills (15%)**, **Experience (20%)**, **Projects & Competitions (18%)**, **Education (10%)**, **Languages & Volunteering (7%)** e **Design, Geometria & ATS (10%)**.
   - Nunca inventa métricas nem inflaciona notas: usa placeholders (`[X ms]`, `[Y%]`) onde faltam números reais.
2. **Auditoria Forense de PDF / ATS (`scripts/audit_pdf_ats.py`):**
   - Script Python **sem dependências externas** (apenas *stdlib*) que verifica:
     - Dimensões reais da página (**A4** vs **US Letter** vs **A3** — apanha armadilhas como canvas A3 disfarçado de A4).
     - Links clicáveis `/URI` embutidos no PDF (e se o texto visível mostra o URL completo).
     - Se o PDF é *Tagged* (`/StructTreeRoot`) e se a ordem de leitura difere do *stream* bruto.
     - Sinais de **texto escondido / white-fonting** (fontes `< 4pt`, opacidade `0` perto de texto, `Tr 3`, preenchimento branco antes de texto).
     - Títulos espaçados (`E X P E R I E N C E`) e palavras partidas por hifenização (`Pre-cision`, `intern-ship`).
3. **Top 5 Job Positions:**
   - Lista os 5 cargos com maior probabilidade real de entrevista com base em evidências observadas no CV, separando **Fit Atual %** de **Fit Potencial %**.
4. **Modo Reavaliação & Edição Segura no Canva:**
   - Permite pedir reavaliações com evolução (`Antes → Depois`) e, quando ligada ao MCP do Canva, prepara rascunhos com pré-visualização antes de gravar qualquer alteração (sem Canva MCP, analisa normalmente PDFs/PNGs exportados do Canva).

---

## Plataformas Suportadas & Caminhos de Instalação

| Agente / Plataforma | Caminho Global | Caminho por Projeto |
| :--- | :--- | :--- |
| **Antigravity** | `~/.gemini/config/skills/cv-review` | `.agents/skills/cv-review` |
| **Claude Code** | `~/.claude/skills/cv-review` | `.claude/skills/cv-review` |
| **Codex CLI / AgentSkills Standard** | `~/.agents/skills/cv-review` | `.agents/skills/cv-review` |
| **Gemini CLI** | `~/.gemini/skills/cv-review` | `.gemini/skills/cv-review` |
| **Cursor** | `~/.cursor/skills/cv-review` | `.cursor/skills/cv-review` |
| **OpenClaw** | `~/.openclaw/skills/cv-review` | `skills/cv-review` |
| **Grok Build / Grok Bot** | `~/.grok/skills/cv-review` | `.grok/skills/cv-review` |

---

## Como Instalar (1 Comando)

### Opção 1 — Via `npx skills add` (Universal — qualquer agente!)
Se tiveres Node.js instalado, o CLI oficial do ecossistema [`skills.sh`](https://skills.sh) instala diretamente do GitHub no agente que escolheres:

```bash
npx skills add jPMm7/cv-review-skill
```
*(Ou filtrando por agente, ex.: `npx skills add jPMm7/cv-review-skill -a claude-code -a codex -a cursor`.)*

### Opção 2 — Via `git clone` + Script Multi-Agente (sem Node.js)
```bash
git clone https://github.com/jPMm7/cv-review-skill.git
cd cv-review-skill
```

* **Windows (PowerShell):**
  ```powershell
  # Deteta automaticamente todos os agentes instalados no teu PC:
  .\install.ps1

  # Ou instala em TODOS os agentes suportados:
  .\install.ps1 -All

  # Ou escolhe agentes específicos:
  .\install.ps1 -Agents claude,codex,grok,cursor
  ```

* **macOS / Linux:**
  ```bash
  chmod +x install.sh

  # Deteta automaticamente todos os agentes instalados:
  ./install.sh

  # Ou instala em TODOS os agentes suportados:
  ./install.sh --all

  # Ou escolhe agentes específicos:
  ./install.sh --agent claude,codex,grok,openclaw
  ```

### Opção 3 — Abrir como Workspace / Chat Web
* **Antigravity / Codex / Cursor:** Basta abrir esta pasta (`cv-review-skill`) diretamente — `.agents/skills/cv-review/` é carregada automaticamente.
* **Chat Web (Gemini / ChatGPT / Claude):** Anexa `.agents/skills/cv-review/SKILL.md` + `references/scoring-rubric.md` + `references/ats-and-visual-checks.md` junto com o PDF do teu CV.

---

## Estrutura da Skill

```text
cv-review-skill/
├── README.md
├── install.ps1                          # Instalador multi-agente Windows
├── install.sh                           # Instalador multi-agente macOS / Linux
└── .agents/
    └── skills/
        └── cv-review/
            ├── SKILL.md                 # Instruções principais (agnósticas ao agente)
            ├── scripts/
            │   └── audit_pdf_ats.py     # Auditor forense de PDF/ATS (zero dependências)
            ├── references/
            │   ├── scoring-rubric.md        # Rubrica detalhada 0-100 e pesos
            │   ├── ats-and-visual-checks.md # Checklist de geometria, OCR e ATS
            │   ├── job-matching-guide.md    # Guia de matching Top 5 Job Positions
            │   └── canva-editing-protocol.md# Protocolo seguro read-only + draft/commit Canva
            └── examples/
                └── sample-report.md     # Formato padrão do relatório
```

---

## Prompts de Exemplo para Usar

* **Avaliar um PDF enviado no chat:**
  > *"Usa a skill cv-review e avalia este CV de 0 a 100 por secções e métricas, verifica armadilhas de ATS e indica-me o Top 5 de job positions."*
* **No Claude Code (invocação direta via slash command):**
  > *`/cv-review avalia este ficheiro cv.pdf e lista o que devo mudar por secção`*
* **Avaliar um CV no Canva (com Canva MCP ligado):**
  > *"Avalia o meu CV no Canva chamado 'O Meu CV' de 0 a 100 por métricas/secções e indica o Top 5 de cargos."*
* **Verificar alinhamento visual / foto:**
  > *"Verifica se o alinhamento da foto, margens e espaçamento deste CV está bom."*
* **Rodar manualmente o auditor de PDF (CLI):**
  ```bash
  python .agents/skills/cv-review/scripts/audit_pdf_ats.py caminho/para/cv.pdf
  ```
