# GeometryFlow

GeometryFlow is a project to teach neural network to play Geometry wars retro evolved.

Currently the project is capable of:
	Recording and modifying gameplay data from geometry wars.
	Recording the game using both controller and keyboard
	Training the models
	Using different architectures of neural networks
	Playing the game by simulating both keyboard and controller

Demonstration video.
[![GeometryFlow demonstartion](http://img.youtube.com/vi/vn2aDBqTAI0/0.jpg)](http://www.youtube.com/watch?v=vn2aDBqTAI0)

The demo model takes input as the current picture, uses CNN to decide which keyboard combination to send to the game.

Setup controller playing the game:

1: Download and install vjoy http://vjoystick.sourceforge.net/site/index.php/download-a-install
2: Open 'configure vJoy'
3: Make sure that device 1 is added and vjoy is enabled, axes X, Y, Rx, Ry are enabled and atleast 1 button is in use.
4: Open 'vJoy feeder'
5: open Geometry wars and head to joystick settings
6: use 'vJoy feeder' to rebind shooting to Rx, and Ry and bomb to button 1.
