from redpoll.analyzer.semantic.semanticerror import SemanticError
from redpoll.analyzer.syntactic import Parser
from redpoll.expressions import *
from redpoll.resources.lookup import action, event, params, tool
from redpoll.resources.messages import semanticerrors as err
from redpoll.types import DataType


class Analyzer(ExpressionVisitor):
    _id_tools: dict[ToolIdExpr, ToolExpr]

    def __init__(self, input_str: str):
        parser = Parser(input_str)
        self._ast = parser.parse()
        # таблица для хранения объектов, связанных с идентификаторами
        self._id_tools = dict()

    def analyze(self) -> ProgramExpr:
        try:
            self.visit_program(self._ast)
            return self._ast
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
                raise SemanticError(expr, err.duplicated_object_id())
            expr.attrs.names.add(obj_id)

    def visit_object_id(self, expr: ObjectIdExpr) -> None:
        expr.attrs.name = expr.value
        expr.attrs.datatype = DataType.OBJECT_ID

    def visit_object(self, expr: ObjectExpr) -> None:
        expr.id.accept(self)

    def visit_tool_block(self, expr: ToolBlockExpr) -> None:
        t: ToolExpr
        for t in expr.items:
            t.accept(self)
            tool_id = t.attrs.name
            if tool_id in expr.attrs.names:
                raise SemanticError(expr, err.duplicated_tool_id())
            expr.attrs.names.add(tool_id)

    def _check_composite_shape(self, tool_type: DataType, composite: ToolPartsExpr) -> bool:
        points = self._get_part_endpoints(composite)
        match tool_type:
            case DataType.AREA:
                if len(points) != len(composite.parts):
                    raise SemanticError(composite, err.unconnected_area())
            case DataType.LINE:
                if len(points) - 1 != len(composite.parts):
                    raise SemanticError(composite, err.unconnected_line())
            case _:
                raise ValueError(err.unsupported_tool_part_type())
        return True

    def _get_part_endpoints(self, composite: ToolPartsExpr) -> set[AtomicExpr]:
        points: set[AtomicExpr] = set()
        parts = {
            DataType.SEGMENT: set(),
            DataType.ARC: set()
        }
        part: SegmentExpr | ArcExpr | ToolIdExpr
        for part in composite.parts:
            # the fact that we need to check the expression type here is kind of annoying
            if isinstance(part, ToolIdExpr):
                part = self._get_part_by_id(part)

            existing_parts_of_same_type = parts[part.attrs.datatype]
            if part in existing_parts_of_same_type:
                raise SemanticError(part, err.duplicated_tool_part())
            existing_parts_of_same_type.add(part)

            start = self._id_tools[part.start.value].coords if isinstance(part.start, ToolIdExpr) else part.start
            end = self._id_tools[part.end.value].coords if isinstance(part.end, ToolIdExpr) else part.end
            points.add(start)
            points.add(end)
        return points

    def _get_part_by_id(self, part: ToolIdExpr):
        if part.value not in self._id_tools.keys():
            raise SemanticError(part, err.undeclared_tool_part())
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
                raise SemanticError(expr, err.undeclared_tool_part())
            if item.attrs.datatype not in {DataType.SEGMENT, DataType.ARC}:
                raise SemanticError(expr, err.unsupported_tool_part_type())
            expr.attrs.value_types.add(item.attrs.datatype)

    def _visit_optional_id(self, expr: ToolExpr) -> None:
        if expr.id:
            expr.id.accept(self)
            expr.attrs.name = expr.id.attrs.name
            # add expr to symbol table
            self._id_tools[expr.attrs.name] = expr

    def _run_tool_checks(self, expr: ToolExpr) -> None:
        for param_name, param_value in expr.params.items():
            if param_name not in tool.param_lists[expr.attrs.datatype]:
                raise SemanticError(expr, err.unexpected_parameter_name(param_name))
            expr.attrs.filled_params.add(param_name)

            param_value.accept(self)

            if param_value.attrs.name:
                if param_value.attrs.name == expr.attrs.name:
                    raise SemanticError(expr, err.self_id_as_arg())
                elif param_value.attrs.name not in self._id_tools:
                    raise SemanticError(
                        expr, err.undeclared_tool_variable(param_value.attrs.name)
                    )

            if param_value.attrs.datatype not in tool.param_types[param_name]:
                raise SemanticError(expr, err.arg_type_mismatch())

            if param_value.attrs.datatype == DataType.COMPOSITE:
                param_value: ToolPartsExpr
                self._check_composite_shape(expr.attrs.datatype, param_value)
        if not expr.attrs.filled_params.issuperset(tool.required_params[expr.attrs.datatype]):
            raise SemanticError(expr, err.missing_required_tool_arg())

    def _visit_tool(self, expr: ToolExpr, datatype: DataType) -> None:
        self._visit_optional_id(expr)
        expr.attrs.datatype = datatype
        self._run_tool_checks(expr)

    def visit_point(self, expr: PointExpr) -> None:
        self._visit_tool(expr, DataType.POINT)

    def visit_segment(self, expr: SegmentExpr) -> None:
        self._visit_tool(expr, DataType.SEGMENT)

    def visit_arc(self, expr: ArcExpr) -> None:
        self._visit_tool(expr, DataType.ARC)

    def visit_area(self, expr: AreaExpr) -> None:
        self._visit_tool(expr, DataType.AREA)

    def visit_line(self, expr: LineExpr) -> None:
        self._visit_tool(expr, DataType.LINE)

    def visit_counter(self, expr: CounterExpr) -> None:
        self._visit_tool(expr, DataType.COUNTER)

    def visit_colour(self, expr: ColourExpr) -> None:
        self._visit_atomic(expr)

    def visit_coords(self, expr: CoordsExpr) -> None:
        self._visit_atomic(expr)

    def visit_float(self, expr: FloatExpr) -> None:
        self._visit_atomic(expr)

    def visit_int(self, expr: IntExpr) -> None:
        self._visit_atomic(expr)

    def visit_string(self, expr: StringExpr) -> None:
        self._visit_atomic(expr)

    @staticmethod
    def _visit_atomic(expr: AtomicExpr) -> None:
        expr.attrs.datatype = expr.type

    def visit_processing_block(self, expr: ProcessingBlockExpr) -> None:
        for proc_expr in expr.items:
            proc_expr.accept(self)
            proc_id = proc_expr.attrs.name
            if proc_id in expr.attrs.names:
                raise SemanticError(expr, err.duplicated_processing_id())
            expr.attrs.names.add(proc_id)

    def visit_processing_id(self, expr: ProcessingIdExpr) -> None:
        expr.attrs.name = expr.value

    def visit_condition(self, expr: ConditionExpr) -> None:
        expr.event.accept(self)
        for act in expr.actions:
            act.accept(self)

    def visit_declaration(self, expr: DeclarationExpr) -> None:
        expr.name.accept(self)
        expr.attrs.name = expr.name.value
        expr.body.accept(self)

    def _visit_declarable_args(self, args: dict[str, ParamsExpr]) -> None:
        param_name: str
        arg: ParamsExpr
        for (param_name, arg) in args.items():
            arg.accept(self)
            if arg.attrs.datatype not in params.types[param_name]:
                raise SemanticError(arg, err.arg_type_mismatch())

    def visit_action(self, expr: ActionExpr) -> None:
        action_name = expr.name.value
        required = action.required_params[action_name]
        if len(expr.args) < len(required):
            raise SemanticError(expr, err.missing_required_action_arg())
        self._visit_declarable_args(expr.args)

    def visit_action_name(self, expr: ActionNameExpr) -> None:
        # todo implement
        pass

    def visit_event(self, expr: EventExpr) -> None:
        expr.attrs.datatype = DataType.EVENT
        expr.target.accept(self)
        event_name = expr.name.value

        if len(expr.args) < len(event.required_params[event_name]):
            raise SemanticError(expr, err.missing_required_event_arg())
        self._visit_declarable_args(expr.args)
        all_param_names = event.param_lists[event_name]
        if len(expr.args) < len(all_param_names):
            self._set_placeholder_params(all_param_names, expr)

    @staticmethod
    def _set_placeholder_params(all_param_names, expr):
        for param_name in all_param_names:
            if param_name not in expr.args:
                expr.args[param_name] = None

    def visit_event_name(self, expr: EventNameExpr) -> None:
        # todo implement
        pass

    def visit_binary(self, expr: BinaryExpr) -> None:
        if expr.left is None or expr.right is None:
            raise SemanticError(expr, err.missing_binary_operand())

        expr.left.accept(self)
        expr.right.accept(self)
        left_type = expr.left.attrs.datatype
        right_type = expr.right.attrs.datatype
        if left_type != right_type:
            raise SemanticError(expr, err.binary_types_mismatch())
        expr.attrs.datatype = left_type

    def visit_side(self, expr: SideExpr) -> None:
        expr.attrs.datatype = expr.type
