# How to create a fold component with open tui

```tsx
import { render } from "@opentui/react";
import { useState } from "react";

type FoldProps = {
  foldedContent: React.ReactNode;
  unfoldedContent: React.ReactNode;
  defaultFolded?: boolean;
};

export const Fold = ({
  foldedContent,
  unfoldedContent,
  defaultFolded = true,
}: FoldProps) => {
  const [isFolded, setIsFolded] = useState(defaultFolded);

  const folded = <text>{">"}</text>;
  const unfolded = <text>v</text>;

  return (
    <box
      border
      onMouseDown={() => setIsFolded((folded) => !folded)}
      style={{ flexDirection: "row" }}
    >
      {isFolded ? folded : unfolded}
      {isFolded ? foldedContent : unfoldedContent}
    </box>
  );
};

function App() {
  return (
    <Fold
      foldedContent={<text>Click to unfold</text>}
      unfoldedContent={
        <box>
          <text>
            This is the unfolded content.
            <br />
            Click to fold back.
          </text>
        </box>
      }
    />
  );
}

render(<App />);
```
