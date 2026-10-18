import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['.artifacts/**', '.proof/**', 'node_modules/**', 'dist/**', 'coverage/**'] },
  {
    files: ['src/**/*.ts', 'examples/polyglot/typescript/src/**/*.ts'],
    extends: [...tseslint.configs.recommendedTypeChecked],
    languageOptions: { parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname } },
    rules: {
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      'no-empty': ['error', { allowEmptyCatch: false }],
      'no-unsafe-finally': 'error',
    },
  },
  { files: ['public/**/*.js'], rules: { 'no-empty': 'error', 'no-unsafe-finally': 'error', 'no-dupe-keys': 'error' } },
);
