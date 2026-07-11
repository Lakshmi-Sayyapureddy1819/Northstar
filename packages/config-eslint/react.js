import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";

import base from "./base.js";

/** Base config plus React hooks rules and browser globals (web + ui). */
export default [
  ...base,
  {
    plugins: { "react-hooks": reactHooks },
    rules: { ...reactHooks.configs.recommended.rules },
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
  },
];
