import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./global.css";
import PaperFrameworkApp from "./PaperFrameworkApp.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <PaperFrameworkApp />
    </BrowserRouter>
  </StrictMode>
);
