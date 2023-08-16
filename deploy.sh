cd backend-repo-team-data-dukes
 git pull origin master
 pm2 kill
 pm2 start fastapi-config.json
