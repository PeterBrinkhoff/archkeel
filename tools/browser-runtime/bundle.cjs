"use strict";
const path = require("node:path");
const esbuild = require("esbuild");
const assets = path.resolve(__dirname, "../../src/archkeel/render/assets");
esbuild.build({
  entryPoints: [path.join(assets, "report-canvas.js")],
  bundle: true,
  format: "iife",
  platform: "browser",
  target: "es2022",
  minify: false,
  minifyWhitespace: true,
  keepNames: true,
  legalComments: "inline",
  write: false,
  plugins: [{
    name: "verified-flow-publication",
    setup(build) {
      build.onResolve({filter: /^elkjs\/lib\/elk\.bundled\.js$/}, args => {
        if (args.importer === path.join(assets, "report-layout.js")) {
          return {path: args.path, namespace: "pinned-inline-elk"};
        }
      });
      build.onLoad({filter: /.*/, namespace: "pinned-inline-elk"}, () => ({
        contents: "export default window.ELK;", loader: "js",
      }));
      build.onResolve({filter: /^\.\/flow\.js$/}, args => {
        if (args.importer === path.join(assets, "report-canvas.js")) {
          return {path: path.join(assets, "flow.runtime.js")};
        }
      });
    },
  }],
}).then(result => process.stdout.write(result.outputFiles[0].contents)).catch(() => process.exit(1));
