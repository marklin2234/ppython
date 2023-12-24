class Error:
    def __init__(self, error_name, start, end, details):
        self.error_name = error_name
        self.start = start
        self.end = end
        self.details = details

    def __repr__(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'    File {self.start.fn}, line {self.start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.start.ftxt, self.start, self.end)
        return result
    
class IllegalCharError(Error):
    def __init__(self, start, end, details):
        super().__init__('Illegal Character Error', start, end, details)

class InvalidSyntaxError(Error):
    def __init__(self, start, end, details):
        super().__init__('Invalid Syntax', start, end, details)

class RTError(Error):
    def __init__(self, start, end, details, context):
        super().__init__('Runtime Error', start, end, details)
        self.context = context
    
    def __repr__(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}\n'
        result += '\n\n' + string_with_arrows(self.start.ftxt, self.start, self.end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.start
        ctx = self.context

        while ctx:
            result += f'    File {pos.fn}, line {pos.ln + 1}, in {ctx.display_name}\n'
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return 'Traceack (most recent call last): \n' + result

def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)
    return result.replace('\t', '')