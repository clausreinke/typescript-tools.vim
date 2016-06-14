import vim
import subprocess
import json
import logging, platform

TSS_LOG_FILENAME='tsstrace.log'
traceFlag = False

class TSSnotrunning:
  def poll(self):
    return 0

tss = TSSnotrunning()
TSS_NOT_RUNNING_MSG='TSS not running - start with :TSSstarthere on main file'
TSS_MDN = "https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/"

def tss_start(cmd):
    global tss
    print(cmd)
    tss = subprocess.Popen(cmd
                          ,bufsize=0
                          ,stdin=subprocess.PIPE
                          ,stdout=subprocess.PIPE
                          ,stderr=subprocess.PIPE
                          ,shell=platform.system()=="Windows"
                          ,universal_newlines=True)

    prompt = tss.stdout.readline()
    sys.stdout.write(prompt)

def tss_trace(flag):
    global traceFlag
    if flag=='on':
      traceFlag = True
      logging.basicConfig(filename=TSS_LOG_FILENAME,level=logging.DEBUG)
    else:
      traceFlag = False
      logger = logging.getLogger()
      logger.handlers[0].stream.close()
      logger.removeHandler(logger.handlers[0])


def tss_cmd(cmd,opts):
    (row,col) = vim.current.window.cursor
    filename  = vim.current.buffer.name
    colArg    = opts['col'] if ('col' in opts) else str(col+1)

    if traceFlag:
        logging.debug(tss)

    if tss.poll()==None:
      if ('rawcmd' in opts):
        request = cmd
      else:
        request = cmd+' '+str(row)+' '+colArg+' '+filename

      if traceFlag:
        logging.debug(request)

      tss.stdin.write(request+'\n')

      if ('lines' in opts):
        for line in opts['lines']:
          tss.stdin.write(line+'\n')

      answer = tss.stdout.readline()

      if traceFlag:
        if ('lines' in opts):
          for line in opts['lines']:
            logging.debug(line)
        logging.debug(answer)

      try:
        result = json.dumps(json.loads(answer,parse_constant=str))
      except:
        result = '"null"'

    else:
      result = '"'+TSS_NOT_RUNNING_MSG+'"'

    vim.command("let null = 'null'")
    vim.command("let true = 'true'")
    vim.command("let false = 'false'")
    vim.command("let result = "+result)

def tss_status():
    rest = tss.poll()
    vim.command("return "+json.dumps(str(rest)))

def tss_end():
    if tss.poll()==None:
      rest = tss.communicate('quit')[0]
      sys.stdout.write(rest)
    else:
      sys.stdout.write(TSS_NOT_RUNNING_MSG+'\n')

