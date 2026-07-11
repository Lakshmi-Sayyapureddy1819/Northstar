import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// globals:false, so register DOM cleanup between tests explicitly.
afterEach(() => {
  cleanup();
});
