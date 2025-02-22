pipeline {
    agent any

    environment {
        GIT_CREDENTIALS_ID = 'github-credentials'  // ID da credencial do GitHub no Jenkins
        SONARQUBE_SERVER = 'http://35.174.156.37:9000/'  // Altere para o IP do seu SonarQube
        SONARQUBE_PROJECT_KEY = 'repoJenkins'  // Nome do projeto no SonarQube
        SONAR_TOKEN = credentials('sonar-token-id')  // ID da credencial do SonarQube no Jenkins
    }

    stages {
        stage('Checkout do Código') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/tanacloud/repoJenkins.git',
                        credentialsId: env.GIT_CREDENTIALS_ID
                    ]]
                ])
            }
        }

        stage('Instalar Dependências') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Executar Testes') {
            steps {
                sh 'python -m unittest discover tests'
            }
        }

        stage('Análise com SonarQube') {
            steps {
                sh """
                    mvn sonar:sonar \
                        -Dsonar.projectKey=${SONARQUBE_PROJECT_KEY} \
                        -Dsonar.host.url=${SONARQUBE_SERVER} \
                        -Dsonar.login=${SONAR_TOKEN}
                """
            }
        }

        stage('Deploy para AWS CodeDeploy') {
            steps {
                sh """
                    aws deploy create-deployment \
                        --application-name MyFlaskApp \
                        --deployment-group-name MyDeploymentGroup \
                        --github-location repository=tanacloud/repoJenkins,commitId=$(git rev-parse HEAD)
                """
            }
        }
    }
}
