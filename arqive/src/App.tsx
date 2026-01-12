import { AuthProvider } from "./components/AuthContext";
import { AuthGuard } from "./components/AuthGuard";
import { QueryCode } from "./components/QueryCode";
import { Toaster } from "react-hot-toast";

import "./index.css";

import logo from "./logo.svg";
import reactLogo from "./react.svg";

export function App() {
  return (
    <AuthProvider>
      <Toaster />
      <div className="container mx-auto p-8 relative z-10">
        <AuthGuard>
          <QueryCode />
        </AuthGuard>
      </div>
    </AuthProvider>
  );
}

export default App;
