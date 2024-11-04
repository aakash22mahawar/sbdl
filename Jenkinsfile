pipeline {
    agent any

    environment {
        CONDA_ENV = 'pyspark'                   // Name of the Conda environment you want to use
        CONDA_HOME = '/home/ubuntu/miniconda3'  // Path to your Conda installation
    }

    stages {
        stage('Setup Conda Environment') {
            steps {
                script {
                    // Check if Conda environment exists, create it if necessary
                    sh """
                        ${CONDA_HOME}/bin/conda env list | grep -q "^${CONDA_ENV} " || ${CONDA_HOME}/bin/conda create -n ${CONDA_ENV} python=3.10.0 -y
                    """
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Use conda run to install dependencies
                    sh """
                        ${CONDA_HOME}/bin/conda run -n ${CONDA_ENV} conda install --file requirements.txt -y
                    """
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Use conda run to execute pytest within the Conda environment
                    sh """
                        ${CONDA_HOME}/bin/conda run -n ${CONDA_ENV} pytest
                    """
                }
            }
        }

        stage('Package') {
            when {
                anyOf {
                    branch "master"
                    branch 'release'
                }
            }
            steps {
                script {
                    // Package files
                    sh "zip -r sbdl.zip lib"
                }
            }
        }

        stage('Release') {
            when {
                branch 'release'
            }
            steps {
                script {
                    // Transfer files to the QA environment
                    sh """
                        scp -i /home/ubuntu/cred/aakash_jenkins.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.sh conf ubuntu@13.60.22.207:/home/ubuntu/sbdl-qa
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                script {
                    // Transfer files to the production environment
                    sh """
                        scp -i /home/ubuntu/cred/aakash_jenkins.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.sh conf ubuntu@13.60.22.207:/home/ubuntu/sbdl-prod
                    """
                }
            }
        }
    }
}
