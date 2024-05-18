pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        SCANNER_HOME= tool 'sonar-scanner'
        DOCKERHUB_USERNAME = 'idrisniyi94'
        FR_DEPLOYMENT_NAME = 'fr-gassikialaw'
        EN_DEPLOYMENT_NAME = 'en-gassikialaw'
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        FR_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${FR_DEPLOYMENT_NAME}:${IMAGE_TAG}"
        EN_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${FEN_DEPLOYMENT_NAME}:${IMAGE_TAG}"
        NAMESPACE = 'gassikialaw'
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
        SMTP_SERVER_PASS = credentials('1be23fe9-d2cf-48d5-a5b8-c1b1f9ea6bca')
        PORT = '465'
        SMTP_SERVER = 'smtp.sendgrid.net'
        EMAIL = 'apikey'
    }

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/NIA_NAMECHEAP.git'
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=gassikalaw -Dsonar.projectName=gassikalaw"
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
                    }
                }
            }
        }
        // stage('Pytest') {
        //     steps {
        //         script {
        //             sh "pip install -r requirements.txt --no-cache-dir"
        //             sh "python3 -m pytest --cov=app --cov-report=xml --cov-report=html"
        //         }
        //     }
        // }
        stage('OWASP') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey 4bdf4acc-8eae-45c1-bfc4-844d549be812', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                script {
                    sh "trivy fs ."
                }
            }
        }
        stage("Login to DockerHub") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Successful"
            }
        }
        stage("Docker Build") {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME --build-arg EMAIL=$EMAIL --build-arg SMTP_SERVER=$SMTP_SERVER --build-arg PORT=$PORT --build-arg SMTP_SERVER_PASS=$SMTP_SERVER_PASS ."
                    echo "Image built successful"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    dir('./k8s') {
                        kubeconfig(credentialsId: '500a0599-809f-4de0-a060-0fdbb6583332', serverUrl: '') {
                            sh "sed -i 's|IMAGE_NAME|${env.IMAGE_NAME}|g' deployment.yaml"
                            sh "kubectl apply -f deployment.yaml"
                            sh "kubectl apply -f service.yaml"
                            slackSend channel: '#alerts', color: 'good', message: "Deployment to Kubernetes was successful and currently running on https://nigeriaislamicassociation.org/"
                        }
                        def rolloutStatus = sh(script: 'kubectl rollout status deploy $DEPLOYMENT_NAME -n $NAMESPACE', returnStatus: true)
                        if (rolloutStatus != 0) {
                            slackSend channel: '#alerts', color: 'danger', message: "Deployment to Kubernetes failed"
                            }
                    }
                }
            }
        }
    }
    post {
        success {
           
            slackSend channel: '#alerts', color: 'good', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
        failure {

            slackSend channel: '#alerts', color: 'danger', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
    }
}