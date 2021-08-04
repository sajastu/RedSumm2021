
BASE_DIR=/home/code-base/tldr_dataset/machine_splits/

python split_files_for_servers.py

echo "all moved"

echo "Now Compressing"

cd $BASE_DIR

tar -cvf m_0.tar m_0/
gupload m_0.tar

tar -cvf m_1.tar m_1/
gupload m_1.tar

tar -cvf m_2.tar m_2/
gupload m_2.tar

tar -cvf m_3.tar m_3/
gupload m_3.tar

tar -cvf m_4.tar m_4/
gupload m_4.tar

