# Centrifugal Pump Analysis for Python

## Dependencies

```
numpy
matplotlib
pint
ross-rotordynamics
```

## Example: Overhung Pump

### Code

```python
import pump_analysis as pa
import numpy as np

rotor = pa.examples.overhung.rotor
rotor.plotRotor()

ross_rotor = rotor.rossRotor(element_dx = 2 * pa.ureg("mm"))
fig = ross_rotor.plot_rotor()
fig.show()

rotor_speed = pa.examples.overhung.design_point.omega
# do rotordynamics with ROSS (ross_rotor is a ross-rotordynamics.Rotor object)
```
### Rotor Plot

![rotor](https://github.com/jpecquet/pump_analysis/assets/122790026/feb6b34a-7d22-4b87-b702-0aca22ba1e28)

### Rotor Plot with ROSS

![newplot(2)](https://github.com/jpecquet/pump_analysis/assets/122790026/44917127-0654-4478-8a06-cb9df37670c7)

## Example: Pump with Outboard Bearing

### Code

```python
import pump_analysis as pa
import numpy as np

rotor = pa.examples.outboard_bearing.rotor
rotor.plotRotor()

ross_rotor = rotor.rossRotor(element_dx = 2 * pa.ureg("mm"))
fig = ross_rotor.plot_rotor()
fig.show()

rotor_speed = pa.examples.overhung.design_point.omega
# do rotordynamics with ROSS (ross_rotor is a ross-rotordynamics.Rotor object)
```

### Rotor Plot

![rotor](https://github.com/jpecquet/pump_analysis/assets/122790026/a8052406-0b60-41b8-b087-1826da2cfb69)

### Rotor Plot with ROSS

![newplot(1)](https://github.com/jpecquet/pump_analysis/assets/122790026/f202ab28-9619-4ed2-b8a1-4789fa3650f0)
