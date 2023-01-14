from .semanticerror import SemanticError
from ..syntactic import Parser
from ...expressions import *
from ...types import DataType
from ...resources import keywords as kw
from ...resources.messages import semanticerrors as err


class Analyzer(ExpressionVisitor):
    _id_tools: dict[ToolIdExpr, ToolExpr]

    def __init__(self, input_str: str):
        parser = Parser(input_str)
        self._ast = parser.parse()
        self._default_params = {kw.COLOUR, kw.THICKNESS}

        # обязательные параметры для инструмента
        self._required_tool_params = {
            DataType.POINT: {kw.POINT},
            DataType.SEGMENT: {kw.FROM, kw.TO},
            DataType.CURVE: {kw.CENTER, kw.RADIUS, kw.ANGLE_FROM, kw.ANGLE_TO},
            DataType.AREA: {kw.CONTENTS},
            DataType.LINE: {kw.CONTENTS},
            DataType.COUNTER: {kw.START, kw.STEP}
        }

        # допустимые параметры для инструмента
        self._tool_param_lists = {k: v.union(self._default_params) if k != DataType.POINT else v
                                  for k, v in self._required_tool_params.items()}

        # допустимые типы данных для параметров инструментов
        self._param_types = {
            kw.CONTENTS: {DataType.COMPOSITE},
            kw.FROM: {DataType.COORDS, DataType.POINT},
            kw.TO: {DataType.COORDS, DataType.POINT},
            kw.ANGLE_FROM: {DataType.INT},
            kw.ANGLE_TO: {DataType.INT},
            kw.POINT: {DataType.COORDS, DataType.TOOL_ID},
            kw.COLOUR: {DataType.COLOUR},
            kw.THICKNESS: {DataType.INT},
            kw.CENTER: {DataType.COORDS, DataType.POINT},
            kw.RADIUS: {DataType.INT},
            kw.START: {DataType.INT},
            kw.STEP: {DataType.INT}
        }

        # таблица для хранения объектов, связанных с идентификаторами
        self._id_tools = dict()

        # допустимые типы данных для частей составного инструмента
        self._part_types = {DataType.SEGMENT, DataType.CURVE}

    def analyze(self) -> bool:
        try:
            self.visit_program(self._ast)
            return True
        except SemanticError:
            raise

    def visit_program(self, expr: ProgramExpr) -> None:
        expr.objects.accept(self)
        expr.tools.accept(self)
        expr.processing.accept(self)

    def visit_object_block(self, expr: ObjectBlockExpr) -> None:
        obj: ObjectExpr
        for obj in expr.items:
            obj.accept(self)
            obj_id = obj.id.value
            if obj_id in expr.attrs.names:
                raise SemanticError(err.duplicated_object_id())
            expr.attrs.names.add(obj_id)

    def visit_object_id(self, expr: ObjectIdExpr) -> None:
        expr.attrs.name = expr.value

    def visit_object(self, expr: ObjectExpr) -> None:
        expr.id.accept(self)

    def visit_tool_block(self, expr: ToolBlockExpr) -> None:
        tool: ToolExpr
        for tool in expr.items:
            tool.accept(self)
            tool_id = tool.attrs.name
            if tool_id in expr.attrs.names:
                raise SemanticError(err.duplicated_tool_id())
            expr.attrs.names.add(tool_id)

    def _check_composite_shape(self, tool_type: DataType, composite: ToolPartsExpr) -> bool:
        points = self._get_part_endpoints(composite)
        match tool_type:
            case DataType.AREA:
                if len(points) != len(composite.parts):
                    raise SemanticError(err.unconnected_area())
            case DataType.LINE:
                if len(points) - 1 != len(composite.parts):
                    raise SemanticError(err.unconnected_line())
            case _:
                raise ValueError(err.unsupported_tool_part_type())

    def _get_part_endpoints(self, composite: ToolPartsExpr) -> set[AtomicExpr]:
        points: set[AtomicExpr] = set()
        parts = {
            DataType.SEGMENT: set(),
            DataType.CURVE: set()
        }
        part: SegmentExpr | CurveExpr | ToolIdExpr
        for part in composite.parts:
            # the fact that we need to check the expression type here is kind of annoying
            if isinstance(part, ToolIdExpr):
                part = self._get_part_by_id(part)

            existing_parts_of_same_type = parts[part.attrs.datatype]
            if part in existing_parts_of_same_type:
                raise SemanticError(err.duplicated_tool_part())
            existing_parts_of_same_type.add(part)
            points.add(part.start)
            points.add(part.end)
        return points

    def _get_part_by_id(self, part: ToolIdExpr):
        if part.value not in self._id_tools.keys():
            raise SemanticError(err.undeclared_tool_part())
        return self._id_tools[part.value]

    def visit_tool_id(self, expr: ToolIdExpr) -> None:
        expr.attrs.name = expr.value
        if expr.value in self._id_tools.keys():
            # if the expression that's referred to by the variable is in the table,
            # then it already has its attributes filled out
            # so accessing the datatype property is okay
            expr.attrs.datatype = self._id_tools[expr.value].attrs.datatype

    def visit_tool_parts(self, expr: ToolPartsExpr) -> None:
        expr.attrs.datatype = DataType.COMPOSITE
        item: ToolExpr | ToolIdExpr
        for item in expr.parts:
            item.accept(self)
            if not item.attrs.datatype:
                # anonymous part declarations will have their type assigned in accept()
                # and declared variables will get the type from the table,
                # so if the item does not have a type attached to it at this point
                # it can only be an undeclared variable
                raise SemanticError(err.undeclared_tool_part())
            if item.attrs.datatype not in {DataType.SEGMENT, DataType.CURVE}:
                raise SemanticError(err.unsupported_tool_part_type())
            expr.attrs.value_types.add(item.attrs.datatype)

    def _visit_optional_id(self, expr: ToolExpr) -> None:
        if expr.id:
            expr.id.accept(self)
            expr.attrs.name = expr.id.attrs.name
            # add expr to symbol table
            self._id_tools[expr.attrs.name] = expr

    def _run_tool_checks(self, expr: ToolExpr) -> None:
        for param_name, param_value in expr.params.items():
            if param_name not in self._tool_param_lists[expr.attrs.datatype]:
                raise SemanticError(err.unexpected_parameter_name(param_name))
            expr.attrs.filled_params.add(param_name)

            param_value.accept(self)

            if param_value.attrs.name:
                if param_value.attrs.name == expr.attrs.name:
                    raise SemanticError(err.self_id_as_param_value())
                elif param_value.attrs.name not in self._id_tools:
                    raise SemanticError(err.undeclared_tool_variable(param_value.attrs.name))

            if param_value.attrs.datatype not in self._param_types[param_name]:
                raise SemanticError(err.parameter_type_mismatch())

            if param_value.attrs.datatype == DataType.COMPOSITE:
                self._check_composite_shape(expr.attrs.datatype, param_value)
        if not expr.attrs.filled_params.issuperset(self._required_tool_params[expr.attrs.datatype]):
            raise SemanticError(err.missing_required_tool_param())

    def _visit_tool(self, expr: ToolExpr, datatype: DataType) -> None:
        self._visit_optional_id(expr)
        expr.attrs.datatype = datatype
        self._run_tool_checks(expr)

    def visit_point(self, expr: PointExpr) -> None:
        self._visit_tool(expr, DataType.POINT)

    def visit_segment(self, expr: SegmentExpr) -> None:
        self._visit_tool(expr, DataType.SEGMENT)

    def visit_curve(self, expr: CurveExpr) -> None:
        self._visit_tool(expr, DataType.CURVE)

    def visit_area(self, expr: AreaExpr) -> None:
        self._visit_tool(expr, DataType.AREA)

    def visit_line(self, expr: LineExpr) -> None:
        self._visit_tool(expr, DataType.LINE)

    def visit_counter(self, expr: CounterExpr) -> None:
        self._visit_tool(expr, DataType.COUNTER)

    def visit_atomic(self, expr: AtomicExpr) -> None:
        expr.attrs.datatype = expr.type

    def visit_processing_block(self, expr: ProcessingBlockExpr) -> None:
        pass

    def visit_processing_id(self, expr: ProcessingIdExpr) -> None:
        expr.attrs.name = expr.value

    def visit_condition(self, expr: ConditionExpr) -> None:
        pass

    def visit_declaration(self, expr: DeclarationExpr) -> None:
        pass

    def visit_action(self, expr: ActionExpr) -> None:
        pass

    def visit_action_id(self, expr: ActionIdExpr) -> None:
        pass

    def visit_event(self, expr: EventExpr) -> None:
        pass

    def visit_event_id(self, expr: EventIdExpr) -> None:
        pass

    def visit_binary(self, expr: BinaryExpr) -> None:
        pass
