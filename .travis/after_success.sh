#!/usr/bin/env bash
#
# Tag and push git and Docker

set -x
set -i

docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_BRANCH}
docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_BRANCH}
docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_BRANCH}
docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_BRANCH}

if [[ $TRAVIS_BRANCH == "master" ]]; then
  echo "Yay, it's release branch, let's tag it and bump docker images!"

  echo "Pushing images latest and v-${BUILD_DATE} images"

  docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:v-${BUILD_DATE}
  docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:latest
  docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:v-${BUILD_DATE}
  docker tag 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:${TRAVIS_COMMIT} 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:latest
  docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:v-${BUILD_DATE}
  docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/front:latest
  docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:v-${BUILD_DATE}
  docker push 402837048690.dkr.ecr.us-east-1.amazonaws.com/${PROJECT}/back:latest

fi
