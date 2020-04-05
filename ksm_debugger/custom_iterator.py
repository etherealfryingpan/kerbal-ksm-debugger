
def peek(byteiterator, num=1):
    return byteiterator.__peek__(num=num)

class ByteIterator:
    def __init__(self, bytelist: list):
        self.bytelist = bytelist
        self.curridx = 0

    def __next__(self):
        try:
            value = self.bytelist[self.curridx]
            self.curridx += 1
            return bytes([value])
        except IndexError:
            raise StopIteration
        
    def __peek__(self, num=1):
        
        try:
            values = []
            
            peekidx = self.curridx

            for i in range(num):
                value = self.bytelist[peekidx]
                values.append(value)
                peekidx += 1
            
            if len(values) == 1:
                return values[0]
            
            values = [bytes([val]) for val in values]

            return values
        except IndexError:
            raise StopIteration
    
    def __len__(self):
        return len(self.bytelist)