# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 21:36:08 2024

@author: halif

in the quest of prime numbers patterns...
kineticnexus@gmail.com

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QLineEdit, QPushButton, QScrollArea
from PyQt5.QtCore import Qt
import sys
import traceback

class ParkerSpiralApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interactive Parker Spiral Visualization')
        self.setGeometry(100, 100, 1800, 1000)

        main_layout = QHBoxLayout()

        # Create a single figure with three subplots
        self.fig = plt.figure(figsize=(18, 12))
        self.ax3d = self.fig.add_subplot(221, projection='3d')
        self.ax_x0 = self.fig.add_subplot(222)
        self.ax_z0 = self.fig.add_subplot(212)
        self.canvas = FigureCanvas(self.fig)

        main_layout.addWidget(self.canvas, stretch=3)

        # Controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        self.sliders = {}
        self.textboxes = {}

        self.params = {
            'V': (400e3, 1e3, 1e6),
            'omega': (2.7e-6, 1e-7, 1e-5),
            'AU': (1.496e11, 1e10, 1e12),
            'r_min': (0.1, 0.01, 1),
            'r_max': (40, 10, 100),
            'n_r': (50, 10, 200),
            'n_phi': (50, 10, 100),
            'n_spirals': (2, 1, 10),
            'spiral_revolutions': (2, 0.5, 10),
            'sin_amplitude': (0.5, 0.1, 2),
            'sin_frequency': (1, 0.1, 5),
            'x_min': (-10, -50, 0),
            'x_max': (60, 10, 100),
            'y_min': (-10, -50, 0),
            'y_max': (60, 10, 100),
            'n_xy': (50, 10, 200),
            'intersection_threshold': (0.1, 0.01, 1),
            'elev': (20, 0, 90),
            'azim': (45, 0, 360),
            'marker_size': (20, 1, 100)
        }

        for param, (default, min_val, max_val) in self.params.items():
            row_layout = QHBoxLayout()
            
            label = QLabel(param)
            row_layout.addWidget(label)
            
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(int((default - min_val) / (max_val - min_val) * 100))
            slider.valueChanged.connect(lambda value, p=param: self.update_value(p, value))
            self.sliders[param] = slider
            row_layout.addWidget(slider)
            
            textbox = QLineEdit(str(default))
            textbox.setMaximumWidth(100)
            textbox.returnPressed.connect(lambda p=param: self.update_from_textbox(p))
            self.textboxes[param] = textbox
            row_layout.addWidget(textbox)
            
            controls_layout.addLayout(row_layout)

        update_button = QPushButton('Update Plot')
        update_button.clicked.connect(self.update_plot)
        controls_layout.addWidget(update_button)

        scroll_area = QScrollArea()
        scroll_area.setWidget(controls_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area, stretch=1)

        self.setLayout(main_layout)

        self.update_plot()

    def update_value(self, param, value):
        min_val, max_val = self.sliders[param].minimum(), self.sliders[param].maximum()
        param_min, param_max = self.params[param][1], self.params[param][2]
        new_value = param_min + (param_max - param_min) * (value - min_val) / (max_val - min_val)
        self.textboxes[param].setText(f"{new_value:.6g}")

    def update_from_textbox(self, param):
        try:
            value = float(self.textboxes[param].text())
            param_min, param_max = self.params[param][1], self.params[param][2]
            slider_value = int((value - param_min) / (param_max - param_min) * 100)
            self.sliders[param].setValue(slider_value)
        except ValueError:
            pass

    def update_plot(self):
        try:
            # Get current parameter values
            params = {k: float(self.textboxes[k].text()) for k in self.textboxes}

            # Clear previous plots
            self.ax3d.clear()
            self.ax_x0.clear()
            self.ax_z0.clear()

            # Create grids
            r = np.linspace(params['r_min'] * params['AU'], params['r_max'] * params['AU'], int(params['n_r']))
            phi = np.linspace(-np.pi/2, np.pi/2, int(params['n_phi']))
            r, phi = np.meshgrid(r, phi)

            x = np.linspace(params['x_min'] * params['AU'], params['x_max'] * params['AU'], int(params['n_xy']))
            y = np.linspace(params['y_min'] * params['AU'], params['y_max'] * params['AU'], int(params['n_xy']))
            X, Y = np.meshgrid(x, y)

            # Calculate surfaces
            def parker_spiral_surface(r, phi, theta0):
                max_theta = 2 * np.pi * params['spiral_revolutions']
                theta = theta0 + np.minimum(params['omega'] * (r - r.min()) / params['V'], max_theta)
                x = r * np.cos(theta) * np.cos(phi)
                y = r * np.sin(theta) * np.cos(phi)
                z = r * np.sin(phi)
                return x, y, z

            def sinusoidal_surface(x, y):
                return params['sin_amplitude'] * params['AU'] * (np.sin(params['sin_frequency'] * x / params['AU']) + np.sin(params['sin_frequency'] * y / params['AU']))

            # Plot Parker spiral surfaces
            for i in range(int(params['n_spirals'])):
                theta0 = 2 * np.pi * i / params['n_spirals']
                x, y, z = parker_spiral_surface(r, phi, theta0)
                self.ax3d.plot_surface(x, y, z, alpha=0.7, cmap='viridis')

            # Plot sinusoidal surface
            Z_sin = sinusoidal_surface(X, Y)
            self.ax3d.plot_surface(X, Y, Z_sin, alpha=0.5, cmap='plasma')

            # Find intersections
            threshold = params['intersection_threshold'] * params['AU']
            intersections = []
            for i in range(int(params['n_spirals'])):
                theta0 = 2 * np.pi * i / params['n_spirals']
                x_parker, y_parker, z_parker = parker_spiral_surface(r, phi, theta0)
                for i in range(x_parker.shape[0]):
                    for j in range(x_parker.shape[1]):
                        x, y, z = x_parker[i,j], y_parker[i,j], z_parker[i,j]
                        if np.min(np.abs(z - Z_sin)) < threshold:
                            intersections.append([x, y, z])

            intersections = np.array(intersections)

            if len(intersections) > 0:
                # 3D plot
                self.ax3d.scatter(intersections[:, 0], intersections[:, 1], intersections[:, 2], 
                                  color='red', s=params['marker_size'])
                
                # X=0 projection (YZ plane)
                self.ax_x0.scatter(intersections[:, 1], intersections[:, 2], 
                                   color='blue', s=params['marker_size'], label='X=0 Projection')
                
                # Z=0 projection (XY plane)
                self.ax_z0.scatter(intersections[:, 0], intersections[:, 1], 
                                   color='green', s=params['marker_size'], label='Z=0 Projection')

            # Set up 3D plot
            self.ax3d.set_xlabel('X (m)')
            self.ax3d.set_ylabel('Y (m)')
            self.ax3d.set_zlabel('Z (m)')
            self.ax3d.set_title('Parker Spiral and Sinusoidal Surface')
            self.ax3d.view_init(elev=params['elev'], azim=params['azim'])

            # Set up X=0 projection plot
            self.ax_x0.set_xlabel('Y (m)')
            self.ax_x0.set_ylabel('Z (m)')
            self.ax_x0.set_title('Projection of Intersections on X=0 Plane')
            self.ax_x0.grid(True)
            self.ax_x0.legend()
            self.ax_x0.set_aspect('equal')

            # Set up Z=0 projection plot
            self.ax_z0.set_xlabel('X (m)')
            self.ax_z0.set_ylabel('Y (m)')
            self.ax_z0.set_title('Projection of Intersections on Z=0 Plane')
            self.ax_z0.grid(True)
            self.ax_z0.legend()
            self.ax_z0.set_aspect('equal')

            # Update canvas
            self.fig.tight_layout()
            self.canvas.draw()

            # Prime number hypothesis
            print("Note: The Z=0 projection might reveal patterns related to prime numbers.")
            print("Investigate the distribution of points in the Z=0 plane for potential insights.")

        except Exception as e:
            print(f"Error in update_plot: {str(e)}")
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ParkerSpiralApp()
    ex.show()
    sys.exit(app.exec_())