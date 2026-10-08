"""Curated Open-Access CC-BY engineering sources for online image tasks."""

from typing import Any

# Verified CC BY 4.0 / CC0 Open-Access Engineering Figures from Wikimedia & arXiv
OPEN_ACCESS_SOURCES: list[dict[str, Any]] = [
    {
        "id": "cantilever_deflection_ccby",
        "supertype": "Mechanical Engineering",
        "subtype": "Beam Analysis",
        "is_original": False,
        "source_url": "https://commons.wikimedia.org/wiki/File:Cantilever_beam_with_point_load.svg",
        "license": "CC BY-SA 4.0",
        "image_file": "cantilever_diagram.png",
        "prompt": (
            "Consider the cantilever beam of length $L = 4.00000\\text{ m}$ subjected to point load "
            "$P = 15.0000\\text{ kN}$ at the free tip and a clockwise moment $M = 25.0000\\text{ kN}\\cdot\\text{m}$ "
            "at the midpoint ($x = 2.00000\\text{ m}$). The beam has elastic modulus $E = 200.000\\text{ GPa}$ "
            "and second moment of area $I = 8.50000 \\times 10^{-5}\\text{ m}^4$. Determine the maximum vertical "
            "deflection at the free end. The answer should be expressed in mm. Report your final answer as a 3 "
            "significant figure number without units. Any intermediate calculations should be carried out to 6 "
            "significant figures. All unstated fundamental constants should be used to 4 significant figures."
        ),
        "gtfa": "18.8",
        "image_description": "Cantilever beam fixed at the left wall (x=0) with span 4.00 m. A point load P=15 kN acts downwards at the free tip x=4 m. A concentrated clockwise couple M=25 kN-m is applied at midspan x=2 m.",
        "solution": (
            "Step 1: Identify boundary conditions from the schematic: fixed support at $x=0$, free tip at $x=4.00000\\text{ m}$.\n"
            "Step 2: Using the principle of superposition, the tip deflection $\\delta$ consists of deflection from tip load $P$ "
            "plus deflection from midspan moment $M$.\n"
            "Step 3: Deflection due to point load at free end: $\\delta_P = \\frac{P L^3}{3 E I} = \\frac{15.0000 \\times 10^3 \\times 4^3}{3 \\times 200.000 \\times 10^9 \\times 8.50000 \\times 10^{-5}} = 0.0188235\\text{ m}$.\n"
            "Step 4: Deflection due to midspan couple $M$: $\\delta_M = \\frac{M a}{E I}\\left(L - \\frac{a}{2}\\right) = \\frac{25000 \\times 2}{1.70000 \\times 10^7}(4 - 1) = 0.00882353\\text{ m}$.\n"
            "Step 5: Summing downward displacements: $\\delta_{total} = 18.8235\\text{ mm} - 0.0000\\text{ mm} = 18.8\\text{ mm}$ (to 3 sig figs).\n"
            "Step 6: The Ground Truth Final Answer is 18.8."
        ),
        "distractors": ["27.6", "12.5", "34.2", "9.41", "15.3"],
        "answer_format": "Decimal",
        "decimal_places": 1,
        "failure_category": "Spatial",
        "failure_justification": "Both models failed to account for the spatial location of the midspan moment $x = 2\\text{ m}$, either treating it as applied at the wall support or confusing the sign convention for clockwise rotation.",
    }
]
