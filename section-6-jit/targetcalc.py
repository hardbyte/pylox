from rpython.rlib import rfile

from vm import VM, IntepretResultToName, IntepretResultCode

LINE_BUFFER_LENGTH = 4096


def repl():
    stdin, stdout, stderr = rfile.create_stdio()
    vm = VM()

    while True:
        stdout.write("> ")
        source = stdin.readline(LINE_BUFFER_LENGTH).strip()
        if not source:
            break

        vm.interpret(source)

    return 0


def runFile(filename):
    source = read_file(filename)
    vm = VM(debug=False)
    try:
        result = vm.interpret(source)
        print IntepretResultToName[result]
        if result == IntepretResultCode.INTERPRET_COMPILE_ERROR:
            print "Compile error"
        elif result == IntepretResultCode.INTERPRET_RUNTIME_ERROR:
            print "Runtime error"
    except ValueError:
        print "Unhandled exception in runFile"


def read_file(filename):
    try:
        file = rfile.create_file(filename, 'r')
    except IOError:
        print "Error opening file"
        raise SystemExit(74)
    source = file.read()
    return source


def entry_point(argv):
    if len(argv) > 1:
        runFile(argv[1])
    elif len(argv) == 1:
        repl()
    else:
        print "Usage: calc [path]"
        raise SystemExit(64)
    return 0


def target(driver, *args):
    driver.exe_name = "calc"
    return entry_point, None


if __name__ == '__main__':
    entry_point([])