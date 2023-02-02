from redpoll.expressions.tools import ToolExpr, PointExpr, SegmentExpr, ArcExpr, AreaExpr, LineExpr, CounterExpr
from redpoll.types import DataType


def instantiate_tool_with_type(tool_type: DataType, line: int, pos: int) -> ToolExpr:
    match tool_type:
        case DataType.POINT:
            return PointExpr(line, pos)
        case DataType.SEGMENT:
            return SegmentExpr(line, pos)
        case DataType.ARC:
            return ArcExpr(line, pos)
        case DataType.AREA:
            return AreaExpr(line, pos)
        case DataType.LINE:
            return LineExpr(line, pos)
        case DataType.COUNTER:
            return CounterExpr(line, pos)
        case _:
            raise ValueError("Unsupported tool type")
