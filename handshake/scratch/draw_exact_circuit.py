import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

# Create drawing with high DPI
d = schemdraw.Drawing(inches_per_unit=0.6)
d.config(fontsize=16, font="sans-serif", unit=1.5, color="black", lw=2)

# Input rails start at x=0
# A at y=10
# B at y=5
# C at y=0

# Rails
# Label A
d.add(logic.Line().at((0, 10)).to((28, 10)))
d.add(elm.Annotate().at((-0.5, 10)).label("A", fontsize=18))

# Label B
d.add(logic.Line().at((0, 5)).to((7, 5)))
d.add(elm.Annotate().at((-0.5, 5)).label("B", fontsize=18))

# Label C
d.add(logic.Line().at((0, 0)).to((27, 0)))
d.add(elm.Annotate().at((-0.5, 0)).label("C", fontsize=18))

# Gate 1: 2-input XOR(A, B) at x=5, y=8.5
g1 = d.add(logic.Xor().at((5, 8.5)).right())
# Connect A to G1 in1
d.add(logic.Dot().at((1.5, 10)))
d.add(logic.Line().at((1.5, 10)).to((1.5, g1.in1[1])))
d.add(logic.Line().at((1.5, g1.in1[1])).to(g1.in1))

# Connect B to G1 in2
d.add(logic.Dot().at((2.5, 5)))
d.add(logic.Line().at((2.5, 5)).to((2.5, g1.in2[1])))
d.add(logic.Line().at((2.5, g1.in2[1])).to(g1.in2))

# Gate 2: 2-input OR(A, B) at x=5, y=5.5
g2 = d.add(logic.Or().at((5, 5.5)).right())
# Connect A to G2 in1
d.add(logic.Dot().at((1.5, 10)))  # junction from A
# Branch down to G2 in1
d.add(logic.Line().at((1.5, g1.in1[1])).to((1.5, g2.in1[1])))
d.add(logic.Line().at((1.5, g2.in1[1])).to(g2.in1))

# Connect B to G2 in2
d.add(logic.Dot().at((3.5, 5)))
d.add(logic.Line().at((3.5, 5)).to((3.5, g2.in2[1])))
d.add(logic.Line().at((3.5, g2.in2[1])).to(g2.in2))

# Gate 3: NOT(B) at x=5, y=2.5
g3 = d.add(logic.Not().at((5, 2.5)).right())
# Connect B to G3 in1
d.add(logic.Dot().at((2.5, 5)))  # from B
d.add(logic.Line().at((2.5, 5)).to((2.5, g3.in1[1])))
d.add(logic.Line().at((2.5, g3.in1[1])).to(g3.in1))

# Gate 4: 2-input AND(G1, C) at x=10, y=8.5
g4 = d.add(logic.And().at((10, 8.5)).right())
# Connect G1 out to G4 in1
d.add(logic.Line().at(g1.out).to(g4.in1))
# Connect C to G4 in2
d.add(logic.Dot().at((8.5, 0)))
d.add(logic.Line().at((8.5, 0)).to((8.5, g4.in2[1])))
d.add(logic.Line().at((8.5, g4.in2[1])).to(g4.in2))

# Gate 5: 2-input XOR(B, G2) at x=10, y=5.0
g5 = d.add(logic.Xor().at((10, 5.0)).right())
# Connect B to G5 in1
d.add(logic.Dot().at((4.5, 5)))
d.add(logic.Line().at((4.5, 5)).to((7.5, 5)).to((7.5, g5.in1[1])).to(g5.in1))
# Connect G2 out to G5 in2
d.add(logic.Line().at(g2.out).to((8.0, g2.out[1])).to((8.0, g5.in2[1])).to(g5.in2))

# Gate 6: 2-input AND(G4, G5) at x=15, y=6.75
g6 = d.add(logic.And().at((15, 6.75)).right())
# Connect G4 out to G6 in1
d.add(logic.Line().at(g4.out).to((13.0, g4.out[1])).to((13.0, g6.in1[1])).to(g6.in1))
# Connect G5 out to G6 in2
d.add(logic.Line().at(g5.out).to((13.0, g5.out[1])).to((13.0, g6.in2[1])).to(g6.in2))

# Gate 7: 2-input NAND(G3, C) at x=12, y=2.0
g7 = d.add(logic.Nand().at((12, 2.0)).right())
# Connect G3 out to G7 in1
d.add(logic.Line().at(g3.out).to((10.0, g3.out[1])).to((10.0, g7.in1[1])).to(g7.in1))
# Connect C to G7 in2
d.add(logic.Dot().at((8.5, 0)))  # junction from C
# We can branch off the vertical line from C (at (8.5, g7.in2[1]))
d.add(logic.Dot().at((8.5, g7.in2[1])))
d.add(logic.Line().at((8.5, g7.in2[1])).to(g7.in2))

# Gate 8: 2-input XOR(G6, G7) at x=19, y=4.5
g8 = d.add(logic.Xor().at((19, 4.5)).right())
# Connect G6 out to G8 in1
d.add(logic.Line().at(g6.out).to((17.0, g6.out[1])).to((17.0, g8.in1[1])).to(g8.in1))
# Connect G7 out to G8 in2
d.add(logic.Line().at(g7.out).to((17.0, g7.out[1])).to((17.0, g8.in2[1])).to(g8.in2))

# Gate 9: 2-input NOR(A, G8) at x=23, y=6.0
g9 = d.add(logic.Nor().at((23, 6.0)).right())
# Connect A to G9 in1
d.add(logic.Dot().at((21.0, 10)))
d.add(logic.Line().at((21.0, 10)).to((21.0, g9.in1[1])).to(g9.in1))
# Connect G8 out to G9 in2
d.add(logic.Line().at(g8.out).to((21.0, g8.out[1])).to((21.0, g9.in2[1])).to(g9.in2))

# Gate 10: 2-input XOR(G9, C) at x=27, y=4.0
g10 = d.add(logic.Xor().at((27, 4.0)).right())
# Connect G9 out to G10 in1
d.add(logic.Line().at(g9.out).to((25.5, g9.out[1])).to((25.5, g10.in1[1])).to(g10.in1))
# Connect C to G10 in2
d.add(logic.Dot().at((25.5, 0)))
d.add(logic.Line().at((25.5, 0)).to((25.5, g10.in2[1])).to(g10.in2))

# Output Q
d.add(logic.Line().at(g10.out).to((30, g10.out[1])))
d.add(elm.Annotate().at((30.5, g10.out[1])).label("Q", fontsize=18))

# Save image
d.save("handshake/scratch/schemdraw_circuit.png", dpi=150)
print("Circuit generated and saved.")
