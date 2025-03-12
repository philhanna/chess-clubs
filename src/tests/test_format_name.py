import pytest

from chess_clubs import format_name

@pytest.mark.parametrize("input_name, expected_output", [
    ("john mcconnell", "McConnell, John"),
    ("sean O'brien", "O'Brien, Sean"),
    ("michael jordan Jr.", "Jordan Jr, Michael"),
    ("robert james Smith III", "Smith III, Robert James"),
    ("MCdonald, alex", "McDonald, Alex"),
    ("O'neal, shaquille", "O'Neal, Shaquille"),
    ("patrick O'donnell", "O'Donnell, Patrick"),
    ("mcgregor, conor", "McGregor, Conor"),
    ("john doe", "Doe, John"),
    ("alice mcintyre", "McIntyre, Alice"),
    ("james smith sr", "Smith Sr, James"),
    ("dr. richard feynman", "Feynman, Dr Richard"),  # "Dr" isn't a suffix, so it's treated as part of the first name
    ("robert de niro", "De Niro, Robert"),  # Testing multi-word last names
    ("leonardo da vinci", "Da Vinci, Leonardo"),  # Testing historical names
    ("chris o'malley", "O'Malley, Chris"),  # Testing proper capitalization of O'
    ("McCartney, Paul", "McCartney, Paul"),  # Testing Mc capitalization when input has a comma
    ("McGonagall, Minerva", "McGonagall, Minerva"),  # Another Mc test case
    ("o'rourke, patrick", "O'Rourke, Patrick"),  # O' capitalization with input having a comma
    ("singleword", "singleword"),  # Should return unchanged for single-word inputs
    ("O'Conner", "O'Conner"),  # Single-word O' names should remain unchanged
])
def test_format_name(input_name, expected_output):
    actual = format_name(input_name)
    expected = expected_output
    assert actual == expected
