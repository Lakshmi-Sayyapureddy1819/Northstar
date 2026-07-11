import js from "@eslint/js";
import eslintConfigPrettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

/**
 * Shared base ESLint flat config for all NorthStar JS/TS workspaces.
 * Prettier owns formatting (eslintConfigPrettier disables conflicting rules).
 */
export default [
  { ignores: ["dist/**", ".next/**", "node_modules/**", "coverage/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  eslintConfigPrettier,
];
