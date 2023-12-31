import traceback

def print_traceback(e):
    print(f'EXCEPTION: {e}')
    traceback.print_tb(e.__traceback__)