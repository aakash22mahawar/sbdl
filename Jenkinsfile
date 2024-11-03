pipeline {
    agent any

    environment {
        CONDA_ENV = 'pyspark'  // Name of the Conda environment you want to use
        CONDA_HOME = '/home/ubuntu/miniconda3'  // Path to your Conda installation
    }

    stages {
        stage('Setup Conda Environment') {
            steps {
                script {
                    // Initialize Conda and create the environment if it doesn't exist
                    echo "Setting up Conda environment '${CONDA_ENV}'"
                    sh '''
                        #!/bin/bash
                        echo "Sourcing Conda profile..."
                        source "${CONDA_HOME}/etc/profile.d/conda.sh"
                        
                        echo "Checking if environment '${CONDA_ENV}' exists..."
                        if conda env list | grep -q "^${CONDA_ENV} "; then
                            echo "Environment '${CONDA_ENV}' already exists."
                        else
                            echo "Environment '${CONDA_ENV}' does not exist. Creating it now..."
                            conda create -n "${CONDA_ENV}" python=3.10.0 -y
                            echo "Environment '${CONDA_ENV}' created successfully."
                        fi
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Activate Conda environment and sync dependencies
                    echo "Activating Conda environment '${CONDA_ENV}' and installing dependencies"
                    sh '''
                        #!/bin/bash
                        source "${CONDA_HOME}/etc/profile.d/conda.sh"
                        conda activate "${CONDA_ENV}"
                        
                        echo "Installing dependencies from requirements.txt..."
                        conda install --file requirements.txt -y
                        echo "Dependencies installed successfully."
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Activate Conda environment and run tests
                    echo "Activating Conda environment '${CONDA_ENV}' and running tests"
                    sh '''
                        #!/bin/bash
                        source "${CONDA_HOME}/etc/profile.d/conda.sh"
                        conda activate "${CONDA_ENV}"
                        
                        echo "Running tests with pytest..."
                        pytest
                        echo "Tests completed."
                    '''
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
                    echo "Packaging files into sbdl.zip"
                    sh "zip -r sbdl.zip lib"
                    echo "Packaging complete."
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
                    echo "Transferring files to QA environment"
                    sh '''
                        scp -i /home/ubuntu/cred/aakash_jenkins.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.sh conf ubuntu@13.60.22.207:/home/ubuntu/sbdl-qa
                        echo "Files transferred to QA environment."
                    '''
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
                    echo "Transferring files to production environment"
                    sh '''
                        scp -i /home/ubuntu/cred/aakash_jenkins.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.sh conf ubuntu@13.60.22.207:/home/ubuntu/sbdl-prod
                        echo "Files transferred to production environment."
                    '''
                }
            }
        }
    }
}
