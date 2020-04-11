import argparse
import gzip
import ksm_debugger.parser as par
from ksm_debugger.logger import log, init_logs
from ksm_debugger.custom_iterator import ByteIterator, peek

def main():
    """The main function that is run"""
    n = parse_args()
    init_logs(n)

    content = read_ksm(n.input_file)

    byte_iter = ByteIterator(content)

    num_arg_index_bytes, arguments = par.parse_arg_section(byte_iter)

    code_parts = par.parse_code_parts(byte_iter, num_arg_index_bytes)

    debug_part = par.parse_debug_section(byte_iter)

    for code_part in code_parts:
        log(code_part)

    log(debug_part)

def is_ksm(content: bytes) -> bool:
    """Returns true if the file contains k3XE as the first 4 bytes, indicating it is a ksm file"""
    return content[:4] == b'k\x03XE'

def read_ksm(path: str) -> bytes:
    """Reads the ksm file specified by path. Errors are caught and the program can exit in this function."""
    contents = None

    try:
        with gzip.open(path, 'rb') as f:
            contents = f.read()
        
        log('File read: {}'.format(path))

        assert is_ksm(contents)
    except FileNotFoundError:
        log('Invalid file path, please try again.')
        exit(1)
    except (OSError, AssertionError):
        log('Not a valid ksm file, exiting.')
        exit(1)
    
    return contents[4:]

def parse_args() -> argparse.Namespace:
    """A function that returns the parsed arguments to the program
    
    Returns
    -------
    A namespace containing the processed arguments
    """

    parser = argparse.ArgumentParser(prog='KSM Debugger', description='A tool for debugging compiled kOS code.')

    parser.add_argument(dest='input_file', action='store', help='The path to a valid .ksm file')
    parser.add_argument('-o', '--output', dest='output_file', action='store', required=False, help='The path to an output file instead of outputting to stdout')

    return parser.parse_args()

if __name__ == "__main__":
    main()