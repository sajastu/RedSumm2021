

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
fileid="17fYfAUT4woA5LCybxDWUnM8tR1wF067B"
filename="m2bart.tar"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /home/code-base/
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

curl -H "Authorization: Bearer ya29.a0ARrdaM9pkuVRkPA8Ow14uK3T4hJv7S_0owD2lntA-QsROLWPcY1OMNGA6wxZgMzAshrbnhNgvFAzEX2-V-gYn4fs67ld2ui1u3M1y_GkiHgwc10d8p92EA7kg0fUAp7oDM0O1BoQ7tEihCHnj1qQGdbhAw5R" https://www.googleapis.com/drive/v3/files/17t1ADPuRdiyDUdTULDtRj59vpviVgAOO?alt=media -o m0bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM9pkuVRkPA8Ow14uK3T4hJv7S_0owD2lntA-QsROLWPcY1OMNGA6wxZgMzAshrbnhNgvFAzEX2-V-gYn4fs67ld2ui1u3M1y_GkiHgwc10d8p92EA7kg0fUAp7oDM0O1BoQ7tEihCHnj1qQGdbhAw5R" https://www.googleapis.com/drive/v3/files/19tenZFat7Sj1_gLaHg1iKf7_Ng_L2Jmj?alt=media -o m1bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM9pkuVRkPA8Ow14uK3T4hJv7S_0owD2lntA-QsROLWPcY1OMNGA6wxZgMzAshrbnhNgvFAzEX2-V-gYn4fs67ld2ui1u3M1y_GkiHgwc10d8p92EA7kg0fUAp7oDM0O1BoQ7tEihCHnj1qQGdbhAw5R" https://www.googleapis.com/drive/v3/files/17fYfAUT4woA5LCybxDWUnM8tR1wF067B?alt=media -o m2bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM9pkuVRkPA8Ow14uK3T4hJv7S_0owD2lntA-QsROLWPcY1OMNGA6wxZgMzAshrbnhNgvFAzEX2-V-gYn4fs67ld2ui1u3M1y_GkiHgwc10d8p92EA7kg0fUAp7oDM0O1BoQ7tEihCHnj1qQGdbhAw5R" https://www.googleapis.com/drive/v3/files/1js7oGGE3pzsfibLQB1MjySM4oPVqeNWQ?alt=media -o m3bart.tar
curl -H "Authorization: Bearer ya29.a0ARrdaM9pkuVRkPA8Ow14uK3T4hJv7S_0owD2lntA-QsROLWPcY1OMNGA6wxZgMzAshrbnhNgvFAzEX2-V-gYn4fs67ld2ui1u3M1y_GkiHgwc10d8p92EA7kg0fUAp7oDM0O1BoQ7tEihCHnj1qQGdbhAw5R" https://www.googleapis.com/drive/v3/files/1MZEqFf0_77TDzdWE3PgFnKOzjSeeGXl-?alt=media -o m4bart.tar