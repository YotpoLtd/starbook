#!/usr/bin/env bash
#
# Tag and push git and Docker

sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_BRANCH}
sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_BRANCH}
sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_BRANCH}
sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_BRANCH}

if [[ $TRAVIS_BRANCH == "master" ]]; then
  echo "Yay, it's release branch, let's tag it and bump docker images!"
  git config user.email "travis-ci@yotpo.com"
  git config user.name "Travis CI"
  git tag -a "v-${BUILD_DATE}" -m "Committed by Travis-CI ${TRAVIS_BUILD_NUMBER} [ci skip]"
  git push --tags

  sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:v-${BUILD_DATE}
  sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:latest
  sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:v-${BUILD_DATE}
  sudo docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:latest
  sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:v-${BUILD_DATE}
  sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:latest
  sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:v-${BUILD_DATE}
  sudo docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:latest

fi
