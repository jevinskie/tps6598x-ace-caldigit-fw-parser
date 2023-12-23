import construct_typed


class EnumBase(construct_typed.EnumBase):
    def __str__(self) -> str:
        return repr(self)
