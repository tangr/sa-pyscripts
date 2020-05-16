import queue
import threading
# import urllib2
import urllib.request
import time
# from beautifulsoup4 import BeautifulSoup
from bs4 import BeautifulSoup

# https://developer.ibm.com/articles/au-threadingpython/#using-queues-with-threads

hosts = ["http://yahoo.com", "http://google.com",
        "http://ibm.com", "http://apple.com"]
in_queue = queue.Queue()
out_queue = queue.Queue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, outqueue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.outqueue = outqueue

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            # url = urllib2.urlopen(host)
            url = urllib.request.urlopen(host)
            chunk = url.read()

            #place chunk into out queue
            self.outqueue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            soup = BeautifulSoup(chunk, features="html.parser")
            print(soup.findAll(['title']))

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()
def main():
    #populate queue with data
#!/usr/bin/env bash

CRS_FTP_URL=${CRS_FTP_URL}
CRS_FTP_USER=${CRS_FTP_USER}
CRS_FTP_PSWD=${CRS_FTP_PSWD}
CRS_BUILD_ID=${CRS_BUILD_ID}
CRS_BUILD_NAME=${CRS_BUILD_NAME}
CRS_BUILD_SIGN=${CRS_BUILD_SIGN}

crs_pkg_pre=/data/crs_pkg_pre
crs_pkg_suf=/data/crs_pkg_suf

log_info() {
    retcode=$1
    if [[ $retcode == 0 ]]; then
        printf '%s\n' '**********************************************************'
        printf '%s\n' "$2"
    fi
}

log_error() {
    retcode=$1
    if [[ $retcode != 0 ]]; then
        printf '%s\n' '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        printf '%s\n' "$2"
        exit 1
    fi
}

mkdir -p ${crs_pkg_suf}/${CRS_BUILD_NAME}

# export MAVEN_HOME=/usr/share/apache-maven
# export M2_HOME=/usr/share/apache-maven
# export HOME=/root

mvn -v -s /root/.m2/settings.xml
# export MAVEN_HOME=/usr/share/apache-maven
# export M2_HOME=/usr/share/apache-maven
# export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.222.b10-0.el7_6.x86_64/jre
export LANG=en_US.UTF-8

GIT_REPO_DIR="/data/releases/nlp-tools"
cd ${GIT_REPO_DIR}
log_error $? "Change to directory ${GIT_REPO_DIR} failed!!!"
log_info 0 "Change to directory .."
pwd

log_info 0 "Begin git pull ..."
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin git checkout master ..."
git checkout master 2>/tmp/crs_${CRS_BUILD_ID}_error.log
log_error $? "git checkout master failed!!!"
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin mvn clean install ..."
# env > /tmp/env
# set > /tmp/set
mvn -s /root/.m2/settings.xml clean install > /tmp/crs_${CRS_BUILD_ID}_mvn_nlp-tools.log
log_error $? "mvn clean install failed!!!"

GIT_REPO_DIR="/data/releases/translation-fsa"
cd ${GIT_REPO_DIR}
log_error $? "Change to directory ${GIT_REPO_DIR} failed!!!"
log_info 0 "Change to directory .."
pwd

log_info 0 "Begin git pull ..."
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin git checkout master ..."
git checkout master 2>/tmp/crs_${CRS_BUILD_ID}_error.log
log_error $? "git checkout master failed!!!"
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin mvn clean install ..."
mvn -s /root/.m2/settings.xml clean install > /tmp/crs_${CRS_BUILD_ID}_mvn_translation-fsa.log
log_error $? "mvn clean install failed!!!"

GIT_REPO_DIR="/data/releases/infra-poa/sentiment-analyzer"
cd ${GIT_REPO_DIR}
log_error $? "Change to directory ${GIT_REPO_DIR} failed!!!"
log_info 0 "Change to directory .."
pwd

log_info 0 "Begin git pull ..."
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin git checkout master ..."
git checkout master 2>/tmp/crs_${CRS_BUILD_ID}_error.log
log_error $? "git checkout master failed!!!"
git pull
log_error $? "git pull failed!!!"

log_info 0 "Begin mvn clean install ..."
mvn -s /root/.m2/settings.xml clean install > /tmp/crs_${CRS_BUILD_ID}_mvn_sentiment-analyzer.log
log_error $? "mvn clean install failed!!!"

CODE_DIR="/data/releases/infra-poa/sen-log/"
cd ${CODE_DIR}
log_error $? "Change to directory ${CODE_DIR} failed!!!"
log_info 0 "Change to directory .."
pwd

git log -1 > zzz_git_log_top1.txt

log_info 0 "Begin untar sentiment-analyzer ..."
tar zxf ../sentiment-analyzer/target/releases/sentiment-analyzer-1.0.0-SNAPSHOT.tar.gz -C lib/
log_error $? "untar sentiment-analyzer failed!!!"

# custom action begion

# custom action end

log_info 0 "Begin tar package ..."
tar pshczf ${crs_pkg_suf}/${CRS_BUILD_NAME}/${CRS_BUILD_SIGN}.tgz --exclude "*/.git*" *
log_error $? "tar package failed!!!"

log_info 0 "Begin upload package ..."
curl -u ${CRS_FTP_USER}:${CRS_FTP_PSWD} -T ${crs_pkg_suf}/${CRS_BUILD_NAME}/${CRS_BUILD_SIGN}.tgz ${CRS_FTP_URL}/${CRS_BUILD_NAME}/ --ftp-create-dirs
log_error $? "tar package failed!!!"

exit 0


    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(in_queue, out_queue)
        t.setDaemon(True)
        t.start()

    for i in range(5):
        dt = DatamineThread(out_queue)
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed
    in_queue.join()
    out_queue.join()

if __name__ == '__main__':
    main()
    print("Elapsed Time: %s" % (time.time() - start))
