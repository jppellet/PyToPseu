#!/usr/bin/env node

(async function () {
    const esbuild = require("esbuild")
    const suffix = ""
    const bundleFile = `web/bundle${suffix}.js`
    const result = await esbuild
        .build({
            minify: false,
            keepNames: true,
            bundle: true,
            sourcemap: true,
            loader: {
                ".html": "text",
                ".css": "text",
                ".icon.svg": "text",
                ".svg": "text",
                ".py": "text",
            },
            logLevel: "info",
            entryPoints: ["web/main.ts"],
            outfile: bundleFile,
            metafile: true,
            // external: ["pyodide2"],
        })

})()