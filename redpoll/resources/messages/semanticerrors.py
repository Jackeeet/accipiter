def duplicated_object_id():
    return "duplicated object id"


def duplicated_processing_id():
    return "duplicated processing id"


def duplicated_tool_id():
    return "duplicated tool id"


def duplicated_tool_part():
    return "Duplicated tool part"


def missing_required_tool_arg():
    return "missing required tool argument"


def missing_required_action_arg():
    return "missing required action argument"


def missing_required_event_arg():
    return "missing required event argument"


def arg_type_mismatch():
    return "argument type mismatch"


def self_id_as_arg():
    return "tool id used as the tool's own argument value"


def unconnected_area():
    return "Unconnected area"


def unconnected_line():
    return "Unconnected line"


def undeclared_tool_part():
    return "Undeclared tool part"


def undeclared_tool_variable(var_name):
    return f"undeclared tool variable: {var_name}"


def unexpected_parameter_name(param_name):
    return f"Unexpected parameter name: {param_name}"


def unsupported_tool_part_type():
    return "only Segment and Arc expressions can be used as tool parts"


def missing_binary_operand():
    return "missing a binary operand"


def binary_types_mismatch():
    return "binary operand types mismatch"
