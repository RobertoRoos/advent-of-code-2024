from enum import StrEnum
from typing import Dict, List, Tuple, Set, Any, FrozenSet

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
        self.output.output_of_gate = self

    def __repr__(self) -> str:
        return f"Gate({self.logic})"

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

    @classmethod
    def build_rules_by_output(cls, wires: List[Wire]):
        """For the given wires, chain the rules together as far as possible."""
        rule_chains = {}

        for wire in wires:
            rule_chains[wire] = cls._build_rules_by_output_recursively(wire)

        return rule_chains

    @classmethod
    def _build_rules_by_output_recursively(cls, wire) -> Tuple["Gate", FrozenSet[Any]]:
        """Created a nested structure following rules down to the real inputs."""
        gate = wire.output_of_gate
        if gate is None:
            return wire

        return (
            gate,
            frozenset(cls._build_rules_by_output_recursively(sub_wire) for sub_wire in gate.inputs)
        )

    # @classmethod
    # def _build_rules_by_input_recursively(cls, wire):
    #     children = []
    #     for gate in wire.input_for_gates:
    #         children.append(
    #             (gate.logic, gate)
    #         )
    #
    #     return children


class Day24(Solver):

    def __call__(self) -> str:

        wires: Dict[str, Wire] = {}
        gates: List[Gate] = []

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
                gates.append(new_gate)

        if self.args.part == 1:

            Gate.process_all(gates)

            # Combine into output:
            result = 0
            for wire in wires.values():
                if wire.name[0] == "z":
                    if wire.value:
                        result += 2 ** wire.number()

            return str(result)

        else:
            # We cannot possibly find the swapped wires through trial-and-error.
            # Instead, we will trace the set of rules all the way down. We already know
            # what the rules must look like for summing binary, namely:
            #   bit 0:          z[0] =   x[0] XOR y[0]
            #   bit n, n>0:     z[n] = ( x[n] XOR y[n] ) XOR ( x[n-1] AND y[n-1] )
            #
            # So when we have the set of rules, we should be able to pick the incorrect
            # ones directly.

            output_wires = [w for w in wires.values() if w.name.startswith("z")]

            full_rules = Gate.build_rules_by_output(output_wires)

            full_rules_names = {wire.name: rules for wire, rules in full_rules.items()}
            names_sorted = sorted(full_rules_names.keys())
            full_rules_sorted = [(name, full_rules_names[name]) for name in names_sorted]

            # outputs = sorted(wire.name for wire in full_rules.keys())
            # full_rules_sorted = {name: full_rules[name] for name in outputs}

            for wire, rules in full_rules.items():
                valid = self.verify_binary_sum(wire, rules)
                if not valid:
                    pass
                pass

            pass

            # Gate.process_all(gates)
            #
            # numbers = {"x": 0, "y": 0, "z": 0}
            # for wire in wires.values():
            #     if wire.name[0] in numbers:
            #         if wire.value:
            #             numbers[wire.name[0]] += 2 ** wire.number()

            return ""

    @classmethod
    def verify_binary_sum(cls, wire, rules) -> bool:
        if rules[0].logic != Gate.Logic.XOR:
            return False

        n = wire.number()
        if n == 0:
            return {w.name for w in rules[1]} == {"x00", "y00"}

        expected = frozenset([
            (Gate.Logic.XOR, frozenset({f"x{n:02}", f"y{n:02}"})),
            (Gate.Logic.AND, frozenset({f"x{(n-1):02}", f"y{(n-1):02}"})),
        ])

        return rules[1] == expected


if __name__ == "__main__":
    main(Day24)
