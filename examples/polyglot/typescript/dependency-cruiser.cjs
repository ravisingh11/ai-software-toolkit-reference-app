module.exports = {
  forbidden: [
    {
      name: "domain-cannot-import-node-builtins",
      severity: "error",
      from: {
        path: "^(examples/polyglot/typescript/src/domain|src/domain)\\.ts$",
      },
      to: { dependencyTypes: ["core"] },
    },
    { name: "no-cycles", severity: "error", from: {}, to: { circular: true } },
    {
      name: "no-unresolved",
      severity: "error",
      from: {},
      to: { couldNotResolve: true },
    },
    {
      name: "domain-cannot-import-cli-or-node-io",
      severity: "error",
      from: {
        path: "^(examples/polyglot/typescript/src/domain|src/domain)\\.ts$",
      },
      to: { path: "(cli\\.mjs$|^node:|^node_modules/)" },
    },
  ],
  options: {
    tsPreCompilationDeps: true,
    doNotFollow: { path: "node_modules" },
  },
};
