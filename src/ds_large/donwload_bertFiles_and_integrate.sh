

##################  Configs

export STORE_DIR=/home/code-base/large_reddit_bertfiles
mkdir -p $STORE_DIR

# m0
URL_m0=https://drive.google.com/file/d/17t1ADPuRdiyDUdTULDtRj59vpviVgAOO/edit

# m1
URL_m1=https://drive.google.com/file/d/19tenZFat7Sj1_gLaHg1iKf7_Ng_L2Jmj/edit

# m2
URL_m2=https://drive.google.com/file/d/17fYfAUT4woA5LCybxDWUnM8tR1wF067B/view

# m3
URL_m3=https://drive.google.com/file/d/ /view

# m4
URL_m4=https://drive.google.com/file/d/1MZEqFf0_77TDzdWE3PgFnKOzjSeeGXl-/edit

################## first Download bertFiles [m0, ..., m4]
#perl gdown/gdownload.pl  $URL_m0 m0-bertFiles.tar
#perl gdown/gdownload.pl  $URL_m1 m1-bertFiles.tar
cd gdown
perl gdownload.pl  $URL_m2 $STORE_DIR/m_2-bertfiles.tar
#perl gdownload.pl  $URL_m3 $STORE_DIR/m_3-bertfiles.tar

#perl gdown/gdownload.pl  $URL_m4 m4-bertFiles.tar

################## Uncompressing bertfiles, should note that it should not interfere names


TOKEN=ya29.a0ARrdaM-4wpoDdKuUlFRJUWLvXz8G1VpK-HcXbpryi4QPjxW88FykNtJmUmQgkUfrcbobjwAOt0WFu5lUw8-hsWPqbxf7LC99FZPbUQCerhZI5Rvugh6kU86Ma4yBo5gNoWnUA2vC_dbYu7i2noq4JyRborD1
FILES=( 1Hzb0wjTkd-OYqA1zhY-_KE0rBVf3yjA0 1aSqMkWIzJbIJySP7hb0y-MWat0FoB3Xk 1pIgqjOrirjxYGhlHSt9ZoB8nGSQ6MvtG 1tnyxsikxFUKT0w-uo80P84rGrhzcuGbO 1LEE33xhmHt1fD4lHwHTKbWfoGbFp8gLe 1Uk1zeM4XvChO0kewZzdoJYZwgDqQx4OP )

FILES=( 1Hzb0wjTkd-OYqA1zhY-_KE0rBVf3yjA0 1LEE33xhmHt1fD4lHwHTKbWfoGbFp8gLe 1Uk1zeM4XvChO0kewZzdoJYZwgDqQx4OP 1aSqMkWIzJbIJySP7hb0y-MWat0FoB3Xk 1pIgqjOrirjxYGhlHSt9ZoB8nGSQ6MvtG 1tnyxsikxFUKT0w-uo80P84rGrhzcuGbO )
for i in "${!FILES[@]}";
do
  echo $FILES[$i]
  curl -H "Authorization: Bearer $TOKEN" https://www.googleapis.com/drive/v3/files/"${FILES[$i]}"?alt=media -o m$i-tldrQ.tar
done


https://drive.google.com/drive/folders/12n3fTqvjrP7X4V29eANUZi3DJs5KlCYo?usp=sharing

FILE_ID=1S1UsUc0vomFRWpPl7a0pf9U83Pqq6UcC
TOKEN=ya29.a0ARrdaM_YIJ1wIpHSA9uQ0GCg8Lc7Hc6TysEcTi9-S0nYU14UmJtPZXoQJnsfWbC3FP-9JJVSXcBzKBooQ15h7XUJuy38l6qrmbxlUlQPY6JckHr1nsfOddD_Y-mWTBeLqnzlLu6DdVy9QF-W1hDNqUPEMuOX
curl -H "Authorization: Bearer $TOKEN" https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media -o dl.tar

https://drive.google.com/open?id=14v75CTKcdkBHv9e70k5L3HkQRZyjpPnu # ext model large


tar -xf m0bart.tar
rm m0bart.tar

tar -xf m1bart.tar
rm m1bart.tar

tar -xf m2bart.tar
rm m2bart.tar

tar -xf m3bart.tar
rm m3bart.tar

tar -xf m4bart.tar
rm m4bart.tar



#perl gdown/gdownload.pl $URL_m3 m3-bertFiles.tar && tar -xf m3-bertFiles.tar --directory /home/code-base/large_reddit_bertfiles/
#perl gdown/gdownload.pl https://drive.google.com/file/d/1-PuqDptfdrCQAXSetJkKK-Oj8cj27Ri3/edit m3-bertFiles.tar

#!/bin/bash

