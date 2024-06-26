pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('1686a704-e66e-40f8-ac04-771a33b6256d')
        SCANNER_HOME= tool 'sonar-scanner'
        DOCKERHUB_USERNAME = 'idrisniyi94'
        FR_DEPLOYMENT_NAME = 'gassikialaw-fr'
        EN_DEPLOYMENT_NAME = 'gassikialaw-en'
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        FR_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${FR_DEPLOYMENT_NAME}:${IMAGE_TAG}"
        EN_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${EN_DEPLOYMENT_NAME}:${IMAGE_TAG}"
        NAMESPACE = 'gassikialaw'
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
        SMTP_SERVER_PASS = credentials('2c133af2-e9eb-4073-b032-00ddcd7366a4')
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
                checkout([$class: 'GitSCM', branches: [[name: '*/dev'], [name: '*/prod']], userRemoteConfigs: [[url: 'https://github.com/stwins60/gassikialaw.git']]])
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
        stage('Change Page URL for French') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        echo "Changing URL for dev branch"
                        sh "sed -i 's|https://gassikialaw.com|https://dev.gassikialaw.com|g' gassikialaw/templates/index.html"
                        sh "sed -i 's|https://gassikialaw.com|https://dev.gassikialaw.com|g' gassikialaw/templates/about.html"
                        sh "sed -i 's|https://gassikialaw.com|https://dev.gassikialaw.com|g' gassikialaw/templates/contact.html"
                        sh "sed -i 's|https://gassikialaw.com|https://dev.gassikialaw.com|g' gassikialaw/templates/service.html"

                        sh "sed -i 's|https://fr.gassikialaw.com|https://fr-dev.gassikialaw.com|g' gassikialaw/templates/index.html"
                        sh "sed -i 's|https://fr.gassikialaw.com|https://fr-dev.gassikialaw.com|g' gassikialaw/templates/about.html"
                        sh "sed -i 's|https://fr.gassikialaw.com|https://fr-dev.gassikialaw.com|g' gassikialaw/templates/contact.html"
                        sh "sed -i 's|https://fr.gassikialaw.com|https://fr-dev.gassikialaw.com|g' gassikialaw/templates/service.html"

                        sh "sed -i 's|https://gassikialaw.com/|https://dev.gassikialaw.com|g' fr_gassikialaw/templates/fr_index.html"
                        sh "sed -i 's|https://gassikialaw.com/|https://dev.gassikialaw.com|g' fr_gassikialaw/templates/fr_about.html"
                        sh "sed -i 's|https://gassikialaw.com/|https://dev.gassikialaw.com|g' fr_gassikialaw/templates/fr_contact.html"
                        sh "sed -i 's|https://gassikialaw.com/|https://dev.gassikialaw.com|g' fr_gassikialaw/templates/fr_service.html"
                    } 
                    // else if (env.BRANCH_NAME == 'prod') {
                    //     echo "Changing URL for prod branch"
                    //     sh "sed -i 's|https://dev.gassikialaw.com|https://gassikialaw.com|g' gassikialaw/index.html"
                    //     sh "sed -i 's|https://dev.gassikialaw.com|https://gassikialaw.com|g' gassikialaw/about.html"
                    //     sh "sed -i 's|https://dev.gassikialaw.com|https://gassikialaw.com|g' gassikialaw/contact.html"
                    //     sh "sed -i 's|https://dev.gassikialaw.com|https://gassikialaw.com|g' gassikialaw/service.html"

                    //     sh "sed -i 's|https://fr.dev.gassikialaw.com|https://fr.gassikialaw.com|g' gassikialaw/index.html"
                    //     sh "sed -i 's|https://fr.dev.gassikialaw.com|https://fr.gassikialaw.com|g' gassikialaw/about.html"
                    //     sh "sed -i 's|https://fr.dev.gassikialaw.com|https://fr.gassikialaw.com|g' gassikialaw/contact.html"
                    //     sh "sed -i 's|https://fr.dev.gassikialaw.com|https://fr.gassikialaw.com|g' gassikialaw/service.html"
                    // }
                    else {
                        echo "Branch name not found"
                    }
                }
            }
        }
        stage("Docker Build") {
            steps {
                script {
                  dir('./gassikialaw'){
                    sh "docker build -t $EN_IMAGE_NAME --build-arg EMAIL=$EMAIL --build-arg SMTP_SERVER=$SMTP_SERVER --build-arg PORT=$PORT --build-arg SMTP_SERVER_PASS=$SMTP_SERVER_PASS ."
                    echo "Image built successful"
                  }
                  dir('./fr_gassikialaw') {
                    sh "docker build -t $FR_IMAGE_NAME --build-arg EMAIL=$EMAIL --build-arg SMTP_SERVER=$SMTP_SERVER --build-arg PORT=$PORT --build-arg SMTP_SERVER_PASS=$SMTP_SERVER_PASS ."
                    echo "Image built successful"
                  }
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $EN_IMAGE_NAME"
                    sh "trivy image $FR_IMAGE_NAME"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $EN_IMAGE_NAME"
                    sh "docker push $FR_IMAGE_NAME"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    dir('./k8s') {
                        withKubeCredentials(kubectlCredentials: [[caCertificate: '', clusterName: '', contextName: '', credentialsId: 'fff8a37d-0976-4787-a985-a82f34d8db40', namespace: '', serverUrl: '']]) {
                            try {
                                if (env.BRANCH_NAME == 'dev') {
                                    echo "Deploying to dev"
                                    sh "sed -i 's|IMAGE_TAG|${env.IMAGE_TAG}|g' overlays/dev/kustomization.yaml"
                                    sh "kubectl apply -k overlays/dev"
                                    slackSend channel: '#alerts', color: 'good', message: "Deployment to Kubernetes was successful and currently running on https://dev.gassikialaw.com/ & https://fr.dev.gassikialaw.com/"
                                }
                                else if (env.BRANCH_NAME == 'prod') {
                                    echo "Deploying to prod"
                                    sh "sed -i 's|IMAGE_TAG|${env.IMAGE_TAG}|g' overlays/prod/kustomization.yaml"
                                    sh "kubectl apply -k overlays/prod"
                                    slackSend channel: '#alerts', color: 'good', message: "Deployment to Kubernetes was successful and currently running on https://gassikialaw.com/ & https://fr.gassikialaw.com/"
                                }
                                else {
                                    slackSend channel: '#alerts', color: 'danger', message: "Deployment failed. Branch name not found"
                                }
                                

                            } catch (Exception e) {
                                // Send failure message to Slack in case of any exception
                                slackSend channel: '#alerts', color: 'danger', message: "Deployment to Kubernetes failed with exception: ${e.message}"
                                // Rethrow the exception to fail the build
                                throw e
                            }
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