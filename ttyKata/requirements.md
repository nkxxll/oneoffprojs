# **Coding Kata Game – MVP Requirements Document**

## **1. Overview**

**Purpose:**
Create a terminal-based application that gamifies coding by measuring **time taken**, **program length**, and **correctness** against predefined inputs and outputs. Users solve programming challenges (katas) stored in a TOML configuration file.

**Scope (MVP):**

1. Launch a user-selected editor to solve a kata.
2. Track **time spent** in the editor.
3. Measure **program length** (lines of code or bytes).
4. Verify the solution against **predefined inputs and expected outputs**.
5. Load kata definitions from a TOML file.
6. Allow the editor to be **interchanged via a flag**.

---

## **2. Functional Requirements**

### **2.1 Kata Management**

* Kata definitions are stored in a **TOML file** (`problems.toml`).
* TOML structure:

```toml
[[problem]]
name = "<kata_name>"
description = "<kata_description>"
inputs = ["path/to/input1.txt", "path/to/input2.txt"]
outputs = ["path/to/output1.txt", "path/to/output2.txt"]
```

* The app must:

  * Load all problems from the TOML file at startup.
  * Display a **list of available problems** to the user.
  * Allow the user to **select a problem** to solve.

---

### **2.2 Editor Launch**

* The app launches a code editor as a **child process** to let the user solve the problem.
* The **editor is configurable** via a command-line flag:

```bash
kata-game --editor=nvim
```

* Default editor can be `$EDITOR`.
* Timer **starts when the editor process launches** and **stops when it exits**.

---

### **2.3 Solution Evaluation**

* After editor exits:

  1. Measure **program length** (bytes or lines of code).
  2. Run the program against **all input files** defined in the kata.
  3. Compare program output to the **corresponding output files**.
* Record:

  * Time taken
  * Program length
  * Correctness (pass/fail for each input-output pair)

---

### **2.4 TUI Interface**

* if there are multiple problems in the toml file you can first choose the problem you want to work on
* the name the description is shown to you you can read it and hit start
* starting starts the editor in a new process that takes over the tty
* when the process stops the finish screen is shown to you you can start a new problem from there restart the current or end
* the start tui interface should also have a recent tries table where you can see your old tries and how long they took
* after a try the time should be saved in another toml file with the results (timestamp, problem, time)
* there should be an option to discard the time

* Display in terminal:

  * Kata name and description
  * Inputs and outputs (paths)
  * Timer status
  * After submission: results (pass/fail, time, program length)

* Must be **terminal-based (TUI)**; can use:

  * **Python**: `prompt_toolkit`, `rich`
  * mvp with prompt_toolkit
  * leaderboard with `rich` table

---
Got it! Based on your description, here’s a **requirements document** tailored for your MVP TUI coding game. I’ve structured it formally so it could guide either Python or Rust development.

---

# **Coding Kata Game – MVP Requirements Document**

## **1. Overview**

**Purpose:**
Create a terminal-based application that gamifies coding by measuring **time taken**, **program length**, and **correctness** against predefined inputs and outputs. Users solve programming challenges (katas) stored in a TOML configuration file.

**Scope (MVP):**

1. Launch a user-selected editor to solve a kata.
2. Track **time spent** in the editor.
3. Measure **program length** (lines of code or bytes).
4. Verify the solution against **predefined inputs and expected outputs**.
5. Load kata definitions from a TOML file.
6. Allow the editor to be **interchanged via a flag**.

---

## **2. Functional Requirements**

### **2.1 Kata Management**

* Kata definitions are stored in a **TOML file** (`problems.toml`).
* TOML structure:

```toml
[[problem]]
name = "<kata_name>"
description = "<kata_description>"
inputs = ["path/to/input1.txt", "path/to/input2.txt"]
outputs = ["path/to/output1.txt", "path/to/output2.txt"]
```

* The app must:

  * Load all problems from the TOML file at startup.
  * Display a **list of available problems** to the user.
  * Allow the user to **select a problem** to solve.

---

### **2.2 Editor Launch**

* The app launches a code editor as a **child process** to let the user solve the problem.
* The **editor is configurable** via a command-line flag:

```bash
kata-game --editor=nvim
```

* Default editor can be `$EDITOR`.
* Timer **starts when the editor process launches** and **stops when it exits**.

---

### **2.3 Solution Evaluation**

* After editor exits:

  1. Measure **program length** (bytes or lines of code).
  2. Run the program against **all input files** defined in the kata.
  3. Compare program output to the **corresponding output files**.
* Record:

  * Time taken
  * Program length
  * Correctness (pass/fail for each input-output pair)

---

### **2.4 TUI Interface**

* Display in terminal:

  * Kata name and description
  * Inputs and outputs (paths)
  * Timer status
  * After submission: results (pass/fail, time, program length)

* Must be **terminal-based (TUI)**; can use:

  * **Python**: `urwid`, `curses`, `prompt_toolkit`
  * **Rust**: `tui-rs`, `crossterm`

---

## **3. Non-Functional Requirements**

* **Cross-platform**: Linux, macOS, Windows.
* **Interchangeable editors** via flag.
* **Configurable problem set** through TOML.
* **Simple MVP design**: minimal visual elements, focus on function.

---

## **4. Inputs and Outputs**

| Type         | Description                                    |
| ------------ | ---------------------------------------------- |
| Input files  | Plain text files for program input             |
| Output files | Expected output files for verification         |
| User program | Written in any language, path selected by user |
| Editor       | Process launched to edit the program           |

---

## **5. CLI Interface / Flags**

* `--editor <editor>`: Specify the editor to launch
* `--problem <name>`: Select problem by name
* `--problems-file <path>`: Optionally specify TOML file (default: `problems.toml`)

**Example:**

```bash
kata-game --editor=nvim --problem="FizzBuzz"
```

---

## **6. Data Flow**

1. Load TOML file → list problems → user selects problem
2. Launch editor → timer starts
3. User edits program → saves & exits editor → timer stops
4. Measure program length
5. Run program on all input files → capture outputs
6. Compare outputs with expected outputs → generate correctness results
7. Display results: time, length, pass/fail

---

## **7. File & Folder Structure (Example)**

```
kata-game/
├─ problems.toml
├─ katas/
│  ├─ fizzbuzz/
│  │  ├─ input1.txt
│  │  ├─ output1.txt
│  │  └─ solution.py (optional)
│  └─ ...
├─ src/
│  └─ main.py (or main.rs)
├─ README.md
```

---

## **8. Future Extensions (Post-MVP)**

* Measure **keystrokes** and edits
* Track **undo/redo events**
* Leaderboard and streaks
* Multi-language support and sandboxing
* Error heatmaps and detailed analytics

---

✅ **Summary:**
The MVP is a **terminal-based coding game** where the user launches an editor to solve predefined katas, the app tracks **time**, **program length**, and **correctness**, and katas are defined in a **TOML file**. Editor can be swapped via a flag.

---

If you want, I can also **write a minimal working Python prototype** that implements **editor launch, timer, reading TOML, running program on inputs, and comparing outputs**, which would be a fully functional MVP.

Do you want me to do that next?

## **3. Non-Functional Requirements**

* **Cross-platform**: Linux, macOS, Windows.
* **Interchangeable editors** via flag.
* **Configurable problem set** through TOML.
* **Simple MVP design**: minimal visual elements, focus on function.

---

## **4. Inputs and Outputs**

| Type         | Description                                    |
| ------------ | ---------------------------------------------- |
| Input files  | Plain text files for program input             |
| Output files | Expected output files for verification         |
| User program | Written in any language, path selected by user |
| Editor       | Process launched to edit the program           |

---

## **5. CLI Interface / Flags**

* `--editor <editor>`: Specify the editor to launch
* `--problem <name>`: Select problem by name
* `--problems-file <path>`: Optionally specify TOML file (default: `problems.toml`)

**Example:**

```bash
kata-game --editor=nvim --problem="FizzBuzz"
```

---

## **6. Data Flow**

1. Load TOML file → list problems → user selects problem
2. Launch editor → timer starts
3. User edits program → saves & exits editor → timer stops
4. Measure program length
5. Run program on all input files → capture outputs
6. Compare outputs with expected outputs → generate correctness results
7. Display results: time, length, pass/fail

---

## **7. File & Folder Structure (Example)**

```
kata-game/
├─ problems.toml
├─ katas/
│  ├─ fizzbuzz/
│  │  ├─ input1.txt
│  │  ├─ output1.txt
│  │  └─ solution.py (optional)
│  └─ ...
├─ src/
│  └─ main.py (or main.rs)
├─ README.md
```

---

## **8. Future Extensions (Post-MVP)**

* Measure **keystrokes** and edits
* Track **undo/redo events**
* Leaderboard and streaks
* Multi-language support and sandboxing
* Error heatmaps and detailed analytics

---

✅ **Summary:**
The MVP is a **terminal-based coding game** where the user launches an editor to solve predefined katas, the app tracks **time**, **program length**, and **correctness**, and katas are defined in a **TOML file**. Editor can be swapped via a flag.
