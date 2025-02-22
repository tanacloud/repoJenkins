pipeline {
    agent any

    environment {
        GIT_CREDENTIALS_ID = 'github-credentials'  
        SONARQUBE_SERVER = 'SonarQube'  // Nome do servidor configurado no Jenkins
        SONARQUBE_PROJECT_KEY = 'repoJenkins'  
        SONAR_TOKEN = credentials('sonar-token-id')  
    }

    stages {
        stage('Checkout do Código') {
            steps {
                script {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/tanacloud/repoJenkins.git',
                            credentialsId: env.GIT_CREDENTIALS_ID
                        ]]
                    ])
                }
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
                script {
                    def sonarCommand = """
                        sonar-scanner \\
                        -Dsonar.projectKey=${env.SONARQUBE_PROJECT_KEY} \\
                        -Dsonar.sources=. \\
                        -Dsonar.host.url=${env.SONARQUBE_SERVER} \\
                        -Dsonar.token=${env.SONAR_TOKEN}
                    """
                    sh sonarCommand
                }
            }
        }

        stage('Deploy para AWS CodeDeploy') {
            steps {
                script {
                    def commitId = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    def deployCommand = """
                        aws deploy create-deployment \\
                        --application-name MyFlaskApp \\
                        --deployment-group-name MyDeploymentGroup \\
                        --github-location repository=tanacloud/repoJenkins,commitId=${commitId}
                    """
                    sh deployCommand
                }
            }
        }
    }
}
