from bidict import bidict

from .filewriter import FileWriter
from .objectmap import names
from .translationerror import TranslationError
from ..types import OpType
from ..analyzer.syntactic import ParseError, Parser
from ..expressions import *
from ..resources import keywords as kw


class Translator(ExpressionVisitor):
    _file: FileWriter
    _param_names: dict[str, str] = {
        kw.CONTENTS: "contents",
        kw.FROM: "start",
        kw.TO: "end",
        kw.ANGLE_FROM: "start",
        kw.ANGLE_TO: "end",
        kw.COLOUR: "colour",
        kw.THICKNESS: "thickness",
        kw.CENTER: "center",
        kw.RADIUS: "radius",
        kw.START: "start",
        kw.STEP: "step",
        kw.POINT: "at",

        kw.ELEMENT: "element",
        kw.MESSAGE: "message",
        kw.NUMBER: "count",
        kw.COUNT: "counter",
    }

    _action_names: dict[str, str] = {
        kw.INCREMENT: "increment",
        kw.DECREMENT: "decrement",
        kw.RESET: "reset",
        kw.ALERT: "alert",
        kw.SAVE: "save",
        kw.SET_COLOUR: "set_colour",
    }

    _event_names: dict[str, str] = {
        kw.CROSSING: "intersects",
        kw.EQUALS: "equals"
    }

    def __init__(self, source: str, output: str) -> None:
        self._source_path = source
        self._output_path = output

        self._tools = bidict()
        self._declarations = bidict()

    def _next_tool_index(self) -> int:
        return len(self._tools)

    def _next_decl_index(self) -> int:
        return len(self._declarations)

    def translate(self) -> None:
        with open(self._source_path, 'r', encoding='utf8') as sourcefile:
            parser = Parser(sourcefile.read())
        root = parser.parse()
        try:
            with FileWriter(self._output_path) as self._file:
                self.visit_program(root)
        except ParseError as err:
            raise TranslationError(err)

    def visit_program(self, expr: ProgramExpr) -> None:
        self._file.writeln("__all__ = ['object_kinds', 'tools', 'conditions']")

        self._file.writeln("print(\"'declared' loaded\")")

        self._file.writeln()
        self._file.writeln("from .declarable.actions import *")
        self._file.writeln("from .declarable.condition import *")
        self._file.writeln("from .declarable.events import *")
        self._file.writeln("from .declarable.tools import *")
        self._file.writeln()

        expr.objects.accept(self)
        expr.tools.accept(self)
        expr.processing.accept(self)

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

    def visit_curve(self, expr: CurveExpr) -> None:
        self._visit_parametrised_tools(expr, "Curve")

    def visit_area(self, expr: AreaExpr) -> None:
        self._visit_parametrised_tools(expr, "Area")

    def visit_line(self, expr: LineExpr) -> None:
        self._visit_parametrised_tools(expr, "Line")

    def visit_counter(self, expr: CounterExpr) -> None:
        self._visit_parametrised_tools(expr, "Counter")

    def visit_atomic(self, expr: AtomicExpr) -> None:
        self._file.write(str(expr.value))

    def visit_processing_block(self, expr: ProcessingBlockExpr) -> None:
        self._file.writeln()
        self._file.writeln("declarations: dict[int, Action | Event] = dict()")
        self._file.writeln("conditions: list[Condition] = []")
        self._file.writeln()

        for item in expr.items:
            item.accept(self)

    def visit_processing_id(self, expr: ProcessingIdExpr) -> None:
        # todo extract method
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
        self._handle_decl_body("Action", expr)

    def visit_action_id(self, expr: ActionIdExpr) -> None:
        self._file.write(self._action_names[expr.value])

    def visit_event(self, expr: EventExpr) -> None:
        self._handle_decl_body("Event", expr)

    def _handle_decl_body(self, kind: str, expr: ActionExpr | EventExpr) -> None:
        self._file.write(f"{kind}(")
        expr.name.accept(self)
        self._file.write(",{")
        for name, value in expr.params.items():
            self._file.write(f"'{self._param_names[name]}'")
            self._file.write(": ")
            value.accept(self)
            self._file.write(",")
        self._file.write("})")

    def visit_event_id(self, expr: EventIdExpr) -> None:
        self._file.write(self._event_names[expr.value])

    def visit_binary(self, expr: BinaryExpr) -> None:
        self._file.writeln("BinaryEventChain(")
        self._file.write("        left=")
        expr.left.accept(self)
        self._file.writeln(",")
        self._file.write("        val=op_")
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
