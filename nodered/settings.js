const path = require('path');

module.exports = {
  uiPort: 1880,
  flowFile: process.env.FLOW_FILE || path.join(__dirname, 'flows-wokwi.json'),
  credentialSecret: false,
  logging: { console: { level: 'info' } },
  editorTheme: { projects: { enabled: false } }
};
