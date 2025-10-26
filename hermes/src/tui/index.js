// minimal viable text ui lib to have folds

const readline = require('readline');

// Model structure:
// {
//   items: [
//     {
//       id: string,
//       content: string,
//       folded: boolean,
//       foldedContent: string
//     }
//   ],
//   selectedIndex: number
// }

// Messages:
// { type: 'move_up' }
// { type: 'move_down' }
// { type: 'toggle_fold' }
// { type: 'quit' }

export function init(initialItems) {
  const model = {
    items: initialItems.map(item => ({
      ...item,
      folded: true
    })),
    selectedIndex: 0
  };
  return [model, null];
}

export function update(model, msg) {
  switch (msg.type) {
    case 'move_up':
      if (model.selectedIndex > 0) {
        model.selectedIndex--;
      }
      return [model, null];
    case 'move_down':
      if (model.selectedIndex < model.items.length - 1) {
        model.selectedIndex++;
      }
      return [model, null];
    case 'toggle_fold':
      const item = model.items[model.selectedIndex];
      item.folded = !item.folded;
      return [model, null];
    case 'quit':
      return [model, null];
    default:
      return [model, null];
  }
}

export function view(model) {
  let output = '';
  for (let i = 0; i < model.items.length; i++) {
    const item = model.items[i];
    const prefix = i === model.selectedIndex ? '> ' : '  ';
    const foldIndicator = item.folded ? '▶ ' : '▼ ';
    const content = item.folded ? item.foldedContent : item.content;
    output += prefix + foldIndicator + content + '\n';
  }
  output += '\nUse ↑↓ to navigate, space to toggle fold, q to quit\n';
  return output;
}

export function run(initialModel, updateFn, viewFn) {
  let model = initialModel;
  let quit = false;

  process.stdin.setRawMode(true);
  process.stdin.resume();

  // Initial render
  process.stdout.write('\u001b[2J\u001b[0;0H'); // Clear screen
  process.stdout.write(viewFn(model));

  process.stdin.on('data', (key) => {
    if (quit) return;

    let msg;
    if (key.length === 3 && key[0] === 27 && key[1] === 91) {
      if (key[2] === 65) { // Up arrow
        msg = { type: 'move_up' };
      } else if (key[2] === 66) { // Down arrow
        msg = { type: 'move_down' };
      }
    } else if (key[0] === 32) { // Space
      msg = { type: 'toggle_fold' };
    } else if (key[0] === 113 || key[0] === 81) { // 'q' or 'Q'
      msg = { type: 'quit' };
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
        process.stdout.write('\u001b[2J\u001b[0;0H'); // Clear screen
        process.stdout.write(viewFn(model));
      } else {
        process.stdin.setRawMode(false);
        process.stdin.pause();
        // Exit the loop
      }
    }
  });
}
