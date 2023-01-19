def duplicated_object_id():
    return "duplicated object id"


def duplicated_processing_id():
    return "duplicated processing id"


def duplicated_tool_id():
    return "duplicated tool id"


def duplicated_tool_part():
    return "Duplicated tool part"


def missing_required_tool_param():
    return "missing required tool param"


def missing_required_action_param():
    return "missing required action param"


def missing_required_event_param():
    return "missing required event param"


def parameter_type_mismatch():
    return "parameter type mismatch"


def self_id_as_param_value():
    return "tool id used as the tool's own param value"


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
    return "only Segment and Curve expressions can be used as tool parts"
