import argparse

log_loc = 'stdout'

def log(s, end='\n'):
    """Logs to either stdout or a file"""

    if log_loc == 'stdout':
        print(s, end=end)
    else:
        with open(log_loc, 'a') as f:
            f.write('{}{}'.format(s, end))

def init_logs(n: argparse.Namespace):
    """Initializes everything needed to use log()"""

    global log_loc

    if n.output_file:
        log_loc = n.output_file
        
        # Overwrites / creates the file
        with open(log_loc, 'w') as f:
            pass
    
    print('Logging output to: {}\n'.format(log_loc))