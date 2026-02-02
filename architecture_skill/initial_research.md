Yes — **there *are* existing tools and skills that can help you automatically generate architecture documentation (including Mermaid diagrams) from a codebase**, which sounds very close to your goal of building a *comprehensive Claude Code skill* for this. Here are the most relevant ones:

---

## 🧠 **1. C4Diagrammer (Open Source)**

* **What it is:** An AI‑powered documentation generator for legacy codebases that walks the directory tree, summarizes code, and generates **C4 architecture diagrams** in **Mermaid.js** format. ([GitHub][1])
* **Key Features:**

  * Generates README documentation for each directory.
  * Produces component and container diagrams via Mermaid. ([GitHub][1])
* **Best for:** Starting points if you want *code‑to‑Mermaid* architectural output you can then use or extend into Claude Code skills.

**GitHub:** C4Diagrammer – AI‑powered doc generator.

---

## 🤖 **2. Swark — VS Code Architecture Diagrams**

* **What it is:** A **VS Code extension** that uses an LLM (via GitHub Copilot) to **automatically create architecture diagrams from code**, **with Mermaid.js output**. ([GitHub][2])
* **How it works:**

  * Scans project files and builds prompts.
  * Sends them to an LLM (Copilot) and outputs Mermaid code.
  * Stores results in a `swark‑output` folder. ([GitHub][2])
* **Why it matters:** This tool already does *code analysis → Mermaid diagram generation* without manual diagram writing — exactly what you want for a Claude Code pipeline.

---

## 🧪 **3. Skill: `design‑doc‑mermaid` (Claude Skill)**

* **What it is:** A **Claude skill** specifically mentioned as generating **Mermaid diagrams and design docs** — including architecture diagrams — and can work with code‑to‑diagram generation logic. ([Claude Code Plugins][3])
* **Capabilities:**

  * Supports activity, deployment, architecture diagrams.
  * Can generate full design documentation with embedded diagrams.
  * Includes Python utilities for diagram extraction and image conversion. ([Claude Code Plugins][3])
* **Best fit for you:** This appears *very close* to what you described: a skill that walks the project, extracts structure, and outputs Mermaid plus documentation.

👉 If this skill matches your intent, you could install/extend it and adapt it to generate SVG/PNG from the Mermaid code.

---

## 🧠 **4. InsightCode (Python Tool + Mermaid)**

* **What it is:** A codebase analysis tool that generates **Mermaid diagram prompts** (flowchart / architecture) and summaries of code. ([GitHub][4])
* **How it helps:**

  * Produces Mermaid prompt text based on static analysis.
  * You can feed that into Claude/LLMs for richer documentation or visualization.
  * It doesn’t render SVGs directly but outputs Mermaid syntax you can render later. ([GitHub][4])

---

## 🛠️ **5. Rendering & Diagram Export Tools**

Once you have Mermaid code (from any tool above), you can convert it to images:

### 🧩 **MassiveDiag**

* **Purpose:** Instantly render Mermaid (and many other formats) to **SVG, PNG, PDF, etc.** from text or AI output. ([Reddit][5])
* Great for pipeline rendering in docs.

### 🧰 **Mermaid CLI / Tools like Oxdraw**

* Mermaid CLI can generate images from `.mmd` Mermaid files via Puppeteer or headless Chromium.
* Tools like **oxdraw** provide CLI support to generate **SVG/PNG/PDF** and allow visual tweaking. ([serverspace.io][6])

---

## 🧠 **Putting It All Together — Example Workflow**

1. **Static Analysis / LLM Parsing**

   * Use *InsightCode* or write a Claude Code skill that walks your codebase.
   * For each module/file, summarize structure and dependencies.

2. **Generate Mermaid Diagrams**

   * Feed the summaries into a prompt template that outputs Mermaid syntax for various diagrams (architecture, flow, dependencies).
   * Optionally reuse or adapt existing skill like `design‑doc‑mermaid`.

3. **Render to Image**

   * Use **MassiveDiag**, **Mermaid CLI**, or **Oxdraw** to produce **SVG/PNG** for documentation export.

4. **Compose Full Docs**

   * Assemble the results into a structured documentation format (Markdown/HTML/PDF) with Mermaid diagram images embedded.

---

## 🧠 **Is There Already a Tool That Does *Everything*?**

Not a single turnkey open tool that:

* Fully walks your project,
* Infers architecture automatically,
* Generates *all kinds* of architecture docs,
* Renders them to images,

*without some setup.* But **several pieces already exist** (above) that you can integrate or wrap into a Claude Code automation pipeline to achieve it.

---

## 🧠 **Recommendations to Proceed**

✅ Explore **C4Diagrammer** and **Swark** for project code‑to‑Mermaid generation. ([GitHub][1])
✅ Try or adapt the **design‑doc‑mermaid Claude skill** as a foundation. ([Claude Code Plugins][3])
✅ Add rendering (MassiveDiag or Mermaid CLI) to get SVG/PNG image output.

---

If you want, I can help you **write a Claude Code skill prompt/template** that systematically walks a codebase and outputs structured architecture documentation with Mermaid diagrams — just tell me your programming language(s) and project stack!

[1]: https://github.com/jonverrier/C4Diagrammer?utm_source=chatgpt.com "GitHub - jonverrier/C4Diagrammer: An AI-Powered documentation generator for legacy codebases"
[2]: https://github.com/swark-io/swark?utm_source=chatgpt.com "GitHub - swark-io/swark: Create architecture diagrams from code automatically using large language models (LLMs)."
[3]: https://claude-plugins.dev/skills/%40SpillwaveSolutions/design-doc-mermaid/SKILL.md?utm_source=chatgpt.com "design-doc-mermaid - Agent Skills"
[4]: https://github.com/MaartenSmeets/insightcode?utm_source=chatgpt.com "GitHub - MaartenSmeets/insightcode: Unlock deep insights into your codebase with intelligent analysis and architecture visualization. Effortlessly summarize complex code, generate high-level system diagrams, and streamline your development workflow. Perfect for developers looking to understand and optimize their projects."
[5]: https://www.reddit.com/r/ClaudeAI/comments/1jl5jmh?utm_source=chatgpt.com "🚀 Claude → Code → Diagram with MassiveDiag (Supports PlantUML, Mermaid, SVG, TikZ & more!)"
[6]: https://serverspace.io/de/support/help/how-to-use-oxdraw-a-visual-editor-for-mermaid-diagrams-with-cli-and-rust-support/?utm_source=chatgpt.com "So verwenden Sie oxdraw: ein visueller Editor für Mermaid-Diagramme mit CLI und Rust-Unterstützung"
