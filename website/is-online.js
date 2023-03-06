// Waits, without blocking, until the document is ready, then runs the function.
function onReady(fn) {
    if (document.readyState === 'loading')
        document.addEventListener('DOMContentLoaded', fn)
    else
        fn()
}

// Update the UI to show loading has failed, with the given error message.
function notifyLoadingError(message) {
    onReady(() => {
        let el = document.getElementById('loadingError')
        el.innerText = `${el.innerText}${message}\n`
        el.style.display = '' // Unset, so show element

        let loading = document.getElementById('loadingProgressContainer')
        loading.style.display = 'none'
    })
}

// Warn the user, with a helpful messages, if JS dependencies are broken.
function assertDependencies() {
    function errMissingDependency(message) {
        notifyLoadingError(message)
        throw message
    }

    if (typeof $ === 'undefined') {
        errMissingDependency('Third-party scripts have been blocked. Please allow scripts to load from the CDN.')
    } else if (typeof WebAssembly === 'undefined') {
        errMissingDependency('WebAssembly is not supported. Please upgrade your browser.')
    }
}
assertDependencies()

// Resolves the asynchronous request for user input, or ignores the input if the application
// is not requesting any input at this time.
let resolveInputPromise = undefined

// Does nothing when the user gives input, because the application is not ready for it.
function ignoreFutureInput() {
    resolveInputPromise = () => { }
}
ignoreFutureInput()

// Writes to the terminal, with no extra newline. For supporting stdout.
// Initialized after the terminal is loaded.
let stdout = (str) => { }

// Called from Python to asynchronously request user input. Later, the request
// will be resolved, returning the input to Python.
async function user_input(prompt) {
    stdout(prompt)
    return new Promise((resolve, reject) => resolveInputPromise = resolve)
}

// Returns the input to Python, then ignores future input (until requested again).
function dispatchInput(str) {
    let resolveInputPromiseOld = resolveInputPromise
    ignoreFutureInput()
    resolveInputPromiseOld(str)
}

// Initialize a terminal using JQuery Terminal.
function initTerminal() {
    let command_processor = dispatchInput
    let options = {
        greetings: '' /* No JQuery Terminal banner */,
        height: 645,
        history: false,
        outputLimit: 500 /* Lines */,
        prompt: '' /* Will be given when needed via Python, so don't have JQuery Terminal add something fixed */,
    }
    let term = $('#terminal').terminal(command_processor, options)

    // Implementation of stdout, as required above.
    function stdout(str) {
        str = $.terminal.escape_brackets(str)
        options = { 'newline': false }
        term.echo(str, options)
    }

    return {
        term,
        stdout,
    }
}

// Update the UI to say we are loading component.
function notifyLoading(component) {
    document.getElementById('loadingText').innerText = `Loading ${component}...`
}

// Load Python using Pyodide.
async function loadPython(term) {
    let println = function (str) {
        stdout(`${str}\n`)
    }
    let eprintln = function (str) {
        str = $.terminal.escape_brackets(str)
        term.echo(`[[;red;black]Error: ${str}]`)
    }

    notifyLoading('Pyodide')
    let pyodide = await loadPyodide()
    pyodide.setStdout({ batched: println })
    pyodide.setStderr({ batched: eprintln })

    return pyodide
}

// Load dependencies, then run Ionnsaich Seo.
async function runApplication(pyodide) {
    notifyLoading('Pandas')
    await pyodide.loadPackage('pandas', { 'errorCallback': notifyLoadingError })

    notifyLoading('Ionnsaich Seo!')
    let appSourceZip = undefined
    try {
        let response = await fetch('IonnsaichSeo-source.zip')
        if (!response.ok)
            throw `Error fetching ${response.url}: HTTP ${response.status} ${response.statusText}`
        appSourceZip = await response.arrayBuffer()
    } catch (err) {
        notifyLoadingError(err)
        throw err
    }
    pyodide.unpackArchive(appSourceZip, 'zip')

    await pyodide.runPythonAsync(`
import js

import is_main_menu

# Hide the loading message. We don't set style "display: none", because
# we don't want the terminal to jump around on the page.
js.document.getElementById('loadingProgressContainer').style.visibility = 'hidden'

await is_main_menu.main()
print('')
print('Application exited. Reload the page to restart the app.')
`)
}

async function main() {
    let terminal = initTerminal()
    let term = terminal.term
    stdout = terminal.stdout

    let pyodide = await loadPython(term)
    await runApplication(pyodide)
    term.pause()
}

onReady(main)
