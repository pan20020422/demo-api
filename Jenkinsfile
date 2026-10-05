pipeline {
  agent any
  environment {
    HARBOR = '192.168.118.100:30002'
    IMAGE = "${HARBOR}/library/demo-api"
    TAG = "v${BUILD_NUMBER}"
    GITOPS_REPO = 'https://github.com/pan20020422/gitops-config.git'
  }
  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Build Image') {
      steps { sh "docker build -t ${IMAGE}:${TAG} ." }
    }

    stage('Trivy Scan') {
      steps {
        sh "trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE}:${TAG}"
      }
    }

    stage('Push Harbor') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'harbor-creds',
                                          usernameVariable: 'HUSER',
                                          passwordVariable: 'HPASS')]) {
          sh """
            docker login ${HARBOR} -u ${HUSER} -p ${HPASS}
            docker push ${IMAGE}:${TAG}
          """
        }
      }
    }

    stage('Update GitOps Repo') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'git-creds',
                                          usernameVariable: 'GUSER',
                                          passwordVariable: 'GPASS')]) {
          sh """
            git clone https://${GUSER}:${GPASS}@github.com/pan20020422/gitops-config.git
            cd gitops-config
            sed -i "s#newTag: .*#newTag: ${TAG}#" apps/demo-api/overlays/dev/kustomization.yaml
            git config user.email "jenkins@ci.local"
            git config user.name "jenkins-ci"
            git commit -am "chore(dev): bump demo-api to ${TAG}"
            git push origin main
          """
        }
      }
    }
  }
  post { always { cleanWs() } }
}
