import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

# We will create a Drawing with schemdraw
with schemdraw.Drawing(file="handshake/scratch/schemdraw_circuit.png", inches_per_unit=0.5) as d:
    d.config(fontsize=14, font="sans-serif", unit=2)
    # Let's see how schemdraw draws logic gates
    pass

print("Schemdraw drawing test completed.")
