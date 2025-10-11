from enum import StrEnum
from typing import Dict, List, Tuple

from advent_of_code.shared import Solver, main


class Wire:
    """Abstraction of wire."""

    def __init__(self, name: str, value: None | bool = None):
        self.name = name
        self.value = value
        self.input_for_gates: List["Gate"] = []
        self.output_of_gates: List["Gate"] = []


class Gate:
    """Logical gate abstraction.

    WHen a gate is instantiated it is also registered with the wire.
    """

    class Logic(StrEnum):
        AND = "AND"
        OR = "OR"
        XOR = "XOR"

    def __init__(self, inputs: List[Wire], logic: Logic, output: Wire):
        self.inputs: Tuple[Wire, Wire] = (inputs[0], inputs[1])
        self.logic = logic
        self.output: Wire = output

        for wire in self.inputs:
            wire.input_for_gates.append(self)
        self.output.output_of_gates.append(self)

    def process(self):
        """Run this gate, assuming inputs are defined.

        Yield child gates that can now be run.
        """
        outcome = None
        if self.logic == self.Logic.AND:
            outcome = self.inputs[0].value and self.inputs[1].value
        elif self.logic == self.Logic.OR:
            outcome = self.inputs[0].value or self.inputs[1].value
        elif self.logic == self.Logic.XOR:
            outcome = self.inputs[0].value != self.inputs[1].value

        self.output.value = outcome

    def has_output(self):
        return self.output.value is not None

    def has_inputs(self):
        return self.inputs[0].value is not None and self.inputs[1].value is not None


class Day24(Solver):

    def __call__(self) -> str:

        wires: Dict[str, Wire] = {}
        gates_by_output: Dict[str, Gate] = {}

        # Track gates that don't have an output yet:
        gates_needing_processing: List[Gate] = []

        # Process input file:
        first_section = True
        for line in self.iterate_input():
            if not line:
                first_section = False
                continue

            if first_section:
                name, _, value = line.partition(": ")
                wires[name] = Wire(name, value == "1")  # Self-registered
            else:
                parts = line.split(" ")
                input_names = [parts[0], parts[2]]
                logic_type = Gate.Logic(parts[1])
                output_name = parts[4]

                for name in input_names + [output_name]:
                    if name not in wires:
                        wires[name] = Wire(name, None)

                new_gate = Gate(
                    [wires[n] for n in input_names], logic_type, wires[output_name]
                )
                gates_by_output[output_name] = new_gate

                if new_gate.has_inputs():
                    gates_needing_processing.append(new_gate)

        # Keep going over all gates that are ready for processing:
        while gates_needing_processing:
            gate = gates_needing_processing.pop()
            gate.process()
            for child in gate.output.input_for_gates:
                if child.has_inputs():
                    gates_needing_processing.append(child)
        # If the gates are set up correctly, we will have handled all of them
        # precisely.

        # Combine into output:
        result = 0
        for wire in wires.values():
            if wire.name[0] == "z":
                pos = int(wire.name[1:])
                if wire.value:
                    result += 2**pos

        return str(result)


if __name__ == "__main__":
    main(Day24)
