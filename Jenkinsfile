def deployToKubernetes(buildNumber) {
  withCredentials([
    usernamePassword(credentialsId: 'elliot-ldap', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'),
    usernamePassword(credentialsId: 'hccer', usernameVariable: 'hccerUser', passwordVariable: 'hccerPass')
  ]) {
    sh "/home/hccer/kubelogin --username=${USERNAME} --password=${PASSWORD} --kubeconfig=/home/hccer/.kube/config"
    def config = readFile 'kubernetes.yml'
    sh "BUILD_NUMBER=${buildNumber} && ME_PASSWORD=${hccerPass} && cat <<EOF | kubectl apply -f -\n${config}\nEOF"
  }
}

node('docker') {
  stage ('Checkout SCM') {
    cleanWs()
    checkout scm
  }

  def mockImage

  stage ('Build mock-server') {
    mockImage = docker.build("qa-gov.cn.lab/mock-server:${env.BUILD_NUMBER}")
  }

  stage ('Upload image') {
    docker.withRegistry('https://qa-gov.cn.lab', 'frank') {
      mockImage.push()
    }
  }

  stage ('Deploy mock-server') {
    deployToKubernetes(env.BUILD_NUMBER)
  }
}