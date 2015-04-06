
(if you are upgrading from an older version, see CHANGES.txt)

## typescript-tools.vim

Vim plugin for TypeScript support, based on clausreinke/typescript-tools.

### Installation

1. Install `typescript-tools` globally

  ```
  $ npm install -g typescript-tools
  ```

  The installation should give you a global `tss` command (try `tss --version`).

2. To use tss from Vim, add the `typescript-tools.vim` directory to your Vim's `rtp`.

  tss can be configured the same way as tsc, either via commandline options or
  via tsconfig.json files (since about TSv1.5). In both cases, only options that
  affect the language service have any effect. 

### vim interface to tss

  Needs Vim 7.3 (plus Python 2.7 with json lib): this repo includes a Vim filetype plugin
  for the `typescript` filetype, so just add the path to the repo to your Vim's
  runtime path and enable filetype plugins.
  ```
  filetype plugin on
  au BufRead,BufNewFile *.ts		setlocal filetype=typescript
  set rtp+=<your_path_here>/typescript-tools/
  ```

  Currently assumes that node is in path and that tss has been npm-installed globally.
  See top of file `ftplugin/typescript_tss.vim` for configuration options.

  In practice, you'll use `:TSSstarthere`, `:TSSend`, `:TSSreload`, `TSStype`, `TSSdef*`,
  as well as CTRL-X CTRL-O for insert mode completion. Also try the project (file) navigation
  commands. Sometimes, calling `:TSSshowErrors` directly can give enough error
  information for the current file -- eventually, you'll probably have to call
  `:TSSreload` to account for changes in dependencies.

  (TODO: vim plugin demo)

### Vim plugin usage tips

  1. the plugin collaborates with a tss server running in the background (via python and nodejs)
  2. the tss server will pick up source file dependencies (via import and references)
  3. start the tss server while editing your main source file (or your main reference file), by issueing `:TSSstarthere`
  4. now you can use the other commands (or `:TSSend`, to get rid of the background server), even while opening TS sources from the same project in different windows or tabs (but in the same Vim instance)

### Vim plugin commands

  ```
  " echo symbol/type of item under cursor
  command! TSSsymbol
  command! TSStype

  " jump to or show definition of item under cursor
  command! TSSdef
  command! TSSdefpreview
  command! TSSdefsplit
  command! TSSdeftab

  " create location list for references
  command! TSSreferences

  " update TSS with current file source
  command! TSSupdate

  " show TSS errors, with updated current file
  command! TSSshowErrors

  " for use as balloonexpr, symbol under mouse pointer
  " set balloonexpr=TSSballoon()
  " set ballooneval
  function! TSSballoon()

  " completions (omnifunc will be set for all *.ts files)
  function! TSScompleteFunc(findstart,base)

  " open project file, with filename completion
  command! -complete=customlist,TSSfile -nargs=1 TSSfile

  " show project file list in preview window
  command! TSSfiles

  " navigate to project file via popup menu
  command! TSSfilesMenu

  " create and open navigation menu for file navigation bar items
  command! TSSnavigation

  " navigate to items in project
  " 1. narrow down symbols via completion, modulo case/prefix/infix/camelCase
  " 2. offer remaining exact (modulo case) matches as a menu
  command! -complete=customlist,TSSnavigateToItems -nargs=1 TSSnavigateTo

  " reload project sources - will ask you to save modified buffers first
  command! TSSreload

  " start typescript service process (asynchronously, via python)
  command! -nargs=* TSSstart
  command! TSSstarthere

  " pass a command to typescript service, get answer
  command! -nargs=1 TSScmd call TSScmd(<f-args>,{})

  " check typescript service
  " (None: still running; <num>: exit status)
  command! TSSstatus

  " stop typescript service
  command! TSSend

  " sample keymap
  " (highjacking some keys otherwise used for tags,
  "  since we support jump to definition directly)
  function! TSSkeymap()
  ```
{ 
