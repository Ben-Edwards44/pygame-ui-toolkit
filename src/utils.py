from inspect import signature


def find_num_params(func: callable) -> int:
    sig = signature(func)
    params = sig.parameters

    return len(params)


def call_func(func: callable, arg1: any) -> None:
    if func == None:
        return
    
    num_params = find_num_params(func)

    if num_params == 0:
        func()
    elif num_params == 1:
        func(arg1)
    else:
        raise Exception(f"Invalid number of parameters for {func}. {func} should accept 0 or 1 arguments.")