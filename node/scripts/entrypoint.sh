SCRIPT_DIR=$SCRIPTDIR_DOCKER
WORK_DIR=$WORKDIR_DOCKER
HOST_UID=1000

NODE_MODULES_DIR=${WORKDIR_DOCKER}node_modules/

if [ ! -e ${WORKDIR_DOCKER}package.json ]; then
  echo 'INFO: Modules not installed.'
  echo 'INFO: You must exec `npm init` and install selenium-webdriver typescript @types/selenium-webdriver.'
  chown -R $HOST_UID $WORKDIR_DOCKER
fi
bash