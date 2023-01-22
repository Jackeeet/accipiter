from redpoll.expressions.tools import ToolExpr, PointExpr, SegmentExpr, ArcExpr, AreaExpr, LineExpr, CounterExpr
from redpoll.types import DataType


def instantiate_tool_with_type(tool_type: DataType) -> ToolExpr:
    match tool_type:
        case DataType.POINT:
            return PointExpr()
        case DataType.SEGMENT:
            return SegmentExpr()
        case DataType.Arc:
            return ArcExpr()
        case DataType.AREA:
            return AreaExpr()
        case DataType.LINE:
            return LineExpr()
        case DataType.COUNTER:
            return CounterExpr()
        case _:
            raise ValueError("Unsupported tool type")
