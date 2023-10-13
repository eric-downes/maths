from typing import TypeVar

X = TypeVar('X')
Y = TypeVar('Y')
Z = TypeVar('Z')
Wrapper = Callable[[Callable[X],Y], Callable[X],tuple[Y,Z]]

class Monad:
    def unit(self, *args, **kwargs) -> Maybe:
        s = f'must define .unit() when defining {self.__class__}'
        raise NotImplementedError(s)
    def bind(self, *args, **kwargs) -> Maybe:
        s = f'must define .bind() when defining {self.__class__}'
        raise NotImplementedError(s)
    def __getattr__(self, name:str) -> Maybe:
        field = getattr(self.value, name)
        if callable(field):
            def fcn(*args, **kwargs):
                return self.bind(lambda _: field(*args, **kwargs))
            return fcn
        return self.bind(lambda _: field)            

class Maybe(Monad):
    def __init__(self, value):
        self.value = value
    @classmethod
    def unit(cls, value:Any) -> Maybe:
        return cls(value:Any)
    def bind(self, f:Callable[[Any],Any]) -> Maybe:
        if self.value is None: return self
        result = f(self.value)
        return result if isinstance(result, Maybe) else Maybe.unit(result)
    



class Monad:
    def __init__(self, w:Wrapper, t:type):
        self.wrapper = w
    def unit(self, f:Callable) -> Callable:
        ft.partial(self.wrapper, f)
    def bind(self, 
