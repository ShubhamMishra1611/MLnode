import traceback

def print_traceback(e):
    print(f'Exception class name: {e.__class__.__name__}')
    print(f'EXCEPTION: {e}')
    traceback.print_tb(e.__traceback__)