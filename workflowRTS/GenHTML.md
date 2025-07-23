You are an expert Phaser.js game developer. Your final task is to take all the previously generated Phaser.js game code (including game overview, game logic) and integrate it into a single, **self-contained HTML file**.

---

**Game Overview:**
{overview}
---

**Game Logic Code:**
{code}

---

**Game Modified Code:**
{ecode}

---

**Game Modified Code2:**
{rcode}

---

**Game Modified Code3:**
{tcode}

---

**Code Integration Requirements:**

Based on all the information provided above (Game Overview, Entity Definitions, Rules, and Terminations), generate a single, **self-contained HTML file** that contains the complete Phaser.js game.

This HTML file must adhere to the following:

1.  **Single File:** The entire game, including HTML structure, CSS styling (if any is needed for the UI, keep it minimal and embedded), and **all JavaScript (Phaser.js game code)**, must be contained within this one HTML file.
2.  **No External Files:** Do not link to any external JavaScript files (e.g., `<script src="game.js"></script>`) or external CSS files. All necessary Phaser.js library code should also be included directly within the `<script>` tags, preferably by loading the full Phaser.js library from a CDN link directly in the HTML.
3.  **Functional Game:** The generated HTML file, when opened in a web browser, should immediately run the full Phaser.js RTS game with all the previously specified functionalities:
    * Entity health and resources.
    * Interactive player-controlled buildings (Base for Workers, Barracks for Military Units) with menus and resource costs.
    * Unit movement control.
    * Unit spawning function.
    * Automated combat between opposing units and units attacking enemy buildings.
    * Unit destruction upon reaching 0 health.
    * Game termination logic (victory/defeat conditions).
    * Game Over UI displaying victory/defeat messages.
    * A "Play Again" button on the Game Over UI that restarts the game.
4.  **Phaser.js CDN:** Ensure the Phaser.js library is loaded using a CDN link within the HTML `<script>` tags (e.g., `https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.min.js`).
5.  **Clear Structure:** The HTML, CSS (if any), and JavaScript sections should be well-organized within the single file. The JavaScript code should be placed within `<script>` tags, typically before the closing `</body>` tag.
6.  **Comments:** Maintain clear and concise comments within the JavaScript code to explain different sections and functionalities.
7. **Replace Const Values:** Change all top-level variables within <script> tags from const or let to var to prevent errors during repeated code execution.

The output should be the complete HTML file content.