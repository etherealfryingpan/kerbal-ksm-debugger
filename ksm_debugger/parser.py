from ksm_debugger.logger import log, init_logs
from ksm_debugger.custom_iterator import ByteIterator, peek
from ksm_debugger.conversion_tools import *
import struct

class Argument:
    """A class that represents an argument that is used in CodeParts"""

    def __init__(self, type: str, index: int, value=None):
        """Constructor, type is required, but value is not"""
        self.type = type
        self.value = value
        self.index = index
    
    @staticmethod
    def parse_arg(byte_iter):
        """A function to parse an argument from the provided byte iterator"""
        id_ = btoi_l(next(byte_iter))

        index = byte_iter.curridx - 1

        if id_ == 0:
            return Argument('NULL', index)
        elif id_ == 1:
            val = btob(next(byte_iter))

            return Argument('BOOL', index, value=val)
        elif id_ == 2:
            val = btoi_l(next(byte_iter))

            return Argument('BYTE', index, value=val)
        elif id_ == 3:
            val = btoh_l(read_bytes(byte_iter, 2))

            return Argument('SWORD', index, value=val)
        elif id_ == 4:
            val = btow_l(read_bytes(byte_iter, 2))

            return Argument('WORD', index, value=val)
        elif id_ == 5:
            val = btof_l(read_bytes(byte_iter, 4))

            return Argument('FLOAT', index, value=val)
        elif id_ == 6:
            val = btod_l(read_bytes(byte_iter, 8))

            return Argument('DOUBLE', index, value=val)
        elif id_ == 7:
            str_len = btoi_l(next(byte_iter))

            str_data = read_bytes(byte_iter, str_len)

            val = btos(str_data)

            return Argument('STRING', index, value=val)
        elif id_ == 8:
            return Argument('ARG_MARKER', index)
        elif id_ == 9:
            val = btol_l(read_bytes(byte_iter, 4))

            return Argument('SCALAR_INT_VALUE', index, value=val)
        elif id_ == 10:
            val = btod_l(read_bytes(byte_iter, 8))

            return Argument('SCALAR_DOUBLE_VALUE', index, value=val)
        elif id_ == 11:
            val = btob(next(byte_iter))

            return Argument('BOOL_VALUE', index, value=val)
        elif id_ == 12:
            str_len = btoi_l(next(byte_iter))

            str_data = read_bytes(byte_iter, str_len)

            val = btos(str_data)

            return Argument('STRING_VALUE', index, value=val)
    
    def __repr__(self):
        if self.value is None:
            return '<{}>'.format(self.type)
        else:
            if self.type in ['STRING', 'STRING_VALUE']:
                return '<{},"{}">'.format(self.type, self.value)
            else:
                return '<{},{}>'.format(self.type, self.value)

class OpCode:
    """Represents a KML opcode"""

    def __init__(self, code: int):
        """Creates an OpCode object using the provided opcode"""

        self.code = code

        self.opcode_lookup = [
            0x00, 'BOGUS', 0,
            0x25, 'DELIMITER', 0,
            0x31, 'EOF', 0,
            0x32, 'EOP', 0,
            0x33, 'NOP', 0,
            0x34, 'STORE', 1,
            0x35, 'UNSET', 0,
            0x36, 'GETMEMBER', 1,
            0x37, 'SETMEMBER', 1,
            0x38, 'GETINDEX', 0,
            0x39, 'SETINDEX', 0,
            0x3A, 'BRANCHFALSE', 1,
            0x3B, 'JUMP', 1,
            0x3C, 'ADD', 0,
            0x3D, 'SUB', 0,
            0x3E, 'MULT', 0,
            0x3F, 'DIV', 0,
            0x40, 'POW', 0,
            0x41, 'GT', 0,
            0x42, 'LT', 0,
            0x43, 'GTE', 0,
            0x44, 'LTE', 0,
            0x45, 'EQ', 0,
            0x46, 'NE', 0,
            0x47, 'NEGATE', 0,
            0x48, 'BOOL', 0,
            0x49, 'NOT', 0,
            0x4A, 'AND', 0,
            0x4B, 'OR', 0,
            0x4C, 'CALL', 2,
            0x4D, 'RETURN', 1,
            0x4E, 'PUSH', 1,
            0x4F, 'POP', 0,
            0x50, 'DUP', 0,
            0x51, 'SWAP', 0,
            0x52, 'EVAL', 0,
            0x53, 'ADDTRIGGER', 2,
            0x54, 'REMOVETRIGGER', 0,
            0x55, 'WAIT', 1,
            0x56, 'ENDWAIT', 0,
            0x57, 'GETMETHOD', 1,
            0x58, 'STORELOCAL', 1,
            0x59, 'STOREGLOBAL', 1,
            0x5A, 'PUSHSCOPE', 2,
            0x5B, 'POPSCOPE', 1,
            0x5C, 'STOREEXIST', 1,
            0x5D, 'PUSHDELEGATE', 2,
            0x5E, 'BRANCHTRUE', 1,
            0x5F, 'EXISTS', 0,
            0x60, 'ARGBOTTOM', 0,
            0x61, 'TESTARGBOTTOM', 0,
            0x62, 'TESTCANCELLED', 0,
            0xce, 'PUSHRELOCATELATER', 1,
            0xcd, 'PUSHDELEGATERELOCATELATER', 2,
            0xf0, 'LABELRESET', 1
        ]

        self.name = self.lookup_name(code)
        self.num_args = self.lookup_num_args(code)
    
    def lookup_name(self, code: int) -> str:
        """Takes an integer of the opcode, and returns the name of the instruction"""

        name = 'BOGUS'

        try:
            name = self.opcode_lookup[self.opcode_lookup.index(code) + 1]
        except IndexError:
            pass

        return name
    
    def lookup_num_args(self, code: int) -> int:
        """Takes an integer of the opcode, and returns the number of arguments that it requires"""

        num_args = None

        try:
            num_args = self.opcode_lookup[self.opcode_lookup.index(code) + 2]
        except IndexError:
            pass

        return num_args
    
    def __repr__(self):
        return '{0.name}, {0.code}, {0.num_args}'.format(self)

class Instruction:
    """Represents a KML instruction"""

    def __init__(self, code: OpCode, arguments=[]):
        """Creates an Instruction object, only code is required. Arguments should be a list of integer indexes of the argument section"""
        self.code = code
        self.arguments = arguments

    @staticmethod
    def parse_instr(num_arg_index_bytes: int, byte_iter):
        """Parses an Instruction from the provided byte iterator"""

        opcode = OpCode(btoi_l(next(byte_iter), signed=False))

        num_args = opcode.num_args

        arguments = []

        for i in range(num_args):

            arg = read_bytes(byte_iter, num_arg_index_bytes)

            arg_index = btoi_l(arg, signed=False)

            arguments.append(arg_index)
        
        return Instruction(opcode, arguments)
    
    def __repr__(self):

        arg_section = ''

        for i in range(len(self.arguments)):
            arg_section += ', {}'.format(self.arguments[i])
        
        return self.code.name + arg_section

def check_header(byte_iter):
    
    next_two = peek(byte_iter, num=2)

    headers = [[b'%', b'F'], [b'%', b'I'], [b'%', b'M'], [b'%', b'D']]

    return next_two in headers

class CodePart:
    """Represents a KML codepart"""

    def __init__(self, function_section: list, init_section: list, main_section: list):
        """Requires a list of Instructions for each subsection"""

        self.function_section = function_section
        self.init_section = init_section
        self.main_section = main_section

    @staticmethod
    def parse_codepart(num_arg_index_bytes: int, byte_iter):

        try:
            assert next(byte_iter) == b'%' and next(byte_iter) == b'F'

            log('Parsing function section')

            # Parse function section

            function_section = CodePart.parse_section(num_arg_index_bytes, byte_iter)

            assert next(byte_iter) == b'%' and next(byte_iter) == b'I'

            log('Parsing initialization section')

            # Parse initializtion section

            init_section = CodePart.parse_section(num_arg_index_bytes, byte_iter)

            assert next(byte_iter) == b'%' and next(byte_iter) == b'M'

            log('Parsing main section')

            # Parse main section

            main_section = CodePart.parse_section(num_arg_index_bytes, byte_iter)

            log('Done parsing\n')

            return CodePart(function_section, init_section, main_section)

        except AssertionError:
            log('Codepart sections in mismatched order. Exiting.')

            exit(1)

    @staticmethod
    def parse_section(num_arg_index_bytes: int, byte_iter) -> list:
        """Parses a code section"""

        instructions = []

        ch = check_header(byte_iter)

        while not ch:

            instruction = Instruction.parse_instr(num_arg_index_bytes, byte_iter)

            instructions.append(instruction)

            ch= check_header(byte_iter)
        
        return instructions
    
    def __repr__(self):

        rep = ''

        rep += 'Function section:\n'

        count = 1
        for inst in self.function_section:
            rep += ' {}\t{}\n'.format(count, inst)
            count += 1
        
        rep += 'Initialization section:\n'

        count = 1
        for inst in self.init_section:
            rep += ' {}\t{}\n'.format(count, inst)
            count += 1
        
        rep += 'Main section:\n'

        count = 1
        for inst in self.main_section:
            rep += ' {}\t{}\n'.format(count, inst)
            count += 1
        
        rep += '\n'

        return rep

def parse_arg_section(byte_iter) -> (int, list):
    """A function to parse the entire argument section

    Returns
    ------
    num_arg_index_bytes: The number of bytes required to index the argument section
    arg_list: A list of Argument objects
    """

    try:
        assert next(byte_iter) == b'%' and next(byte_iter) == b'A'
    except:
        log('Invalid argument section, exiting..')
        exit(1)
    
    num_arg_index_bytes = btoi_l(next(byte_iter))

    log('Argument index size: {} {}'.format(num_arg_index_bytes, 'byte' if num_arg_index_bytes == 1 else 'bytes' ))
    
    peek_1, peek_2 = peek(byte_iter, num=2)

    arg_list = []

    while not (peek_1 == b'%' and peek_2 == b'F'):

        arg = Argument.parse_arg(byte_iter)
        arg_list.append(arg)

        peek_1, peek_2 = peek(byte_iter, num=2)
    
    log('Argument section parsed:')

    for arg in arg_list:
        log('{0.index}\t{0}'.format(arg))
    
    log('')

    return num_arg_index_bytes, arg_list

def parse_code_parts(byte_iter, num_arg_index_bytes: int):
    """A function that returns a list of parsed CodePart objects"""

    peek_1, peek_2 = peek(byte_iter, num=2)

    codeparts = []

    while not (peek_1 == b'%' and peek_2 == b'D'):

        codepart = CodePart.parse_codepart(num_arg_index_bytes, byte_iter)

        codeparts.append(codepart)

        peek_1, peek_2 = peek(byte_iter, num=2)

    return codeparts

class DebugLine:
    def __init__(self, line_number: int, ranges: list):
        self.line_number = line_number
        self.ranges = ranges

    @staticmethod
    def parse_debug_line(byte_iter, index_bytes: int):

        line_number = btoh_l(read_bytes(byte_iter, 2))

        num_ranges = btoi_l(next(byte_iter))

        ranges = []

        for i in range(num_ranges):
            range_start = btoi_b(read_bytes(byte_iter, index_bytes))
            range_end = btoi_b(read_bytes(byte_iter, index_bytes))

            ranges.append([range_start, range_end])
        
        return DebugLine(line_number, ranges)
    
    def __repr__(self):
        
        rep = ''

        rep += 'Line {} | '.format(str(self.line_number))

        for r in self.ranges:
            rep += '[{}..{}],'.format(r[0], r[1])
        
        if rep[-1] == ',':
            rep = rep[:-1]

        return rep

class Debug:
    def __init__(self, debug_lines: list):
        self.debug_lines = debug_lines

    @staticmethod
    def parse_debug(byte_iter):

        next(byte_iter) # %
        next(byte_iter) # D

        num_debug_index_bytes = btoi_l(next(byte_iter))

        debug_lines = []

        try:
            while True:
                debug_line = DebugLine.parse_debug_line(byte_iter, num_debug_index_bytes)

                debug_lines.append(debug_line)
        except StopIteration:
            pass

        return Debug(debug_lines)
    
    def __repr__(self):

        rep = 'Debug section:\n'

        for line in self.debug_lines:
            rep += '\t{}\n'.format(line)
        
        rep += '\n'

        return rep

def parse_debug_section(byte_iter):
    return Debug.parse_debug(byte_iter)