from inspect import signature
from pygame import font


def find_num_params(func: callable) -> int:
    sig = signature(func)
    params = sig.parameters

    return len(params)


def call_func(func: callable, *args) -> None:
    if func == None:
        return
    
    num_params = find_num_params(func)

    if num_params == 0:
        func()
    elif num_params == 1:
        func(args[0])
    elif num_params == 2:
        func(args[0], args[1])
    else:
        raise Exception(f"Invalid number of parameters for {func}. {func} should accept 0, 1 or 2 arguments.")
    

def update_font_attrs(obj: object, text: str, font_colour: tuple[int], font_name: str, font_size: int) -> None:
    obj.text = text
    obj.font_colour = font_colour

    obj.font = font.Font(font_name, font_size)