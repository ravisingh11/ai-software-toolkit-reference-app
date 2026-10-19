// Keep the verification runtime tied to the real application's configuration.
export function localConfiguration(source, revision) {
  if (!/^[a-f0-9]{40}$/.test(revision)) throw new Error('Missing immutable source revision');
  if (!Array.isArray(source.d1_databases) || source.d1_databases.length !== 1 || source.d1_databases[0].binding !== 'DB') {
    throw new Error('Expected the real application DB binding');
  }
  if (source.assets?.binding !== 'ASSETS' || !source.vars?.TOOLKIT_REVISION) {
    throw new Error('Expected real application assets and toolkit revision');
  }
  const { account_id: _account, $schema: _schema, ...local } = source;
  return {
    ...local,
    name: 'fieldnotes-lifecycle-verification',
    main: '/app/dist/index.js',
    no_bundle: true,
    assets: { ...source.assets, directory: '/app/public' },
    vars: { ...source.vars, APP_REVISION: revision },
    d1_databases: [{ binding: 'DB', database_name: 'fieldnotes-local-verification', database_id: '00000000-0000-0000-0000-000000000000', migrations_dir: '/app/migrations' }],
  };
}
