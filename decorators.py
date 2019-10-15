from functools import wraps

def param(param_type):
    def decorator(f):
        param_fields = {
            key for key, value in param_type.__dataclass_fields__.items() if value.init
        }

        @wraps(f)
        def wrapper(*args, **kwargs):
            params_values = {}
            for field in param_fields:
                if field in kwargs:
                    params_values[field] = kwargs.pop(field)

            param_passed = False
            if args and isinstance(args[-1], param_type):
                param_passed = True

            if param_passed and params_values:
                raise TypeError(
                    "Either {param_type.__name__} or its parameters expected, "
                    "but both passed."
                )
            if param_passed and not params_values:
                return f(*args, **kwargs)
            param_value = param_type(**params_values)
            return f(*args, param_value, **kwargs)

        additional_docs = (
            f"\n\nTip:\n\tIt is possible to pass the {param_type.__name__}"
            " parameters to the function as keyword arguments."
            "\n\tAccepted keyword arguments to construct the parameter"
            f" object are: {tuple(param_fields)}"
        )
        if wrapper.__doc__:
            wrapper.__doc__ += additional_docs

        return wrapper

    return decorator
