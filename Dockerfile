FROM tomcat:9-jdk11 AS builder

ENV RDF4J_VERSION="3.5.1" 
ENV RDF4J_DATA="/opt/eclipse-rdf4j-${RDF4J_VERSION}/data" 
ENV JVM_PARAMS="-Xmx4g" 

RUN curl -sS -o /tmp/rdf4j.zip -L http://download.eclipse.org/rdf4j/eclipse-rdf4j-${RDF4J_VERSION}-sdk.zip && \
    cd /opt && \ 
    unzip /tmp/rdf4j.zip && \
    rm /tmp/rdf4j.zip

RUN mv /opt/eclipse-rdf4j-${RDF4J_VERSION}/war/*.war /usr/local/tomcat/webapps

RUN echo "CATALINA_OPTS=\"\$CATALINA_OPTS \$JVM_PARAMS -Dorg.eclipse.rdf4j.appdata.basedir=\$RDF4J_DATA\"" >> /usr/local/tomcat/bin/setenv.sh

VOLUME ${RDF4J_DATA}

EXPOSE 8080

COPY conf/*.xml /usr/local/tomcat/conf/

COPY conf/importTTL.sh /tmp/

RUN apt-get update && apt-get install unattended-upgrades apt-listchanges -y

#COPY cron/crontab /etc/crontab

COPY owl/ /opt/

RUN cat /tmp/importTTL.sh | /opt/eclipse-rdf4j-${RDF4J_VERSION}/bin/console.sh

FROM builder AS production
COPY --from=builder /root/.RDF4J/console/repositories/* /opt/eclipse-rdf4j-${RDF4J_VERSION}/data/server/repositories/atlantgis/

ARG SERVICEJSON=""

RUN rm -rf /usr/local/tomcat/webapps/ROOT/

COPY *.ttl /usr/local/tomcat/

COPY target/proj4rdf-0.0.1-SNAPSHOT.war /tmp/ROOT.war

RUN unzip /tmp/ROOT.war -d /usr/local/tomcat/webapps/ROOT/
