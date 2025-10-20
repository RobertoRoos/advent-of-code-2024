from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, List, Tuple

from advent_of_code.shared import Solver, main


class Wire:
    """Abstraction of wire."""

    def __init__(self, name: str, value: None | bool = None):
        self.name = name
        self.value = value
        self.input_for_gates: List["Gate"] = []
        # ^ this wire is an input for the following gates

        self.output_of_gate: "None | Gate" = None
        # ^ this wire is the output of the following gate

    def number(self) -> int:
        return int(self.name[1:])

    def __repr__(self) -> str:
        return f"Wire({self.name})"


class Logic(StrEnum):
    """Different logic gate types."""

    AND = "AND"
    OR = "OR"
    XOR = "XOR"


class Gate:
    """Logical gate abstraction.

    WHen a gate is instantiated it is also registered with the wire.
    """

    def __init__(self, inputs: List[Wire], logic: Logic, output: Wire):
        self.inputs: Tuple[Wire, Wire] = (inputs[0], inputs[1])
        self.logic = logic
        self.output: Wire = output

        for wire in self.inputs:
            wire.input_for_gates.append(self)
        self.output.output_of_gate = self

    def __repr__(self) -> str:
        return f"Gate({self.logic})"

    def process(self):
        """Run this gate, assuming inputs are defined.

        Yield child gates that can now be run.
        """
        outcome = None
        if self.logic == Logic.AND:
            outcome = self.inputs[0].value and self.inputs[1].value
        elif self.logic == Logic.OR:
            outcome = self.inputs[0].value or self.inputs[1].value
        elif self.logic == Logic.XOR:
            outcome = self.inputs[0].value != self.inputs[1].value

        self.output.value = outcome

    def has_inputs(self):
        """``True`` if both inputs have a not-None value."""
        return self.inputs[0].value is not None and self.inputs[1].value is not None

    @classmethod
    def process_all(cls, gates: List["Gate"]):
        """Process all provided logical gates.

        The tree structure will be followed through their linked objects.
        """

        # Track gates that don't have an output yet:
        gates_needing_processing: List[Gate] = [g for g in gates if g.has_inputs()]

        # Keep going over all gates that are ready for processing:
        while gates_needing_processing:
            gate = gates_needing_processing.pop()
            gate.process()
            for child in gate.output.input_for_gates:
                if child.has_inputs():
                    gates_needing_processing.append(child)
        # If the gates are set up correctly, we will have handled all of them
        # precisely.


@dataclass
class Adder:
    x: Wire | None = None
    y: Wire | None = None
    z: Wire | None = None


class Day24(Solver):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.wires: Dict[str, Wire] = {}
        self.gates: List[Gate] = []
        self.adders: List[Adder] = []

    def __call__(self) -> str:

        # Process input file:
        first_section = True
        for line in self.iterate_input():
            if not line:
                first_section = False
                continue

            if first_section:
                name, _, value = line.partition(": ")
                new_wire = Wire(name, value == "1")  # Self-registering
                self.wires[name] = new_wire
            else:
                parts = line.split(" ")
                input_names = [parts[0], parts[2]]
                logic_type = Logic(parts[1])
                output_name = parts[4]

                for name in input_names + [output_name]:
                    if name not in self.wires:
                        self.wires[name] = Wire(name, None)

                new_gate = Gate(
                    [self.wires[n] for n in input_names],
                    logic_type,
                    self.wires[output_name],
                )
                self.gates.append(new_gate)

        # Organize all the wires a little:
        self.adders = [Adder() for w in self.wires.keys() if w.startswith("z")]

        for wire in self.wires.values():
            letter = wire.name[0]
            if letter in ["x", "y", "z"]:
                n = wire.number()
                setattr(self.adders[n], letter, wire)

        if self.args.part == 1:

            Gate.process_all(self.gates)

            # Combine into output:
            result = 0
            for wire in self.wires.values():
                if wire.name[0] == "z":
                    if wire.value:
                        result += 2 ** wire.number()

            return str(result)

        else:
            swapped_wires = [g.output for g in self.gates if not self.check_validity(g)]

            names_sorted = sorted(w.name for w in swapped_wires)

            return ",".join(names_sorted)

    def check_validity(self, gate) -> bool:
        """Check if a specific logic gate makes sense for our binary addition.

        It's a little bit cheap, but by simply comparing the gates following a certain
        gates we can in this exercise determine which wires must have been crossed.

        Note that binary addition looks like this:

        ```
        n > 1:
            u[n] = x[n] XOR y[n]
            v[n] = x[n] AND y[n]
            w[n] = c[n-1] AND u[n]
            z[n] = c[n-1] XOR u[n]
            c[n] = w[n] AND v[n]

        n == 0:
            z[0] = x[0] XOR y[0]
            c[0] = x[0] AND y[0]
        ```

        Here ``c`` represents the carry-over.
        """
        if (
            gate.output.name[0] == "z"
            and gate.output != self.adders[-1].z
            and gate.logic != Logic.XOR
        ):
            # The gate before an output must be XOR, with the exception for the last bit
            return False

        if (
            gate.logic == Logic.XOR
            and gate.output.name[0] not in ("x", "y", "z")
            and gate.inputs[0].name[0] not in ("x", "y", "z")
            and gate.inputs[1].name[0] not in ("x", "y", "z")
        ):
            # All "XOR"s must either have x/y as an input or z as an output
            return False

        if gate.logic == Logic.AND and self.adders[0].x not in gate.inputs:
            for child_gates in gate.output.input_for_gates:
                if child_gates.logic != Logic.OR:
                    # There are two "AND" gates and both direct into an "OR"
                    # (Except for the gate for x[0] and y[0])
                    return False

        if gate.logic == Logic.XOR:
            for child_gates in gate.output.input_for_gates:
                if child_gates.logic == Logic.OR:
                    # No "XOR"s direct into an "OR" at all
                    return False

        return True


if __name__ == "__main__":
    main(Day24)
