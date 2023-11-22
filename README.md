
## LCAP Listening Test

### Steps to run
1. `git clone https://github.com/mhrice/lcap-listening-test.git`
2. Place all audio in the /static/audio directory. It can be nested in subdirectories.
3. `pip install -r requirements.txt`
4. `flask run`

Every time the server is run, it will generate a new test with a random subset of the audio files. The test will be available at `localhost:5000`.