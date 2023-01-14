from abc import ABC, abstractmethod


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_program(self, expr) -> None: pass

    @abstractmethod
    def visit_object_block(self, expr) -> None: pass

    @abstractmethod
    def visit_object_id(self, expr) -> None: pass

    @abstractmethod
    def visit_object(self, expr) -> None: pass

    @abstractmethod
    def visit_tool_block(self, expr) -> None: pass

    @abstractmethod
    def visit_tool_id(self, expr) -> None: pass

    @abstractmethod
    def visit_tool_parts(self, expr) -> None: pass

    @abstractmethod
    def visit_point(self, expr) -> None: pass

    @abstractmethod
    def visit_segment(self, expr) -> None: pass

    @abstractmethod
    def visit_curve(self, expr) -> None: pass

    @abstractmethod
    def visit_area(self, expr) -> None: pass

    @abstractmethod
    def visit_line(self, expr) -> None: pass

    @abstractmethod
    def visit_counter(self, expr) -> None: pass

    @abstractmethod
    def visit_atomic(self, expr) -> None: pass

    @abstractmethod
    def visit_processing_block(self, expr) -> None: pass

    @abstractmethod
    def visit_processing_id(self, expr) -> None: pass

    @abstractmethod
    def visit_condition(self, expr) -> None: pass

    @abstractmethod
    def visit_declaration(self, expr) -> None: pass

    @abstractmethod
    def visit_action(self, expr) -> None: pass

    @abstractmethod
    def visit_action_id(self, expr) -> None: pass

    @abstractmethod
    def visit_event(self, expr) -> None: pass

    @abstractmethod
    def visit_event_id(self, expr) -> None: pass

    @abstractmethod
    def visit_binary(self, expr) -> None: pass
