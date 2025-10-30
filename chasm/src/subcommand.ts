export async function getGitDiff(): Promise<string> {
  const proc = Bun.spawn(['git', 'diff'], {
    stdout: 'pipe',
    stderr: 'pipe',
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`git diff failed: ${error}`);
  }

  return output;
}

export async function getGitStatus(): Promise<string> {
  const proc = Bun.spawn(['git', 'status', '--porcelain'], {
    stdout: 'pipe',
    stderr: 'pipe',
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`git status failed: ${error}`);
  }

  return output;
}
