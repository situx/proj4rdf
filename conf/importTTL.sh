#connect "http://localhost:8080/rdf4j-server".
show repositories.
create native-shacl.
atlantgis
atlantgisstore
10000
spoc

open atlantgis.
load "/opt/result.ttl".
load "/opt/countries.ttl".
load "/opt/proj4rdf_data.ttl".
close.
quit.