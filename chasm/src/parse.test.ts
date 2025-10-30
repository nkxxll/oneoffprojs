import { test, expect } from "bun:test";
import { parse, getAllFileStatuses } from "./parse.ts";

test("parses a simple diff with added and removed lines", () => {
  const diff = `diff --git a/file.txt b/file.txt
index 1234567..abcdef0 100644
--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,3 @@
 context line
-old line
+new line
 context line`;

  const result = parse(diff);

  expect(result.files).toHaveLength(1);
  const file = result.files[0]!;
  expect(file.from).toBe("a/file.txt");
  expect(file.to).toBe("b/file.txt");
  expect(file.hunks).toHaveLength(1);

  const hunk = file.hunks[0]!;
  expect(hunk.header).toBe("@@ -1,3 +1,3 @@");
  expect(hunk.lines).toHaveLength(5); // context, removed, added, context, context?

  // Check lines
  expect(result.all).toHaveLength(diff.split("\n").length);
  expect(result.all[0]!.kind).toBe("diff_header");
  expect(result.all[1]!.kind).toBe("index_header");
  expect(result.all[2]!.kind).toBe("file_header_old");
  expect(result.all[3]!.kind).toBe("file_header_new");
  expect(result.all[4]!.kind).toBe("hunk_header");
  expect(result.all[5]!.kind).toBe("context");
  expect(result.all[6]!.kind).toBe("removed");
  expect(result.all[7]!.kind).toBe("added");
  expect(result.all[8]!.kind).toBe("context");
});

test("parses diff with multiple files", () => {
  const diff = `diff --git a/file1.txt b/file1.txt
--- a/file1.txt
+++ b/file1.txt
@@ -1 +1 @@
-old
+new
diff --git a/file2.txt b/file2.txt
--- a/file2.txt
+++ b/file2.txt
@@ -2 +2 @@
-old2
+new2`;

  const result = parse(diff);

  expect(result.files).toHaveLength(2);
  expect(result.files[0]!.from).toBe("a/file1.txt");
  expect(result.files[1]!.from).toBe("a/file2.txt");
});

test("parses empty diff", () => {
  const diff = "";

  const result = parse(diff);

  expect(result.files).toHaveLength(0);
  expect(result.all).toHaveLength(1);
  expect(result.all[0]!.kind).toBe("context");
});

test("handles diff with only headers", () => {
  const diff = `diff --git a/file.txt b/file.txt
index 123..456 100644
--- a/file.txt
+++ b/file.txt`;

  const result = parse(diff);

  expect(result.files).toHaveLength(1);
  expect(result.files[0]!.hunks).toHaveLength(0);
});

test("parses long real diff with multiple hunks", () => {
  const diff = `diff --git a/src/main.js b/src/main.js
index 83db48f..bf3c6e4 100644
--- a/src/main.js
+++ b/src/main.js
@@ -1,10 +1,12 @@
+// Added comment
 const express = require('express');
 const app = express();

 app.get('/', (req, res) => {
-  res.send('Hello World!');
+  res.send('Hello, World!');
 });

+// Another added line
 app.listen(3000, () => {
   console.log('Server running on port 3000');
 });
@@ -15,7 +17,8 @@ app.listen(3000, () => {
 // Function to handle errors
 function handleError(err) {
   console.error('Error:', err);
-  process.exit(1);
+  // Log and exit
+  process.exit(1);
 }

 module.exports = app;`;

  const result = parse(diff);

  expect(result.files).toHaveLength(1);
  const file = result.files[0]!;
  expect(file.from).toBe("a/src/main.js");
  expect(file.to).toBe("b/src/main.js");
  expect(file.hunks).toHaveLength(2);

  // First hunk
  const hunk1 = file.hunks[0]!;
  expect(hunk1.header).toBe("@@ -1,10 +1,12 @@");
  expect(hunk1.lines.some(line => line.kind === "added" && line.content === "+// Added comment")).toBe(true);

  // Second hunk
  const hunk2 = file.hunks[1]!;
  expect(hunk2.header).toBe("@@ -15,7 +17,8 @@ app.listen(3000, () => {");
  expect(hunk2.lines.some(line => line.kind === "added" && line.content === "+  // Log and exit")).toBe(true);

  expect(result.all.length).toBeGreaterThan(20);
});

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
  expect(statuses.find(s => s.file.to === 'b/added.txt')?.status).toBe('added');
  expect(statuses.find(s => s.file.to === '/dev/null')?.status).toBe('deleted');
  expect(statuses.find(s => s.file.to === 'b/modified.txt' && s.file.from === 'a/modified.txt')?.status).toBe('modified');
  expect(statuses.find(s => s.file.to === 'b/new.txt')?.status).toBe('renamed');
});
