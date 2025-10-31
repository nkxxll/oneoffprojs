import { parseGitStatus } from "./status";

export interface DebuggerProps {
  debugging: boolean;
  status: string;
  data: any;
}

export function Debugger({ debugging, status, data }: DebuggerProps) {
  return (
    <>
      {debugging && (
        <div>
          <scrollbox
            style={{ backgroundColor: "black", zIndex: 20 }}
            flexGrow={1}
          >
            <text>
              {JSON.stringify(parseGitStatus(status), null, 2)}{" "}
              {JSON.stringify(data?.statusGroups, null, 2)}{" "}
            </text>
          </scrollbox>
        </div>
      )}
    </>
  );
}
