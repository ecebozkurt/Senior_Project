# Computing and the Arts Senior Project

## Building a Web App for Ranking Classical Music Recordings on Spotify

### Introduction

Spotify is one of the most popular services used for music streaming, with 217 million users worldwide. The application is very successful in recommending songs in mainstream genres, since the team is able to collect a considerable amount of data for their recommendation algorithms due to high demand from users. In a mainstream genre like pop, although interpretations of the same song exist, they are much less common than they are in classical music. In pop, hip-hop, or rock, publishing (songwriting) and recording go hand in hand. Therefore, usually when a user searches for a particular pop song, they are presented with one artist’s recording rather than a plethora of options, and proceed by listening to the only version of the song. 

However, in classical music, interpretations play a very important role. A poor performance can have a substantial impact on how a piece is received by the listener. There are hundreds of different recordings that exist for one piece. Therefore, when a Spotify user looks up a well-known piece like Beethoven’s 9th Symphony, she encounters a long list of recordings, and listening to all of them and picking her favorite one becomes a tough and time consuming decision. 

In this project, I aim to create a Web Application that automates this selection process. The application takes the name and composer of the piece from the user, and retrieves the first page of the Google results associated with the piece. Then, the application parses these forums and reviews to get the most popular recordings made by the most acclaimed performers, and returns a ranking of these recordings to the user. The user can click on these recordings and listen to them on Spotify, and add them to her playlists as she pleases.

### Instructions

1. Make sure that your computer has python 3.x installed. You can check this by opening Terminal, and running the command `python --version`

    If you don't, then install it by using Homebrew. 
    
    To do this, go to [https://brew.sh] and copy the command under the title 'Install Homebrew' into your Terminal and press Enter. Then follow the instructions through your Terminal. 
    
    After Homebrew has been installed, you can run the command `brew install python3` to get the latest version of python 3.x.

2. Then get the latest version of pip by running `pip install --upgrade pip` in your Terminal.

3. Download or Clone this Repository to your computer.

4. Using the requirements.txt file provided in this repository, run the command 

    ` pip install -r requirements.txt`

    This will download all of the libraries you need in order to successfully run this program.

5. Navigate into the folder that includes the .py files through your Terminal.

6. Once you are in this folder, run `python3 app.py`

7. Open your browser and load `127.0.0.1:8081` and start exploring the application!
