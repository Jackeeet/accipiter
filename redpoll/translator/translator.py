from bidict import bidict

from redpoll.analyzer.semantic import Analyzer, SemanticError
from redpoll.analyzer.syntactic import ParseError
from redpoll.expressions import *
from redpoll.resources import keywords as kw
from redpoll.translator.filewriter import FileWriter
from redpoll.translator.objectmap import names
from redpoll.translator.translationerror import TranslationError
from redpoll.types import OpType


class Translator(ExpressionVisitor):
    _file: FileWriter
    _param_names: dict[str, str] = {
        kw.COMPONENTS: "components",
        kw.FROM: "start",
        kw.TO: "end",
        kw.ANGLE_FROM: "start_angle",
        kw.ANGLE_TO: "end_angle",
        kw.COLOUR: "colour",
        kw.THICKNESS: "thickness",
        kw.CENTER: "center",
        kw.RADIUS: "radius",
        kw.START: "start",
        kw.STEP: "step",
        kw.POINT: "at",
    }

    _action_names: dict[str, str] = {
        kw.INCREMENT: "increment",
        kw.DECREMENT: "decrement",
        kw.RESET: "reset",
        kw.ALERT: "alert",
        kw.SAVE: "save",
        kw.FLASH: "flash",
    }

    _event_names: dict[str, str] = {
        kw.CROSSING: "crosses",
        kw.EQUALS: "equals"
    }

    def __init__(self, source: str, output: str) -> None:
        self._source_path = source
        self._output_path = output

        self._object_kinds = bidict()
        self._tools = bidict()
        self._declarations = bidict()

    def _next_obj_index(self) -> int:
        return len(self._object_kinds)

    def _next_tool_index(self) -> int:
        return len(self._tools)

    def _next_decl_index(self) -> int:
        return len(self._declarations)

    def translate(self) -> None:
        try:
            with open(self._source_path, 'r', encoding='utf8') as sourcefile:
                analyzer = Analyzer(sourcefile.read())
            root = analyzer.analyze()
        except (ParseError, SemanticError) as err:
            raise TranslationError(err)

        with FileWriter(self._output_path) as self._file:
            self.visit_program(root)

    def visit_program(self, expr: ProgramExpr) -> None:
        self._file.writeln("__all__ = ['object_kinds', 'tools', 'conditions']")
        self._write_imports()
        self._file.writeln("print(\"'declared' loaded\")")

        expr.objects.accept(self)
        expr.tools.accept(self)
        expr.processing.accept(self)

    def _write_imports(self) -> None:
        self._file.writeln()
        self._file.writeln("from videoanalytics.analytics.declarable.actions import *")
        self._file.writeln("from videoanalytics.analytics.declarable.condition import *")
        self._file.writeln("from videoanalytics.analytics.declarable.events import *")
        self._file.writeln("from videoanalytics.analytics.declarable.tools import *")
        self._file.writeln("from videoanalytics.models.operators import *")
        self._file.writeln("from videoanalytics.models import Coords, Side, SideValue")
        self._file.writeln()

    def visit_object_block(self, expr: ObjectBlockExpr) -> None:
        self._file.write("object_kinds = [")
        for obj in expr.items:
            obj.accept(self)
        self._file.writeln("]")

    def visit_object(self, expr: ObjectExpr) -> None:
        self._file.write("'")
        expr.id.accept(self)
        self._file.write("', ")

    def visit_object_id(self, expr: ObjectIdExpr) -> None:
        if expr.value in self._object_kinds.inverse:
            index = self._object_kinds.inverse[expr.value]
            self._file.write(f"object_kinds[{index}]")
        else:
            index = self._next_obj_index()
            self._object_kinds[index] = expr.value
            self._file.write(names[expr.value])

    def visit_tool_block(self, expr: ToolBlockExpr) -> None:
        self._file.writeln("tools: dict[int, Tool | tuple[int, int]] = dict()")
        self._file.writeln()
        for tool in expr.items:
            tool.accept(self)
            self._file.writeln()
        self._file.writeln()
        self._file.writeln("tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}")

    def visit_tool_id(self, expr: ToolIdExpr) -> None:
        if expr.value in self._tools.inverse:
            index = self._tools.inverse[expr.value]
        else:
            index = self._next_tool_index()
            self._tools[index] = expr.value
        self._file.write(f"tools[{index}]")

    def visit_tool_parts(self, expr: ToolPartsExpr) -> None:
        self._file.writeln("[")
        for tool_part in expr.parts:
            self._file.write("    ")
            tool_part.accept(self)
            self._file.writeln(",")
        self._file.write("]")

    def _visit_optional_id(self, expr: ToolExpr) -> None:
        if expr.id is not None:
            expr.id.accept(self)
            self._file.write(" = ")

    def visit_point(self, expr: PointExpr) -> None:
        self._visit_optional_id(expr)
        expr.params[kw.POINT].accept(self)

    def _visit_parametrised_tools(self, expr: ToolExpr, tool_name: str) -> None:
        self._visit_optional_id(expr)
        self._visit_tool_params(expr, tool_name)

    def _visit_tool_params(self, expr: ToolExpr, tool_name: str) -> None:
        self._file.write(tool_name)
        self._file.write("(")
        for name, value in expr.params.items():
            self._file.write(self._param_names[name])
            self._file.write("=")
            value.accept(self)
            self._file.write(",")
        self._file.write(")")

    def visit_segment(self, expr: SegmentExpr) -> None:
        self._visit_parametrised_tools(expr, "Segment")

    def visit_arc(self, expr: ArcExpr) -> None:
        self._visit_parametrised_tools(expr, "Arc")

    def visit_area(self, expr: AreaExpr) -> None:
        self._visit_parametrised_tools(expr, "Area")

    def visit_line(self, expr: LineExpr) -> None:
        self._visit_parametrised_tools(expr, "Line")

    def visit_counter(self, expr: CounterExpr) -> None:
        self._visit_parametrised_tools(expr, "Counter")

    def visit_colour(self, expr: ColourExpr) -> None:
        self._visit_atomic(expr)

    def visit_coords(self, expr: CoordsExpr) -> None:
        self._file.write("Coords")
        self._visit_atomic(expr)

    def visit_float(self, expr: FloatExpr) -> None:
        self._visit_atomic(expr)

    def visit_int(self, expr: IntExpr) -> None:
        self._visit_atomic(expr)

    def visit_string(self, expr: StringExpr) -> None:
        self._visit_atomic(expr)

    def _visit_atomic(self, expr: AtomicExpr) -> None:
        self._file.write(str(expr.value))

    def visit_processing_block(self, expr: ProcessingBlockExpr) -> None:
        self._file.writeln()
        self._file.writeln("declarations: dict[int, Action | Event] = dict()")
        self._file.writeln("conditions: list[Condition] = []")
        self._file.writeln()

        for item in expr.items:
            item.accept(self)

    def visit_processing_id(self, expr: ProcessingIdExpr) -> None:
        if expr.value in self._declarations.inverse:
            index = self._declarations.inverse[expr.value]
        else:
            index = self._next_decl_index()
            self._declarations[index] = expr.value
        self._file.write(f"declarations[{index}]")

    def visit_condition(self, expr: ConditionExpr) -> None:
        self._file.writeln("conditions.append(Condition(")
        self._file.write("    ")
        expr.event.accept(self)
        self._file.writeln(",")
        self._file.write("    [")
        for action in expr.actions:
            action.accept(self)
            self._file.write(",")
        self._file.writeln("]")
        self._file.writeln("))")

    def visit_declaration(self, expr: DeclarationExpr) -> None:
        expr.name.accept(self)
        self._file.write(" = ")
        expr.body.accept(self)
        self._file.writeln()

    def visit_action(self, expr: ActionExpr) -> None:
        self._file.write("Action(")
        expr.name.accept(self)
        self._file.write(",{")
        assert (len(expr.attrs.param_names) == len(expr.args))
        for name, value in zip(expr.attrs.param_names, expr.args):
            self._file.write(f"'{name}'")
            self._file.write(": ")
            value.accept(self)
            self._file.write(",")
        self._file.write("})")

    def visit_action_name(self, expr: ActionNameExpr) -> None:
        self._file.write(self._action_names[expr.value])

    def visit_event(self, expr: EventExpr) -> None:
        self._file.write("Event(")
        expr.name.accept(self)
        self._file.write(",")
        expr.target.accept(self)
        self._file.write(",{")

        assert (len(expr.attrs.param_names) == len(expr.args))
        for name, value in zip(expr.attrs.param_names, expr.args):
            self._file.write(f"'{name}'")
            self._file.write(": ")
            value.accept(self)
            self._file.write(",")
        self._file.write("})")

    def visit_event_name(self, expr: EventNameExpr) -> None:
        self._file.write(self._event_names[expr.value])

    def visit_binary(self, expr: BinaryExpr) -> None:
        self._file.writeln("EvalTree(")
        self._file.write("        left=")
        expr.left.accept(self)
        self._file.writeln(",")
        self._file.write("        op_or_val=op_")
        match expr.op:
            case OpType.AND:
                self._file.writeln("and,")
            case OpType.OR:
                self._file.writeln("or,")
            case _:
                raise TranslationError(f"Unsupported binary operator ({expr.op})")
        self._file.write("        right=")
        expr.right.accept(self)
        self._file.writeln()
        self._file.write("    )")

    def visit_side(self, expr: SideExpr) -> None:
        self._file.write(f"Side(SideValue('{expr.value}'))")
