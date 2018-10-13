# Concert Play

Concert Play lets you see upcoming concerts in your city and creates playlists based on those concerts.

This was built with Django, jQuery, Spotify's Web API and Songkick's API.

![Concert Play](http://i.imgur.com/880hWCX.png)

#### Spotify Web API implementation
Creating playlists via Spotify's API must be done on behalf of some Spotify user, which means that playlist creation calls require user authorization. Using 0Auth, I created a refresh token for a "throwaway" Spotify user. This refresh token is then used to create access tokens to create public playlists.

Ultimately, this allows people to create playlists without having to grant Concert Play access to their own Spotify accounts. Instead playlists are created for the throwaway user.


**Important Note**: Without legitimate Spotify/Songkick env variables, most of which are private and won't be shared in this repo, you will not be able to get the main features of this app working locally. The following documentation is only for documentation's sake. I will have a working copy during my on-site.

## Installing and Getting Started

First order of business is to install pip and virtualenv (if they aren't already installed on your machine):
```
sudo easy_install pip
sudo easy_install virtualenv # "pip install virtualenv" should work also
```
Once you have that worked out you'll want to clone the repo, create your virtualenv, install dependencies, and run migrations
```
cd concert_play/
virtualenv myenv
source myenv/bin/activate #activate virtualenv

pip install -r requirements.txt #install python deps
python manage.py migrate #migrate local db
```

After successfully running the previous commands, you will be able to kick start the app with
```
python manage.py runserver ## good starting point is http://127.0.0.1:8000/
```

## Environmental Variables for Concert Play

To get Spotify and Songkick APIs working you will need to set the following env variables:
```
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
SPOTIFY_USER_ID
REFRESH_TOKEN
SONGKICK_API_KEY
```
You can find these settings in <insert teams's password manager>


## Testing

There are no unit tests for this app. I got caught up in the fun of making this app come alive. In a more professional or official context, writing tests would be paramount.




