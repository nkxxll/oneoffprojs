# Detailed Plan: Storage Layer

This plan covers the implementation of the storage layer in `storage.go`. This layer is responsible for all persistence logic, including loading prompts from and saving them to a TOML file.

## 1. File Path Management

-   **Action:** Implement a function to resolve the storage file path.
-   **Function:** `getStorageFilePath() (string, error)`
-   **Logic:**
    1.  Get the user's home directory using `os.UserHomeDir()`.
    2.  Construct the config directory path (e.g., `~/.config/prompt-manager`).
    3.  Use `os.MkdirAll()` to create this directory if it doesn't exist. This is idempotent and safe to call every time.
    4.  Join the directory path with the filename `prompts.toml` to get the final file path.
    5.  Return the path and any error that occurred.

## 2. Store Constructor

-   **Action:** Create a constructor for the `Store`.
-   **Function:** `NewStore() (*Store, error)`
-   **Logic:**
    1.  Call `getStorageFilePath()` to get the path to the `prompts.toml` file.
    2.  If there's an error, return it immediately.
    3.  Initialize a `Store` instance with the file path.
    4.  Call the `Load()` method on the new store instance to populate the in-memory prompt slice.
    5.  Return the pointer to the `Store` and a `nil` error.

## 3. Core I/O Methods

-   **Action:** Implement the `Load` and `Save` methods to handle file I/O.
-   **`Load()` Method:**
    -   **Signature:** `(s *Store) Load() error`
    -   **Logic:**
        1.  Read the entire content of `s.filePath` using `os.ReadFile()`.
        2.  If the file doesn't exist (`os.IsNotExist(err)`), do nothing and return `nil`. This is a valid state for the first run.
        3.  If another read error occurs, return it.
        4.  Use `toml.Unmarshal()` to decode the file content into `s.prompts`.
        5.  Return any unmarshaling error.
-   **`Save()` Method:**
    -   **Signature:** `(s *Store) Save() error`
    -   **Logic:**
        1.  Use `toml.Marshal()` to encode the `s.prompts` slice into a TOML byte slice.
        2.  If a marshaling error occurs, return it.
        3.  Write the byte slice to `s.filePath` using `os.WriteFile()` with permissions `0644`.
        4.  Return any write error.

## 4. CRUD Operations

-   **Action:** Implement the public methods for Create, Read, Update, and Delete. These methods will manipulate the in-memory `s.prompts` slice and call `s.Save()` to persist changes immediately.
-   **`GetAll()`:**
    -   **Signature:** `(s *Store) GetAll() []Prompt`
    -   **Logic:** Return a copy of the `s.prompts` slice.
-   **`Add(p Prompt)`:**
    -   **Signature:** `(s *Store) Add(p Prompt) error`
    -   **Logic:**
        1.  Append the new `Prompt` `p` to the `s.prompts` slice.
        2.  Call `s.Save()` and return its error.
-   **`Get(id uuid.UUID)`:**
    -   **Signature:** `(s *Store) Get(id uuid.UUID) (Prompt, bool)`
    -   **Logic:**
        1.  Iterate through `s.prompts`.
        2.  If a prompt with the matching `id` is found, return that prompt and `true`.
        3.  If no match is found, return an empty `Prompt` struct and `false`.
-   **`Update(p Prompt)`:**
    -   **Signature:** `(s *Store) Update(p Prompt) error`
    -   **Logic:**
        1.  Iterate through `s.prompts` with an index.
        2.  If a prompt with the matching `p.ID` is found, replace the element at that index with `p`.
        3.  Call `s.Save()` and return its error.
        4.  If not found, return an error (e.g., `fmt.Errorf("prompt with ID %s not found", p.ID)`).
-   **`Remove(id uuid.UUID)`:**
    -   **Signature:** `(s *Store) Remove(id uuid.UUID) error`
    -   **Logic:**
        1.  Find the index of the prompt with the given `id`.
        2.  If not found, return an error.
        3.  Remove the element from the slice using `s.prompts = append(s.prompts[:i], s.prompts[i+1:]...)`.
        4.  Call `s.Save()` and return its error.
