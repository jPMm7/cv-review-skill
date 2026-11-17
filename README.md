# CV Review & ATS Auditor Skill (`cv-review`)

Uma **Agent Skill** completa e estruturada para avaliar currículos de **0 a 100** em 8 secções e sub-métricas, detetar armadilhas reais de **ATS/OCR em PDFs**, sugerir correções práticas **"Antes → Depois"**, verificar alinhamentos visuais e recomendar o **Top 5 de Job Positions** mais enquadrados com o CV.

Funciona com **PDFs**, **imagens/screenshots**, **texto/LaTeX/Markdown**, **Google Docs** e **designs do Canva** (via Canva MCP).

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
     - Sinais de **texto escondido / white-fonting** (fontes `< 4pt`, opacidade `0`, `Tr 3`, preenchimento branco antes de texto).
     - Títulos espaçados (`E X P E R I E N C E`) e palavras partidas por hifenização (`Pre-cision`, `intern-ship`).
3. **Top 5 Job Positions:**
   - Lista os 5 cargos com maior probabilidade real de entrevista com base em evidências observadas no CV, separando **Fit Atual %** de **Fit Potencial %**.
4. **Modo Reavaliação & Edição Segura no Canva:**
   - Permite pedir reavaliações com evolução (`Antes → Depois`) e, quando ligada ao MCP do Canva, prepara rascunhos com pré-visualização antes de gravar qualquer alteração.

---

## Estrutura da Skill

```text
cv-review-skill/
├── README.md
├── install.ps1                          # Instalador 1-clique para Windows
├── install.sh                           # Instalador 1-clique para macOS / Linux
└── .agents/
    └── skills/
        └── cv-review/
            ├── SKILL.md                 # Instruções principais da skill
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

## Como Instalar e Partilhar com Amigos

### Clonar do GitHub
```bash
git clone https://github.com/jPMm7/cv-review-skill.git
cd cv-review-skill
```

### Opção A — Antigravity (Instalação Global — Recomendado)
Depois de instalares globalmente, a skill fica disponível em **qualquer** conversa ou projeto teu.

* **Windows (PowerShell):**
  ```powershell
  .\install.ps1
  ```
* **macOS / Linux:**
  ```bash
  chmod +x install.sh && ./install.sh
  ```
* **Manual:** Copia a pasta `.agents/skills/cv-review/` para:
  * Windows: `%USERPROFILE%\.gemini\config\skills\cv-review\`
  * macOS/Linux: `~/.gemini/config/skills/cv-review/`

### Opção B — Antigravity (Abrir como Workspace)
Basta abrir esta pasta (`cv-review-skill`) como *workspace* no Antigravity — a pasta `.agents/skills/cv-review/` é descoberta automaticamente.

### Opção C — Outros Agentes (Claude Code, Gemini CLI, Codex, Cursor)
A skill segue o formato aberto `SKILL.md` + `references/` + `scripts/`:
* **Claude Code:** copia `.agents/skills/cv-review/` para `~/.claude/skills/cv-review/` (ou `.claude/skills/cv-review/` no teu projeto).
* **Gemini CLI / Codex:** copia `.agents/skills/cv-review/` para a pasta de skills do agente ou `.agents/skills/`.
* **Chat Web (Gemini / ChatGPT / Claude):** anexa `SKILL.md` + `references/scoring-rubric.md` + `references/ats-and-visual-checks.md` juntamente com o PDF do CV.

---

## Prompts de Exemplo para Usar

* **Avaliar um PDF enviado no chat:**
  > *"Usa a skill cv-review e avalia este CV de 0 a 100 por secções e métricas, verifica armadilhas de ATS e indica-me o Top 5 de job positions."*
* **Avaliar um CV no Canva:**
  > *"Avalia o meu CV no Canva chamado 'O Meu CV' de 0 a 100 por métricas/secções e indica o Top 5 de cargos."*
* **Pedir reescrita concreta:**
  > *"Lista o que devo mudar em cada secção com exemplos Antes -> Depois para este CV."*
* **Verificar alinhamento visual / foto:**
  > *"Verifica se o alinhamento da foto, margens e espaçamento deste CV está bom."*
* **Rodar manualmente o auditor de PDF (CLI):**
  ```bash
  python .agents/skills/cv-review/scripts/audit_pdf_ats.py caminho/para/cv.pdf
  ```

---

## Quick Start (English)

1. **Install globally in Antigravity:** run `./install.ps1` (Windows) or `./install.sh` (macOS/Linux), or copy `.agents/skills/cv-review` to `~/.gemini/config/skills/cv-review`.
2. **Or share via Git / ZIP:** anyone opening this folder in Antigravity (or copying `.agents/skills/cv-review` to their agent's `skills/` directory) gets the full 0–100 rubric, zero-dependency PDF ATS auditor (`scripts/audit_pdf_ats.py`), and Top-5 job matcher immediately.
