export type LineKind =
  | "diff_header"
  | "index_header"
  | "file_header_old"
  | "file_header_new"
  | "hunk_header"
  | "context"
  | "added"
  | "removed";

export interface DiffHunk {
  header: string;
  startLine: number;
  lines: DiffLine[];
}

export interface DiffFile {
  from: string;
  to: string;
  headerStart: number;
  hunks: DiffHunk[];
}

export interface DiffLine {
  kind: LineKind;
  content: string;
  lineNumber: number;
  file?: string;
  hunk?: number;
}

export interface DiffMap {
  files: DiffFile[];
  all: DiffLine[];
  fileIndex: Map<number, DiffFile>; // line → file
  hunkIndex: Map<number, DiffHunk>; // line → hunk
}

export type FileStatus = 'added' | 'deleted' | 'modified' | 'renamed';

export function parse(diff: string): DiffMap {
  const diffSplit = diff.split("\n");

  const all: DiffLine[] = [];
  const files: DiffFile[] = [];
  const fileIndex = new Map<number, DiffFile>();
  const hunkIndex = new Map<number, DiffHunk>();

  let currentFile: DiffFile | null = null;
  let currentHunk: DiffHunk | null = null;

  for (let i = 0; i < diffSplit.length; i++) {
    const line = diffSplit[i]!;
    let kind: LineKind;

    if (line.startsWith("diff --git")) {
      currentFile = { from: "", to: "", headerStart: i, hunks: [] };
      files.push(currentFile);
      kind = "diff_header";
    } else if (line.startsWith("index ")) {
      kind = "index_header";
    } else if (line.startsWith("--- ")) {
      kind = "file_header_old";
      currentFile!.from = line.substring(4);
    } else if (line.startsWith("+++ ")) {
      kind = "file_header_new";
      currentFile!.to = line.substring(4);
    } else if (line.startsWith("@@")) {
      kind = "hunk_header";
      currentHunk = { header: line, startLine: i, lines: [] };
      currentFile!.hunks.push(currentHunk);
    } else if (line.startsWith("+")) kind = "added";
    else if (line.startsWith("-")) kind = "removed";
    else kind = "context";

    const diffLine: DiffLine = { kind, content: line, lineNumber: i };
    all.push(diffLine);
    if (currentFile) fileIndex.set(i, currentFile);
    if (currentHunk) {
      currentHunk.lines.push(diffLine);
      hunkIndex.set(i, currentHunk);
    }
  }

  return { files, all, fileIndex, hunkIndex };
}

function getFileName(path: string): string {
  if (path === '/dev/null') return path;
  if (path.startsWith('a/')) return path.slice(2);
  if (path.startsWith('b/')) return path.slice(2);
  return path;
}

export function getFileStatus(file: DiffFile): FileStatus {
  const { from, to } = file;
  if (from === '/dev/null' && to !== '/dev/null') return 'added';
  if (from !== '/dev/null' && to === '/dev/null') return 'deleted';
  if (getFileName(from) === getFileName(to)) return 'modified';
  return 'renamed';
}

export function getAllFileStatuses(diffMap: DiffMap): Array<{file: DiffFile, status: FileStatus}> {
  return diffMap.files.map(file => ({
    file,
    status: getFileStatus(file)
  }));
}
