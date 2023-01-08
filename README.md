# python-sales-bot

## Requirements
- Docker
- Python3 / Pip3 (if you don't have Docker or want to do local development and testing without using Docker)
- OpenSEA API Key
- Twitter API Keys

## Getting Started: Local development/testing steps (Using Docker)

- Make sure docker is installed and working on your local workstation/laptop.
- create new github branch (done, "check_mints" branch has been created).
- docker login --username <username> (omit the password in the login command. Instead, enter your token when asked for a password).

- Using Docker for Local dev /testing:
- clone the repo
- git checkout whatever branch needed (ex. git checkout get_mints)
- Note, these next 2 files are in the .gitigore by design (we do not want to check in API keys to git!)
- If not already created, create file: .env_test (Will have to contain only Twitter API keys)
- If not already created, create file: .env_prod (Will have to contain Twitter and OpenSea API keys)
- Make sure docker works (ex. docker run -it jkendall1975/python-salesbot:1.0.0-get-mints /salesbot/salesbot.py "pixawitches" --mints -t)
- make code changes!
- docker build based on branch name (ex. docker build . -t jkendall1975/python-salesbot:1.0.0-get-mints)
- Test locally with docker run (ex. docker run -it jkendall1975/python-salesbot:1.0.0-get-mints /salesbot/salesbot.py "pixawitches" --mints -t)
- Once code works:
- git add, commit, push to the branch when ready!
- Create PR to main branch when ready  
- git checkout main branch
- docker build main branch 
- docker push (ex: docker push jkendall1975/python-salesbot:1.0.0-get-mints)
- docker run with new image tag on AWS host after docker system prune -a on AWS host (note this will nuke current sales bot! Ask jlk if any questions on this part!)
- If docker run witb new image tag on AWS host looks good, then docker system prune -a again, and update the crontab job with new image tag and any new command line flags etc.
- Wait until next cron run, then run docker logs salesbot to make sure no errors!

## Getting Started: Local development/testing steps (Not Using Docker)
- git checkout whatever branch needed (ex. git checkout get_mints)
- create file: .env_test (Will have to contain only Twitter API keys)
- create file: .env_prod (Will have to contain Twitter and OpenSea API keys)
- python3 -m venv venv
- source ./venv/bin/activate
- pip install -r ./requirements.txt
- python3 ./salesbot.py "pixawitches" --mints -t
- make code changes, run python3 ./salesbot.py "pixawitches" --mints -t again to test!
- Once code works:
- git add, commit, push to the branch when ready!
- Create PR to main branch when ready (ideally should have tested docker container works ok before this step though, and should have pushed a working docker image to dockerhub so we can point the crontab on the AWS server to that new image!.)



## Print Help/Usage

`python ./salesbot/salesbot.py -h`

`docker run -it jkendall1975/python-salesbot:1.0.0-get-mints /salesbot/salesbot.py -h`

usage: salesbot [-h] [-s SLEEP] [-d] [-db] [-t] [-p] [-m] Collections

Check for NFT Sales

positional arguments:
  Collections           the nft collection to check

optional arguments:

  -h, --help            show this help message and exit

  -s SLEEP, --sleep SLEEP
                        Time to Sleep in Seconds before next API call

  -d, --dryrun          DRY RUN, WILL NOT SEND TWEETS

  -db, --database       PRINT DATABASE FILE (db.JSON)

  -t, --test            FOR TESTING, WILL USE .env_test for ENV variables if set.

  -p, --pause           FOR TESTING, WILL PAUSE SCRIPT FOR SLEEP TIME.

  -m, --mints           GET NEW "MINTS" (instead of Sales).

## Examples (Docker)

### Check only pixawitches collection for new sales, sleep 5 seconds between API calls, and do not actually send out any Tweets (dryrun)

`docker run -it jkendall1975/python-salesbot:1.0.1 /salesbot/salesbot.py "pixawitches" --sleep 5 --dryrun`

### Another Example

`docker run -it jkendall1975/python-salesbot:1.0.7 /salesbot/salesbot.py "pixawitches" --sleep 60 --database --test --pause --dryrun`

### Cleanup container on each run

`docker run --rm --name salesbot -v ~/salesbot/data:/salesbot/data -it jkendall1975/python-salesbot:1.0.8 /salesbot/salesbot.py "pixawitches" --sleep 5 --database --test --pause --dryrun`

## Examples (No Docker)

`python3 ./salesbot.py "pixawitches" --sleep 5 --dryrun --database -t -p`

`python3 ./salesbot.py "pixawizards pixawyverns pixabrews relics-of-the-pixarealm pixawitches" --sleep 5 --dryrun`

`python3 ./salesbot.py "pixawitches" --sleep 5 --dryrun`

### -t flag: Use .env_test file (Use Testing API keys for Twitter..)

`python3 ./salesbot.py "pixawitches" --sleep 5 --dryrun -t`
 

## db.json File Example

NOTE: This file is where the salesbot stores last sale date/time stamps for each collection.) Currently, the file must be added /created manually on the host where the docker container runs and mounted to the running docker container with the docker run -v <local_dir:container_dir> convention. 

`{"pixawizards": "2022-03-21T22:21:55.278824", "pixawyverns": "2022-03-26T08:51:12.484808", "pixabrews": "2022-03-16T07:44:50.643085", "relics-of-the-pixarealm": "2022-01-28T15:35:04.526175", "pixawitches": "2022-02-28T15:46:16.348208"}`

## Crontabs
*/30 * * * * docker start salesbot || docker run --name salesbot -v ~/salesbot/data:/salesbot/data jkendall1975/python-salesbot:1.0.8 /salesbot/salesbot.py "pixawizards pixawyverns pixabrews relics-of-the-pixarealm pixawitches" --sleep 30