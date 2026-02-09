const html = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Font Fitter</title>
    <style>
      :root {
        color-scheme: light;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          sans-serif;
        background: #f6f6f6;
        color: #1c1c1c;
        --bg-primary: #f6f6f6;
        --bg-secondary: #ffffff;
        --text-primary: #1c1c1c;
        --text-secondary: #6d6d6d;
        --border-color: #e2e2e2;
        --border-light: #efefef;
      }

      :root[data-theme="dark"] {
        color-scheme: dark;
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --text-primary: #f0f0f0;
        --text-secondary: #a0a0a0;
        --border-color: #404040;
        --border-light: #333333;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--bg-primary);
        color: var(--text-primary);
      }

      .app {
        min-height: 100vh;
        display: grid;
        grid-template-columns: minmax(280px, 340px) 1fr;
      }

      .controls {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 20px;
      }

      .controls-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
      }

      .controls h1 {
        margin: 0;
        font-size: 20px;
        flex: 1;
      }

      .theme-toggle {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 6px 10px;
        cursor: pointer;
        font-size: 14px;
        color: var(--text-primary);
      }

      .theme-toggle:hover {
        opacity: 0.8;
      }

      .control-group {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-light);
      }

      .control-group:last-of-type {
        border-bottom: none;
      }

      label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--text-primary);
      }

      select,
      input[type="range"] {
        width: 100%;
      }

      select {
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        background: var(--bg-secondary);
        color: var(--text-primary);
        font-size: 14px;
      }

      select option {
        background: var(--bg-secondary);
        color: var(--text-primary);
      }

      input[type="range"] {
        accent-color: #2f7cf6;
      }

      .slider-row {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .slider-value {
        min-width: 48px;
        text-align: right;
        font-variant-numeric: tabular-nums;
        color: var(--text-secondary);
      }

      .preview {
        padding: 40px 60px;
        display: flex;
        flex-direction: column;
        gap: 24px;
        background: var(--bg-primary);
      }

      .preview h2,
      .preview p {
        margin: 0;
        color: var(--text-primary);
      }

      .preview [contenteditable="true"]:focus {
        outline: 2px solid #2f7cf6;
        outline-offset: 4px;
      }

      .hint {
        font-size: 13px;
        color: var(--text-secondary);
      }

      @media (max-width: 900px) {
        .app {
          grid-template-columns: 1fr;
        }

        .controls {
          border-right: none;
          border-bottom: 1px solid var(--border-color);
        }

        .preview {
          padding: 32px;
        }
      }
    </style>
  </head>
  <body>
    <div class="app">
      <aside class="controls">
        <div class="controls-header">
          <h1>Font Fitter</h1>
          <button class="theme-toggle" id="theme-toggle">🌙</button>
        </div>
        <div class="control-group">
          <label for="heading-font">Heading Font</label>
          <select id="heading-font"></select>
          <div class="slider-row">
            <input id="heading-size" type="range" min="32" max="96" step="1" />
            <span id="heading-size-value" class="slider-value">64px</span>
          </div>
        </div>
        <div class="control-group">
          <label for="body-font">Body Font</label>
          <select id="body-font"></select>
          <div class="slider-row">
            <input id="body-size" type="range" min="14" max="32" step="1" />
            <span id="body-size-value" class="slider-value">18px</span>
          </div>
        </div>
        <div class="hint">Tip: click the preview text to edit.</div>
      </aside>
      <main class="preview">
        <h2 id="heading-preview" contenteditable="true">
          A serif statement for the headline
        </h2>
        <p id="body-preview" contenteditable="true">
          This is the body copy. Use the controls to find a comfortable pairing
          between display and supporting text. Adjust the sizes until it feels
          balanced, then keep editing to see how the fonts respond.
        </p>
      </main>
    </div>

    <script type="module">
      const headingFonts = [
        "Playfair Display",
        "Cormorant Garamond",
        "Bodoni Moda",
        "Dancing Script",
        "Great Vibes",
        "Parisienne",
        "Abril Fatface",
        "Crimson Text",
        "Merriweather",
        "Poppins",
        "Raleway",
        "Rubik Mono One",
      ];
      const bodyFonts = [
        "Inter",
        "Roboto",
        "Open Sans",
        "Lato",
        "Montserrat",
        "Nunito",
        "Source Sans Pro",
        "Poppins",
        "Raleway",
        "Ubuntu",
        "Lexend",
        "JetBrains Mono",
      ];

      const headingSelect = document.getElementById("heading-font");
      const bodySelect = document.getElementById("body-font");
      const headingPreview = document.getElementById("heading-preview");
      const bodyPreview = document.getElementById("body-preview");
      const headingSizeInput = document.getElementById("heading-size");
      const bodySizeInput = document.getElementById("body-size");
      const headingSizeValue = document.getElementById("heading-size-value");
      const bodySizeValue = document.getElementById("body-size-value");
      const themeToggle = document.getElementById("theme-toggle");

      const loadedFonts = new Set();

      // Theme management
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const savedTheme = localStorage.getItem("theme");
      const currentTheme = savedTheme || (prefersDark ? "dark" : "light");

      function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        themeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
      }

      setTheme(currentTheme);

      themeToggle.addEventListener("click", () => {
        const newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        setTheme(newTheme);
      });

      function toFontUrl(fontName) {
        const formatted = fontName.trim().replace(/\s+/g, "+");
        return (
          "https://fonts.googleapis.com/css2?family=" +
          formatted +
          "&display=swap"
        );
      }

      function loadFont(fontName) {
        if (loadedFonts.has(fontName)) {
          return;
        }
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = toFontUrl(fontName);
        document.head.appendChild(link);
        loadedFonts.add(fontName);
      }

      function populateSelect(select, fonts) {
        fonts.forEach((font) => {
          const option = document.createElement("option");
          option.value = font;
          option.textContent = font;
          select.appendChild(option);
        });
      }

      function updateFontPreview(target, fontName) {
        loadFont(fontName);
        target.style.fontFamily = '"' + fontName + '", serif';
      }

      function updateSizeValue(label, value) {
        label.textContent = value + "px";
      }

      populateSelect(headingSelect, headingFonts);
      populateSelect(bodySelect, bodyFonts);

      headingSelect.value = headingFonts[0];
      bodySelect.value = bodyFonts[0];
      headingSizeInput.value = "64";
      bodySizeInput.value = "18";

      updateFontPreview(headingPreview, headingSelect.value);
      updateFontPreview(bodyPreview, bodySelect.value);
      headingPreview.style.fontSize = headingSizeInput.value + "px";
      bodyPreview.style.fontSize = bodySizeInput.value + "px";
      updateSizeValue(headingSizeValue, headingSizeInput.value);
      updateSizeValue(bodySizeValue, bodySizeInput.value);

      headingSelect.addEventListener("change", (event) => {
        updateFontPreview(headingPreview, event.target.value);
      });

      bodySelect.addEventListener("change", (event) => {
        updateFontPreview(bodyPreview, event.target.value);
      });

      headingSizeInput.addEventListener("input", (event) => {
        const size = event.target.value;
        headingPreview.style.fontSize = size + "px";
        updateSizeValue(headingSizeValue, size);
      });

      bodySizeInput.addEventListener("input", (event) => {
        const size = event.target.value;
        bodyPreview.style.fontSize = size + "px";
        updateSizeValue(bodySizeValue, size);
      });
    </script>
  </body>
</html>`;

Bun.serve({
  port: 3000,
  fetch() {
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
      },
    });
  },
});

console.log("Font Fitter running at http://localhost:3000");
