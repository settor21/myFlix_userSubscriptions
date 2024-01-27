pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = 'xxxxx'
        PROD_DIR = '/home/amedikusettor/myflix/user-subscriptions'
        DOCKER_IMAGE_NAME = 'user-subscriptions-deployment'
        DOCKER_CONTAINER_NAME = 'user-subscriptions'
        DOCKER_CONTAINER_PORT = '5002'
        DOCKER_HOST_PORT = '5002'
    }

    stages {
        stage('Load Code to Workspace') {
            steps {
                checkout scm
            }
        }

        stage('Deploy Repo to Prod. Server') {
            steps {
                script {
                    sh 'echo Packaging files ...'
                    sh 'tar -czf usersubscriptions_files.tar.gz *'
                    sh "scp -o StrictHostKeyChecking=no usersubscriptions_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix/user-subscriptions && tar -xzf usersubscriptions_files.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to dockerize application ..'
                }
            }
        }

        stage('Dockerize Application') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-subscriptions && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for userSubscriptions rebuilt. Preparing to redeploy container to web..."
                }
            }
        }

        stage('Redeploy Container to Web') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-subscriptions && docker stop ${DOCKER_CONTAINER_NAME} || echo \"Failed to stop container\"'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-subscriptions && docker rm ${DOCKER_CONTAINER_NAME} || echo \"Failed to remove container\"'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"
                    
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-subscriptions && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                    sh "echo userSubscriptions Microservice Deployed!"
                }
            }
        }
    }
}
