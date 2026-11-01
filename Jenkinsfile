pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'

        AWS_ACCOUNT_ID = '697245141888'

        ECR_REPOSITORY = 'sample-flask-app'

        ECR_REGISTRY =
            "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        ECR_IMAGE =
            "${ECR_REGISTRY}/${ECR_REPOSITORY}"

        DEPLOY_HOST = '172.31.33.47'

        APP_PORT = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out GitHub source code'

                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing application dependencies'

                sh '''
                    python3 -m venv .venv

                    .venv/bin/pip install \
                    -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running Python unit tests'

                sh '''
                    .venv/bin/python -m unittest -v
                '''
            }
        }

        stage('Docker Image Build') {
            steps {
                echo 'Building Docker image'

                sh '''
                    docker build \
                    -t ${ECR_IMAGE}:${BUILD_NUMBER} \
                    -t ${ECR_IMAGE}:latest .
                '''
            }
        }

        stage('Docker Image Push') {
            steps {
                echo 'Authenticating with Amazon ECR'

                sh '''
                    aws ecr get-login-password \
                    --region ${AWS_REGION} |
                    docker login \
                    --username AWS \
                    --password-stdin ${ECR_REGISTRY}
                '''

                echo 'Pushing image to Amazon ECR'

                sh '''
                    docker push ${ECR_IMAGE}:${BUILD_NUMBER}

                    docker push ${ECR_IMAGE}:latest

                    docker logout ${ECR_REGISTRY}
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deploying image to Application EC2'

                sshagent(credentials: ['ec2-deploy-key']) {

                    sh '''
                        ssh -o BatchMode=yes \
                        ubuntu@${DEPLOY_HOST} "

                            aws ecr get-login-password \
                            --region ${AWS_REGION} |
                            docker login \
                            --username AWS \
                            --password-stdin ${ECR_REGISTRY}

                            docker pull ${ECR_IMAGE}:${BUILD_NUMBER}

                            docker rm -f sample-app || true

                            docker run -d \
                            --name sample-app \
                            --restart unless-stopped \
                            -p ${APP_PORT}:5000 \
                            -e APP_VERSION=${BUILD_NUMBER} \
                            ${ECR_IMAGE}:${BUILD_NUMBER}

                            docker logout ${ECR_REGISTRY}
                        "
                    '''
                }
            }
        }

        stage('Deployment Verification') {
            steps {
                echo 'Checking application health'

                sh '''
                    curl --fail \
                    --retry 10 \
                    --retry-delay 3 \
                    http://${DEPLOY_HOST}:${APP_PORT}/health

                    echo "Application deployed successfully"
                '''
            }
        }
    }

    post {

        success {
            echo 'CI/CD pipeline completed successfully'
        }

        failure {
            echo 'CI/CD pipeline failed. Check console output'
        }

        always {
            echo 'Pipeline execution finished'
        }
    }
}
