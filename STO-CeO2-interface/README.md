asap gen_desc --fxyz asap_titerm_b4_export.xyz --prefix SOAP_titerm_b4_export soap -u minimal -e

asap map --fxyz SOAP_titerm_b4_export.xyz -dm '[SOAP-n4-l3-c4.6-g0.58-e]' -c energy pca

asap map --fxyz SOAP_titerm_b4_export.xyz -dm '[SOAP-n4-l3-c4.6-g0.58-e]' -c energy skpca -n 100 -s fps -k polynomial -kp 2

asap fit -f SOAP_titerm_b4_export.xyz -dm '[SOAP-n4-l3-c4.6-g0.58-e]' --y energy ridge


