from abc import ABC

from redpoll.expressions import BlockItemExpr, ToolIdExpr, ParamsExpr


class ToolExpr(BlockItemExpr, ABC):
    id: ToolIdExpr | None
    params: dict[str, ParamsExpr]

    def __init__(self, name: ToolIdExpr = None) -> None:
        super().__init__()
        self.id = name
        self.params = dict()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ToolExpr):
            return self.id == o.id
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    # @staticmethod
    # def instantiate_with_type(tool_type: DataType):
    #     match tool_type:
    #         case DataType.POINT:
    #             return PointExpr()
    #         case DataType.SEGMENT:
    #             return SegmentExpr()
    #         case DataType.CURVE:
    #             return CurveExpr()
    #         case DataType.AREA:
    #             return AreaExpr()
    #         case DataType.LINE:
    #             return LineExpr()
    #         case DataType.COUNTER:
    #             return CounterExpr()
    #         case _:
    #             raise ValueError("Unsupported tool type")
