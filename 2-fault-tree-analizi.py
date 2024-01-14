import numpy as np

class Event:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

class Gate:
    def __init__(self, logic, *inputs):
        self.logic = logic
        self.inputs = inputs

def calculate_probability(event_or_gate):
    if isinstance(event_or_gate, Event):
        return event_or_gate.probability
    elif isinstance(event_or_gate, Gate):
        if event_or_gate.logic == 'AND':
            return min(calculate_probability(input_) for input_ in event_or_gate.inputs)
        elif event_or_gate.logic == 'OR':
            probabilities = [1 - calculate_probability(input_) for input_ in event_or_gate.inputs]
            return 1 - np.prod(probabilities)
        elif event_or_gate.logic == 'NOT':
            return 1 - calculate_probability(event_or_gate.inputs[0])
    else:
        raise ValueError("Invalid input")

# Örnek Fault Tree:
# A AND (B OR C)
A = Event('A', 0.8)
B = Event('B', 0.9)
C = Event('C', 0.7)

gate_B_OR_C = Gate('OR', B, C)
gate_A_AND_B_OR_C = Gate('AND', A, gate_B_OR_C)

# Hesaplamalar
probability_A = calculate_probability(A)
probability_B_OR_C = calculate_probability(gate_B_OR_C)
probability_A_AND_B_OR_C = calculate_probability(gate_A_AND_B_OR_C)

# Sonuçları yazdırma
print(f"Olay A'nın Olasılığı: {probability_A}")
print(f"Olay B veya C'nin Olasılığı: {probability_B_OR_C}")
print(f"Olay A ve (B veya C)'nin Olasılığı: {probability_A_AND_B_OR_C}")
