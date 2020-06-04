cat bcc-lj.xyz lj.xyz > all.xyz

asap gen_desc -f all.xyz soap -c 3.0 -n 8 -l 6 -g 0.2 -pa

asap map -f ASAP-desc.xyz -dm '[*]' -c fcccubic -clab 'fcc order parameter' -ua -s journal -o none -p pca pca
