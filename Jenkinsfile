pipeline {
    agent any

    environment {
        VENV = "venv"
        DEPLOY_DIR = "/tmp/flask_task_app"
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

       stage('Run Unit Tests') {
    steps {
        sh '''
            . venv/bin/activate
            pytest ./tests.py
        '''
    }
}


        stage('Build Application') {
            steps {
                sh '''
                    mkdir -p build
                    tar -czf build/flask_app.tar.gz .
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    mkdir -p ${DEPLOY_DIR}
                    tar -xzf build/flask_app.tar.gz -C ${DEPLOY_DIR}
                '''
            }
        }
    }
}
