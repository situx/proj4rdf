FROM tomcat:9

RUN apt-get update

RUN apt-get install unattended-upgrades apt-listchanges -y