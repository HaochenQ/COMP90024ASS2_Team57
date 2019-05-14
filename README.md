# Instructions:

## VM:
1. Go to COMP90024ASS2/ansible/instances
2. Run run-nectar.sh, password can be found in COMP90024ASS2/ansible/instances/password&profile.txt
---------------------------------------------------------------------------
## Couchdb:
1. Go to COMP90024ASS2/ansible/couchdb
2. Run ansible-playbook install_configure_couchdb.yml --key-file "CCC-keypair.pem" --extra-vars "ansible_sudo_pass=<your_sudo_password>" -i hosts.ini, it will 
  1) install docker 
  2) install couchdb via docker 
  3) configure couchdb(change hostname and set cookies)
3. To join nodes into cluster, either getting it done by loging into Fauxton
(a GUI for couchdb database management, this method is the preferred methods in official documentation) or by running couchdb_joincluster.sh.

---------------------------------------------------------------------------
## Twitter analysis:

1. Go to COMP90024ASS2/ansible/twitter_analysis:
    
    cd path/to/COMP90024ASS2/ansible/twitter_analysis

2. Run run_twitter_analysis.sh file to start the ansible, it will:
 (1) install the docker-ce, docker-compose and useful packages. 
 (2) transfer all twitter analysis files to remote instances
 (3) build the spark using docker
 (4) read docker-compose,yml

    sudo ./run_twitter_analysis.sh

3. Go to the remote server (in our project it is 45.113.235.188):
    
    docker exec -ti spark_spark-master_1 /bin/bash

in the spark master bash, execute: 
    
    ./bin/spark-submit /root/wa.py --word2vec=True --syms_num=100

more arguments refer to parser in code wa.py.

Then the results will be stored in couchdb on server (default in database data_analysis)

---------------------------------------------------------------------------
## Twitter correlation analysis:

---------------------------------------------------------------------------
## Web deploy:

1. Go to COMP90024ASS2/web:

    cd path/to/COMP90024ASS2/web
    
2. Run command:

    pip3 install -r requirements.txt

   to install the useful packages. 

3. Then execute:
    
    python3 ass2.py
    
    The username and the password of the website are both "admin"

4. Then open a new terminal and enter curl sentences, then, the ReSTful API can be used. There are three resources: twitter_tasks, aurin_tasks and analysis_tasks. And the sample commands are:
    
    Get a whole list of tasks:
        curl -XGET http://localhost:5000/twitter/api/twitter_tasks --basic --user admin:admin -H "Content-Type: application/json"
    
    Get a specific task:
        curl -XGET http://localhost:5000/twitter/api/twitter_tasks/sydney --basic --user admin:admin -H "Content-Type: application/json"

    Create a new task:
        curl -XPOST http://localhost:5000/twitter/api/twitter_tasks --basic --user admin:admin -H "Content-Type: application/json" -d '{"city":"cairns"}'
    
    Update a task:
        curl -XPUT http://localhost:5000/twitter/api/twitter_tasks/cairns --basic --user admin:admin -H "Content-Type: application/json" -d '{"city":"Cairns", "total_twitter": 50}'
    
    Delete a task:
        curl -XDELETE http://localhost:5000/twitter/api/twitter_tasks/cairns --basic --user admin:admin -H "Content-Type: application/json"
