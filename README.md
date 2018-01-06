# L-System
L-System also known as Liedermayer System is a way to describe procedural geometries with a few set of rules.

This python implementation supports following features:

    * Simple rules e.g. A -> AB
    * Branching A[BC]
    * Arguments F(x,t) -> F(x*2, t-1)+F(2(x^2)-7, t-1)
    * Contextual matching A < B > A (matches ABA and not AAB)
    * Probabilistic rules A -> {0.25:'AB', 0.75:'AA'}

There is also dummy viewer to present solid lines and polygons generated by the lsystem

## Organization
The python scripts is found in the lsystem folder and its corresponding tests are in tests.

_example.py_ contains multiple set of rules and pattern, demonstrating usage of the entire library. _There are a lot of commented lines!!!_

_index.html_ is a web page meant to be a intuitive user interface where one could learn programming in a playful way. It uses __Brython__ in order to call the python script.