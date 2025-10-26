/**
 * @typedef {Object} Test
 * @property {string} type - type of the test
 * @property {number} testIndex - index of the test
 * @property {object} message - request message
 * @property {object} response - response to the message
 * @property {object} fixture - fixture if available
 */

/**
 * @typedef {Object} Item
 * @property {string} runName - name of the run
 * @property {Test} test - test object
 * @property {string} content - Full content when unfolded
 * @property {boolean} folded - Whether the item is folded
 * @property {string} foldedContent - Preview content when folded
 */

import { saveFixture } from "../fixtures";

/**
 * @typedef {Object} Model
 * @property {Item[]} items - Array of displayable items
 * @property {number} selectedIndex - Index of the currently selected item
 */

/**
 * @typedef {Object} Message
 * @property {string} type - The type of message (e.g., 'move_up', 'toggle_fold', 'quit')
 */

/**
 * @typedef {null|Promise<Message>} Command
 */

/**
 * Initializes the TUI model with the given items, all folded by default.
 * @param {Item[]} initialItems - The initial array of items without folded state
 * @returns {[Model, Command]} The initial model and optional command
 */
export function init(initialItems) {
  const model = {
    items: initialItems.map((item) => ({
      ...item,
      folded: true,
    })),
    selectedIndex: 0,
  };
  return [model, null];
}

/**
 * Updates the model based on the given message.
 * @param {Model} model - The current model state
 * @param {Message} msg - The message to process
 * @returns {[Model, Command]} The updated model and optional command
 */
export function update(model, msg) {
  switch (msg.type) {
    case "save_fixture":
      const currentItem = model.items[model.selectedIndex];
      const name = currentItem.runName;
      const idx = currentItem.testIndex;
      const response = currentItem.test.response;
      saveFixture(name, idx, response);
      return [model, null];
    case "move_up":
      if (model.selectedIndex > 0) {
        model.selectedIndex--;
      }
      return [model, null];
    case "move_down":
      if (model.selectedIndex < model.items.length - 1) {
        model.selectedIndex++;
      }
      return [model, null];
    case "toggle_fold":
      const item = model.items[model.selectedIndex];
      item.folded = !item.folded;
      return [model, null];
    case "quit":
      return [model, null];
    default:
      return [model, null];
  }
}

/**
 * Renders the current model state as a string for terminal output.
 * @param {Model} model - The model to render
 * @returns {string} The rendered output string
 */
export function view(model) {
  let output = "";
  for (let i = 0; i < model.items.length; i++) {
    const item = model.items[i];
    const prefix = i === model.selectedIndex ? "> " : "  ";
    const foldIndicator = item.folded ? "▶ " : "▼ ";
    const content = item.folded ? item.foldedContent : item.content;
    output += prefix + foldIndicator + content + "\n";
  }
  output += "\nUse ↑↓ to navigate, space to toggle fold, q to quit\n";
  return output;
}

/**
 * Runs the TUI application loop, handling user input and rendering.
 * @param {Model} initialModel - The starting model state
 * @param {function(Model, Message): [Model, Command]} updateFn - The update function
 * @param {function(Model): string} viewFn - The view function
 */
export function run(initialModel, updateFn, viewFn) {
  let model = initialModel;
  let quit = false;

  // Handle SIGTERM and SIGINT for graceful exit
  const cleanup = () => {
    process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
    process.stdin.setRawMode(false);
    process.stdin.pause();
    process.exit(0);
  };

  process.on("SIGTERM", cleanup);
  process.on("SIGINT", cleanup);

  process.stdin.setRawMode(true);
  process.stdin.resume();

  // Initial render
  process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
  process.stdout.write(viewFn(model));

  process.stdin.on("data", (key) => {
    if (quit) return;

    let msg;
    // arrow keys have a special utf-16 representation
    if (key.length === 3 && key[0] === 27 && key[1] === 91) {
      if (key[2] === 65) {
        // Up arrow
        msg = { type: "move_up" };
      } else if (key[2] === 66) {
        // Down arrow
        msg = { type: "move_down" };
      }
    } else if (key[0] === "s".charCodeAt(0)) {
      msg = { type: "save_fixture" };
    } else if (key[0] === "j".charCodeAt(0)) {
      msg = { type: "move_down" };
    } else if (key[0] === "k".charCodeAt(0)) {
      msg = { type: "move_up" };
    } else if (key[0] === 32 || key[0] === "l".charCodeAt(0)) {
      // Space
      msg = { type: "toggle_fold" };
    } else if (key[0] === 113 || key[0] === 81 || key[0] === 3) {
      // 'q' or 'Q' or <ctrl-c>
      msg = { type: "quit" };
      quit = true;
    } else {
      return; // Ignore other keys
    }

    if (msg) {
      const [newModel, command] = updateFn(model, msg);
      model = newModel;
      if (command) {
        // Handle command if present (not implemented yet)
      }

      if (!quit) {
        process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
        process.stdout.write(viewFn(model));
      } else {
        process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
        process.stdin.setRawMode(false);
        process.stdin.pause();
      }
    }
  });
}
