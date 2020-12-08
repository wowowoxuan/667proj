# 667proj
Required package: 

1.python 3.6.8

2.numpy 1.18.4

3.torch==1.2.0

4.torchfile==0.1.0

5.torchsummary==1.5.1

6.torchvision==0.4.0

7.matplotlib==3.1.1

Download python:

https://www.python.org/downloads/


After python is installed, run: pip install -r requirements.txt to download the required packages.

The /667proj/requirements.txt is a simplified version of /667proj/environment/requirements.txt, I delete the packages which are not used in the project and test on my computer, if /667proj/requirements.txt did not works well, please use the /667proj/environment/requirements.txt.

If you want to take a look at the code, in the ./game file, the connect4withaimodify.py is the code for playing the game.

The CNN.py is the NN model and CNN model training, testing and implementation.

The generate_data.py will call some function in connect4withai.py to generate the training data.

drawloss.py and drawscore.py is the code for drawing the figures in the paper.

The pretrained model used in the experiments is stored in the pretrained folder.

The generated data is stored in the data folder.

After the environment is set up, run:

python playwithai.py

it will show you how to select the player and play the game. In the final project, you can only select 7x7, 8x8, 9x9, 10x10, 11x11 board, because the NN model is trained on these board size.
