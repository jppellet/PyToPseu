import { loadPyodide } from 'pyodide'

import { autocompletion } from '@codemirror/autocomplete'
import { python } from '@codemirror/lang-python'
import { Prec, Text } from '@codemirror/state'
import { keymap, lineNumbers } from '@codemirror/view'
import { EditorView, basicSetup } from 'codemirror'

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import PyToPseu from '../pytopseu.py'

type InitPyodide = ReturnType<typeof loadPyodide>

let initPyodide: InitPyodide

async function main() {
    const doLoadPyodide = (globalThis as any).loadPyodide as typeof loadPyodide

    let changeListenerTimeoutHandle: number | undefined = undefined

    let updateAnnotations: () => Promise<void>
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
            try {
                editor.dispatch(editor.state.update({
                    changes: { from: line.from, to: line.to, insert: lineText.substring(0, lastCharToInclude + 1) },
                    selection: { anchor: line.from + selCol }
                }))
            } finally {
                ignoreUpdate = false
            }
        }
        changeListenerTimeoutHandle = setTimeout(updateAnnotations, 1000)
    })

    const editor = new EditorView({
        doc: "# Tapez votre code ci-dessous",
        extensions: [
            basicSetup,
            lineNumbers(),
            python(),
            autocompletion(),
            clearLineAndUpdateListener,
            Prec.highest(
                keymap.of([
                    { key: "Ctrl-u", mac: "Cmd-u", run: () => { console.log("cmd-u"); updateAnnotations(); return true } },
                ])
            )
        ],
        parent: document.body,
    })

    updateAnnotations = async () => {
        // get code from editor
        const userCode = editor.state.doc.toString()
        console.log("Original:")
        console.log(userCode)
        try {
            const pyodide = await initPyodide
            await pyodide.runPythonAsync(`__user_code__ = ${JSON.stringify(userCode)}`)
            let result = await pyodide.runPythonAsync(PyToPseu)
            if (typeof result === "object" && "toJs" in result) {
                result = result.toJs()
                if ("target" in result) {
                    result = result.target
                }
            }
            if (typeof result === "string") {
                console.log("Annotated:")
                console.log(result)

                const oldSelPos = editor.state.selection.main.from
                const oldLine = editor.state.doc.lineAt(oldSelPos)
                const oldCol = oldSelPos - oldLine.from
                const oldHаsPreamble = preambleLength(editor.state.doc) !== 0
                console.log({ oldSelPos, oldLine, oldLineNumber: oldLine.number, oldCol })
                ignoreUpdate = true
                try {
                    editor.dispatch(editor.state.update({
                        changes: { from: 0, to: editor.state.doc.length, insert: result },
                    }))
                    const newLine = editor.state.doc.line(oldLine.number + (oldHаsPreamble ? 0 : 4))
                    const newSelPos = newLine.from + oldCol
                    console.log({ newLine, newLineNumber: newLine.number, newSelPos })
                    editor.dispatch(editor.state.update({
                        selection: { anchor: newSelPos }
                    }))
                } finally {
                    ignoreUpdate = false
                }
            } else {
                console.log(result)
            }
        } catch (e) {
            console.error(e)
        }
    }

    const editorStyle = editor.dom.style
    editorStyle.height = '100%'
    editorStyle.fontFamily = "Menlo"
    editorStyle.fontSize = "16px"
    editorStyle.lineHeight = "1.5"


    // const buttons = document.getElementById('buttons')!

    // const annotateButton = document.createElement('button')
    // annotateButton.textContent = 'Annotate'
    // annotateButton.onclick = updateAnnotations

    // buttons.appendChild(annotateButton)
    initPyodide = doLoadPyodide()
}


function preambleLength(doc: Text): number {
    if (doc.lines < 5 || !doc.line(1).text.startsWith('"""') || !doc.line(4).text.startsWith('"""') || !doc.line(3).text.startsWith("---") || !doc.line(2).text.startsWith("Source")) {
        return 0
    }
    return doc.line(5).from
}

main()
