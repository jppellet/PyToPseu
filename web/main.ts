import { loadPyodide } from 'pyodide'

import { autocompletion } from '@codemirror/autocomplete'
import { python } from '@codemirror/lang-python'
import { Prec } from '@codemirror/state'
import { keymap, lineNumbers } from '@codemirror/view'
import { EditorView, basicSetup } from 'codemirror'

import * as LZString from "lz-string"

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import PyToPseu from '../pytopseu.py'

type InitPyodide = ReturnType<typeof loadPyodide>

// Keep in sync with Python type declaration
type AnnotationResult = {
    input_had_preamble: boolean
    input_continuations: number[]
    output: string[]
    output_continuations: number[]
}

let initPyodide: InitPyodide

const BASE_EXTERNAL_PACKAGES = ['typing-extensions']

async function main() {
    const doLoadPyodide = (globalThis as any).loadPyodide as typeof loadPyodide

    let changeListenerTimeoutHandle: number | undefined = undefined

    let updateAnnotations: () => Promise<void>
    let saveToURL: () => Promise<void>

    let ignoreUpdate = false

    const clearLineAndUpdateListener = EditorView.updateListener.of((update) => {
        if (ignoreUpdate || !update.docChanged) {
            return
        }

        if (changeListenerTimeoutHandle) {
            clearTimeout(changeListenerTimeoutHandle)
        }
        const sel = update.state.selection.asSingle().main
        if (!sel.empty) {
            return
        }

        const line = update.state.doc.lineAt(sel.anchor)
        const selCol = sel.anchor - line.from
        const lineText = line.text
        const Marker = "#│"
        const markerPos = lineText.indexOf(Marker)
        if (markerPos !== -1) {
            let lastCharToInclude = markerPos - 1
            while (lineText[lastCharToInclude] === ' ') {
                lastCharToInclude--
            }
            ignoreUpdate = true
            const newLineText = lineText.substring(0, lastCharToInclude + 1)
            try {
                editor.dispatch(editor.state.update({
                    changes: { from: line.from, to: line.to, insert: newLineText },
                    selection: { anchor: line.from + Math.min(selCol, newLineText.length) }
                }))
            } finally {
                ignoreUpdate = false
            }
        }
        changeListenerTimeoutHandle = setTimeout(updateAnnotations, 1000)
    })

    const initialCode = "# Tapez votre code ci-dessous\n"

    const editor = new EditorView({
        doc: initialCode,
        selection: { anchor: initialCode.length },
        extensions: [
            basicSetup,
            lineNumbers(),
            python(),
            autocompletion(),
            clearLineAndUpdateListener,
            Prec.highest(
                keymap.of([
                    { key: "Ctrl-u", mac: "Cmd-u", run: () => { updateAnnotations(); return true } },
                    { key: "Ctrl-s", mac: "Cmd-s", run: () => { saveToURL(); return true } },
                ])
            ),
            EditorView.theme({
                "&": {
                    fontSize: "14pt",
                    border: "2px solid lightgray"
                },
                ".cm-content": {
                    fontFamily: "JetBrains Mono, Menlo, Monaco, Lucida Console, monospace",
                },
                ".cm-line, .cm-gutterElement": {
                    height: "24px",
                },
            }
            ),
        ],
        parent: document.body,
    })

    async function updateAnnotationsFor(userCode: string) {
        try {
            const pyodide = await initPyodide
            await pyodide.runPythonAsync(`__user_code__ = ${JSON.stringify(userCode)}`)
            let runResult = await pyodide.runPythonAsync(PyToPseu)
            if (typeof runResult === "object" && "toJs" in runResult) {
                runResult = runResult.toJs()
                if ("target" in runResult) {
                    runResult = runResult.target
                }
            }
            if (typeof runResult === "string") {
                const annotationResult = JSON.parse(runResult) as AnnotationResult
                // console.log("Annotated:")
                // console.log(annotationResult)

                const oldSelPos = editor.state.selection.main.from
                const oldLine = editor.state.doc.lineAt(oldSelPos)
                const oldCol = oldSelPos - oldLine.from
                // console.log({ oldSelPos, oldLine, oldLineNumber: oldLine.number, oldCol })
                ignoreUpdate = true
                try {
                    editor.dispatch(editor.state.update({
                        changes: { from: 0, to: editor.state.doc.length, insert: annotationResult.output.join("\n") },
                    }))
                    const newLineNumber = oldLine.number + (annotationResult.input_had_preamble ? 0 : 4)
                    let newLineDelta = 0
                    for (const continuation of annotationResult.input_continuations) {
                        if (continuation <= newLineNumber) {
                            newLineDelta--
                        } else {
                            break
                        }
                    }
                    for (const continuation of annotationResult.output_continuations) {
                        if (continuation <= newLineNumber) {
                            newLineDelta++
                        } else {
                            break
                        }
                    }
                    const newLine = editor.state.doc.line(newLineNumber + newLineDelta)
                    const newSelPos = newLine.from + oldCol
                    // console.log({ newLine, newLineDelta, newLineNumber: newLineNumber, newSelPos })
                    editor.dispatch(editor.state.update({
                        selection: { anchor: newSelPos }
                    }))
                } finally {
                    ignoreUpdate = false
                }
            } else {
                console.log(runResult)
            }
        } catch (e) {
            console.error(e)
        }
    }

    updateAnnotations = async () => {
        return updateAnnotationsFor(editor.state.doc.toString())
    }

    saveToURL = async () => {
        const userCode = editor.state.doc.toString()
        const compressed = LZString.compressToEncodedURIComponent(userCode)
        const url = new URL(window.location.href)
        url.searchParams.set('t', compressed)
        window.history.replaceState({}, '', url.toString())
    }


    const editorStyle = editor.dom.style
    editorStyle.height = '100%'


    // const buttons = document.getElementById('buttons')!

    // const annotateButton = document.createElement('button')
    // annotateButton.textContent = 'Annotate'
    // annotateButton.onclick = updateAnnotations

    // buttons.appendChild(annotateButton)

    // load pyodide and external packages
    initPyodide = doLoadPyodide().then((pyodide) => {
        return pyodide.loadPackage(BASE_EXTERNAL_PACKAGES).then(() => {
            return pyodide
        })
    })

    // check if there is code to preload the editor with in the URL
    initPyodide.then(() => {
        const url = new URL(window.location.href)
        const compressedCode = url.searchParams.get('t')
        if (compressedCode) {
            const code = LZString.decompressFromEncodedURIComponent(compressedCode)
            if (code) {
                updateAnnotationsFor(code).then(() => {
                    // move cursor to end
                    editor.dispatch(editor.state.update({
                        selection: { anchor: editor.state.doc.length }
                    }))
                })
            }
        }
    })

    // set focus to editor
    editor.focus()
}


// function preambleLength(doc: Text): number {
//     if (doc.lines < 5 || !doc.line(1).text.startsWith('"""') || !doc.line(4).text.startsWith('"""') || !doc.line(3).text.startsWith("---") || !doc.line(2).text.startsWith("Source")) {
//         return 0
//     }
//     return doc.line(5).from
// }

main()
