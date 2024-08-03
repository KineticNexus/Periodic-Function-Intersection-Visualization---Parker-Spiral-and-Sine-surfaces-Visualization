# Periodic-Function-Intersection-Visualization---Parker-Spiral-and-Sine-surfaces-Visualization
Periodic Function Intersection Visualization This application provides an interactive visualization of Parker spirals surfaces and Sine surfaces and the intersection between two periodic functions in 3D space. It's designed to explore patterns that emerge from these intersections, with a particular focus on potential connections to prime numbers.

Features

Interactive 3D Visualization: Shows two intersecting periodic surfaces in 3D space.
X=0 Plane Projection: Displays the projection of intersection points on the YZ plane.
Z=0 Plane Projection: Shows the projection of intersection points on the XY plane, which is particularly relevant for exploring number-theoretic patterns.
Adjustable Parameters: Users can modify various parameters in real-time using sliders or direct input, including:

Frequency and amplitude of both periodic functions
Spatial range and resolution
Number of periods
Intersection threshold
Viewing angles for 3D plot

Technical Details

Language: Python 3
Libraries:

NumPy for numerical computations
Matplotlib for plotting
PyQt5 for the graphical user interface

Code Structure

PeriodicIntersectionApp class: Main application class

initUI(): Sets up the user interface
update_value(): Updates parameter values from slider input
update_from_textbox(): Updates parameter values from text input
update_plot(): Core function that recalculates and redraws all plots

Key Functions

spiral_surface(): Generates a spiral-like periodic surface
sinusoidal_surface(): Generates a sinusoidal surface
Intersection calculation: Performed in the update_plot() method

Usage

Adjust parameters using sliders or by entering values in the text boxes.
Click "Update Plot" or press Enter in a text box to refresh the visualization.
Observe the 3D plot and the two projection plots to explore the intersections.
Pay special attention to the Z=0 projection for potential number-theoretic patterns.

Installation

Ensure Python 3 is installed on your system.
Install required libraries:
Copypip install numpy matplotlib PyQt5

Run the script:
Copypython periodic_intersection_app.py
