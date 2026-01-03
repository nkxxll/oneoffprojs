
In the `mini.files` module, directory editing is done interactively through text buffers, allowing users to directly modify the filesystem using familiar Neovim editing actions. Below is an overview of how the process of editing directories works within `mini.files`:

### General Workflow
1. **Navigate to Directory to Edit:**
   - Use the file explorer to navigate to the target directory where you want to perform edits.

2. **Edit the Directory Buffer:**
   - In the directory buffer, each filesystem entry (files and directories) is displayed as a line. You can edit these lines to represent the desired changes.
   - Edits are made directly in the buffer using native Neovim commands.

3. **Synchronize Edits:**
   - Once the desired edits are made, execute the `MiniFiles.synchronize()` action (default key: `=`).
   - This will:
     - Parse user edits in directory buffers.
     - Show a confirmation dialog for all the actions to be applied.
     - Apply the changes to the filesystem if confirmed.

---

### Supported Actions
Below are the file system manipulations you can perform by editing the directory buffer:

#### **1. Create**
- Create a file:
  - Add a new line with the desired filename (including an extension, if needed).
- Create a directory:
  - Add a new line with the directory name, followed by a `/`.
- Create files or directories inside nested directories:
  - Use the format `dir/nested-dir/` for directories or `dir/nested-dir/file` for files.

#### **2. Delete**
- To delete a file or directory:
  - Remove the corresponding line from the buffer.

#### **3. Rename**
- To rename a file or directory:
  - Update the name in the buffer (do not change any icons or prefix data to the left of the name).

#### **4. Copy**
- To copy a file or directory:
  - Duplicate its line in the buffer and paste it into the buffer of the target directory.
  - Update the target path if needed, or keep the path to copy within the same parent directory (but with a new name).

#### **5. Move**
- To move a file or directory:
  - Cut the corresponding line and paste it into the buffer of the target directory.
  - Optionally update the name in the target location.

---

### Key Features & Notes on Editing
- **Visualizing Directory Structure:** Buffers show directory entries as lines with a compact and editable format.
- **No Automatic Synchronization:** Buffers do not automatically update to reflect external changes to the filesystem. You must use `MiniFiles.synchronize()` to refresh them.
- **Simulated Changes:** Until synchronization, edits made in a directory buffer only simulate changes—they are not applied to the actual filesystem.
- **Undo-Friendly Workflow:** Multiple edits can be performed, and changes can be reverted before synchronization.

---

### How Synchronization Works
- When `MiniFiles.synchronize()` is executed:
  - Your edits are analyzed to generate a list of actions (create, delete, rename, move, copy).
  - A **confirmation dialog** is shown, summarizing the actions to be applied.
  - You can confirm (`y`/`<CR>`) or cancel (`n`/`<Esc>`) these changes:
    - Confirming will apply the edits to the filesystem and update the buffer.
    - Canceling will refresh the buffer without applying changes.

---

### Limitations
- **No Automatic Tracking of External Changes:**
  - If the filesystem changes externally (e.g., from another program), you need to manually refresh the buffer using `MiniFiles.synchronize()` to see those changes.
  
- **Cyclic Renames Are Not Supported:**
  - Circular renaming like renaming "a" to "b" and "b" to "a" is not allowed.

- **No Editing Prefixes or Metadata:**
  - You must not modify the generated prefixes (icons, path indexes) to the left of each file/directory name.

- **Directory-to-File Conversion:**
  - Appending a trailing `/` to a filename changes it to an empty directory, and vice versa.

---

By combining familiar editing capabilities in Neovim with the flexibility to directly modify the filesystem through a text-based interface, `mini.files` provides a simple yet powerful way to manipulate directories.
