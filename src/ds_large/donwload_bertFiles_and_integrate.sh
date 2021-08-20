

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

curl -H "Authorization: Bearer ya29.a0ARrdaM91PN40_355-xHL_SzqwqptlpAw0r3goLXGe4zYDAgJkpHbkD5aSjMzRhh6Xo8xJuO9pv9p8Ba07rcZfPCVPKIIuut6huuIODm-94nRXg7n0Zi1e3ZwheUb2cH4xGNmiNxxUWZBGFadia0R9VN8GV61JA" https://www.googleapis.com/drive/v3/files/17t1ADPuRdiyDUdTULDtRj59vpviVgAOO?alt=media -o m0bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM91PN40_355-xHL_SzqwqptlpAw0r3goLXGe4zYDAgJkpHbkD5aSjMzRhh6Xo8xJuO9pv9p8Ba07rcZfPCVPKIIuut6huuIODm-94nRXg7n0Zi1e3ZwheUb2cH4xGNmiNxxUWZBGFadia0R9VN8GV61JA" https://www.googleapis.com/drive/v3/files/19tenZFat7Sj1_gLaHg1iKf7_Ng_L2Jmj?alt=media -o m1bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM91PN40_355-xHL_SzqwqptlpAw0r3goLXGe4zYDAgJkpHbkD5aSjMzRhh6Xo8xJuO9pv9p8Ba07rcZfPCVPKIIuut6huuIODm-94nRXg7n0Zi1e3ZwheUb2cH4xGNmiNxxUWZBGFadia0R9VN8GV61JA" https://www.googleapis.com/drive/v3/files/17fYfAUT4woA5LCybxDWUnM8tR1wF067B?alt=media -o m2bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM91PN40_355-xHL_SzqwqptlpAw0r3goLXGe4zYDAgJkpHbkD5aSjMzRhh6Xo8xJuO9pv9p8Ba07rcZfPCVPKIIuut6huuIODm-94nRXg7n0Zi1e3ZwheUb2cH4xGNmiNxxUWZBGFadia0R9VN8GV61JA" https://www.googleapis.com/drive/v3/files/1js7oGGE3pzsfibLQB1MjySM4oPVqeNWQ?alt=media -o m3bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM91PN40_355-xHL_SzqwqptlpAw0r3goLXGe4zYDAgJkpHbkD5aSjMzRhh6Xo8xJuO9pv9p8Ba07rcZfPCVPKIIuut6huuIODm-94nRXg7n0Zi1e3ZwheUb2cH4xGNmiNxxUWZBGFadia0R9VN8GV61JA" https://www.googleapis.com/drive/v3/files/1MZEqFf0_77TDzdWE3PgFnKOzjSeeGXl-?alt=media -o m4bart.tar

TOKEN=ya29.a0ARrdaM-cSWCzmhHgIW4Tl45FlwmtVy-_REpPnACQFo1jHALjT2JssaVEpBI84oZKqsqgz20PD3CkB3fFl8Hg5i0EC_IiAKDZhR3buYPBcR6vZHkOOehYtt5tTN-_GyH_CBdYbImbV9lqA121AiZcdLLS9m-H
FILES=( 1Hzb0wjTkd-OYqA1zhY-_KE0rBVf3yjA0 1aSqMkWIzJbIJySP7hb0y-MWat0FoB3Xk 1pIgqjOrirjxYGhlHSt9ZoB8nGSQ6MvtG 1tnyxsikxFUKT0w-uo80P84rGrhzcuGbO 1LEE33xhmHt1fD4lHwHTKbWfoGbFp8gLe 1Uk1zeM4XvChO0kewZzdoJYZwgDqQx4OP )

for i in "${!FILES[@]}";
do
  echo $FILES[$i]
  curl -H "Authorization: Bearer $TOKEN" https://www.googleapis.com/drive/v3/files/"${FILES[$i]}"?alt=media -o stat_m$i.pkl
done

FILE_ID=1aXUQst3WfZ8nnd2ZY_gOzYgNi0FJ3jeb
FILE_ID=1CAe_0BDjaKIK4YbHVSQTmciem0bkDXRW
FILE_ID=17t1ADPuRdiyDUdTULDtRj59vpviVgAOO
TOKEN=ya29.a0ARrdaM92_UKKo1Mdkz85EK2AFUPcEX_hLS_e89idGYM21pduYEF4vKqRAS_CtbJJNn6nzygYQYT6cpc_pDlxqpcikpd3-MaoZe8BCYvV5dfTkFmHPTqRqQwIchHNgoY97DfQnfRU916EN8aRqQnGa9lbUqgf
curl -H "Authorization: Bearer $TOKEN" https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media -o m1fullBert.tar

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

