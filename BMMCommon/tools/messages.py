
from rich import print as cprint
from rich.panel import Panel

try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


def colored(text, tint='white', attrs=[], end=None):
    '''
    A simple wrapper around rich.print
    '''
    if not is_re_worker_active():
        tint = tint.lower()
        this = f'[{tint}]{text}[/{tint}]'
        if end is not None:
            cprint(f'[{tint}]{text}[/{tint}]', end=end)
        else:
            cprint(f'[{tint}]{text}[/{tint}]')
    else:
        print(text)


def error_msg(text, end=None):
    '''Red text'''
    colored(text, 'red1', end=end)
def warning_msg(text, end=None):
    '''Yellow text'''
    colored(text, 'yellow', end=end)
def go_msg(text, end=None):
    '''Green text'''
    colored(text, 'green', end=end)
def url_msg(text, end=None):
    '''Underlined text, intended for URL decoration...'''
    colored(text, 'underline', end=end)
def bold_msg(text, end=None):
    '''Bright yellow text'''
    colored(text, 'yellow2', end=end)
def verbosebold_msg(text, end=None):
    '''Bright cyan text'''
    colored(text, 'cyan', end=end)
def list_msg(text, end=None):
    '''Dark cyan text'''
    colored(text, 'bold cyan', end=end)
def disconnected_msg(text, end=None):
    '''Purple text'''
    colored(text, 'magenta3', end=end)
def info_msg(text, end=None):
    '''Brown text'''
    colored(text, 'light_goldenrod2', end=end)
def cold_msg(text, end=None):
    '''Light blue text'''
    colored(text, 'blue', end=end)
def whisper(text, end=None):
    '''Light gray text'''
    colored(text, 'bold black', end=end)
        
def boxedtext(text, title='', color='green'):
    cprint(Panel(text, title=title, title_align='left', highlight=True, expand=False, border_style=color))
