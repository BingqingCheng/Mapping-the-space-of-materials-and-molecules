asap gen_desc -f dataset_1593_eVAng.xyz soap -u longrange

asap map -f ASAP-desc.xyz -dm '[SOAP-n8-l4-c4.0-g0.41,SOAP-n8-l4-c2.0-g0.21]' -c volume -clab 'volume/atom [$\AA^3$]' -s journal -p kpca-volume -o none skpca -k polynomial -kp 2 -n -1 --no-scale

asap map -f ASAP-desc.xyz -dm '[SOAP-n8-l4-c4.0-g0.41,SOAP-n8-l4-c2.0-g0.21]' -c TotEnergy -clab 'relative energy [eV]' -c0 -s journal -p kpca-energy -o none skpca -k polynomial -kp 2 -n -1 --no-scale


