# Status Component Plan

## Overview
Build a status component that processes a parsed Git diff (`DiffMap`) to determine and display the status of each file (added, deleted, modified, renamed). This component will be built using OpenTUI React for terminal UI rendering.

## Requirements
- Input: `DiffMap` from the existing `parse` function
- Output: Visual display grouping files by status
- Handle edge cases like empty diffs or files with no changes

## Implementation Steps

### 1. Extend Parser with Status Computation
Add a new function in `parse.ts` to compute file statuses based on `from` and `to` paths:

```typescript
export type FileStatus = 'added' | 'deleted' | 'modified' | 'renamed';

export function getFileStatus(file: DiffFile): FileStatus {
  const { from, to } = file;
  if (from === '/dev/null' && to !== '/dev/null') return 'added';
  if (from !== '/dev/null' && to === '/dev/null') return 'deleted';
  if (from === to) return 'modified';
  return 'renamed';
}

export function getAllFileStatuses(diffMap: DiffMap): Array<{file: DiffFile, status: FileStatus}> {
  return diffMap.files.map(file => ({
    file,
    status: getFileStatus(file)
  }));
}
```

### 2. Create StatusComponent
Create a new file `StatusComponent.tsx` in `src/`:

```typescript
import { TextAttributes } from "@opentui/core";
import { getAllFileStatuses, FileStatus } from "./parse.ts";

interface StatusComponentProps {
  diffMap: DiffMap;
}

export function StatusComponent({ diffMap }: StatusComponentProps) {
  const fileStatuses = getAllFileStatuses(diffMap);

  const grouped = fileStatuses.reduce((acc, { file, status }) => {
    if (!acc[status]) acc[status] = [];
    acc[status].push(file);
    return acc;
  }, {} as Record<FileStatus, DiffFile[]>);

  const statusColors = {
    added: TextAttributes.GREEN,
    deleted: TextAttributes.RED,
    modified: TextAttributes.YELLOW,
    renamed: TextAttributes.BLUE
  };

  return (
    <box flexDirection="column">
      {(['added', 'deleted', 'modified', 'renamed'] as FileStatus[]).map(status => {
        const files = grouped[status] || [];
        if (files.length === 0) return null;

        return (
          <box key={status} flexDirection="column" marginBottom={1}>
            <text attributes={statusColors[status]}>
              {status.toUpperCase()}:
            </text>
            {files.map((file, i) => (
              <text key={i} attributes={TextAttributes.DIM}>
                {status === 'renamed' ? `${file.from} -> ${file.to}` : file.to}
              </text>
            ))}
          </box>
        );
      })}
    </box>
  );
}
```

### 3. Update App Component
Modify `src/index.tsx` to include the StatusComponent and handle diff input:

```typescript
// ... existing imports
import { StatusComponent } from "./StatusComponent.tsx";
import { parse } from "./parse.ts";

// Example diff - in real usage, this would come from props, stdin, etc.
const exampleDiff = `diff --git a/newfile.txt b/newfile.txt
new file mode 100644
index 0000000..e69de29
--- /dev/null
+++ b/newfile.txt
@@ -0,0 +1 @@
+hello world
diff --git a/oldfile.txt b/oldfile.txt
deleted file mode 100644
index e69de29..0000000
--- a/oldfile.txt
+++ /dev/null
@@ -1 +0,0 @@
-hello world
diff --git a/modified.txt b/modified.txt
index 83db48f..bf3c6e4 100644
--- a/modified.txt
+++ b/modified.txt
@@ -1 +1 @@
-hello
+world
diff --git a/oldname.txt b/newname.txt
similarity index 100%
rename from oldname.txt
rename to newname.txt`;

function App() {
  const diffMap = parse(exampleDiff);

  return (
    <box alignItems="center" justifyContent="center" flexGrow={1}>
      <box justifyContent="center" alignItems="flex-start" flexDirection="column">
        <ascii-font font="tiny" text="Git Diff Status" />
        <StatusComponent diffMap={diffMap} />
      </box>
    </box>
  );
}
```

### 4. Add Tests
Extend `parse.test.ts` with tests for status computation:

```typescript
test("computes file statuses correctly", () => {
  const diff = `diff --git a/added.txt b/added.txt
--- /dev/null
+++ b/added.txt
@@ -0,0 +1 @@
+new file
diff --git a/deleted.txt b/deleted.txt
--- a/deleted.txt
+++ /dev/null
@@ -1 +0,0 @@
-old file
diff --git a/modified.txt b/modified.txt
--- a/modified.txt
+++ b/modified.txt
@@ -1 +1 @@
-old
+new
diff --git a/old.txt b/new.txt
--- a/old.txt
+++ b/new.txt
@@ -1 +1 @@
-same
+same`;

  const diffMap = parse(diff);
  const statuses = getAllFileStatuses(diffMap);

  expect(statuses).toHaveLength(4);
  expect(statuses.find(s => s.file.to === 'added.txt')?.status).toBe('added');
  expect(statuses.find(s => s.file.to === 'deleted.txt')?.status).toBe('deleted');
  expect(statuses.find(s => s.file.to === 'modified.txt')?.status).toBe('modified');
  expect(statuses.find(s => s.file.to === 'new.txt')?.status).toBe('renamed');
});
```

### 5. Run and Verify
- Run `bun run dev` to test the UI
- Run `bun test` to verify tests pass
- Check that statuses are displayed correctly for various diff scenarios

## Future Enhancements
- Add file mode changes (e.g., executable permissions)
- Include diff statistics (lines added/removed per file)
- Support for binary files
- Interactive navigation through files
