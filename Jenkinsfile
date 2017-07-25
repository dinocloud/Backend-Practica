node {

    parameters
    {
    string(name:'BackendRevision', defaultValue:'master', description: 'BackendRevision is the commit which docker will build the image.')
    string(name:'BackendBranch', description:'BackendBranch will be used for docker tagging')
    }

    stage('Checkout')
    {
        checkout([$class: 'GitSCM', branches: [[name: '*']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/dinocloud/DevOps-Practica']]])
        echo "current git revision ${params.BackendRevision}"
        echo "current branch revision ${params.BackendBranch}"
    }

    stage('Build image')
    /*In this stage, docker builds the image in the path stablished.*/
    {
        sh "/usr/bin/docker build -t backend-practica --build-arg BACKEND_REVISION=${params.BackendRevision} . "
        echo "current git revision ${params.BackendRevision}"
    }

    stage('Test image') {
         //app.inside {
        //    sh 'echo "Tests passed"'
        //}
    }

    stage('Push image')
    {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */

        withCredentials([usernamePassword(credentialsId: '48253a45-d82c-43c8-b39e-031c511bc475', passwordVariable: 'DOCKER_REGISTRY_PASS', usernameVariable: 'DOCKER_REGISTRY_USER')]) {
            sh "docker login --username=${DOCKER_REGISTRY_USER} --password=${DOCKER_REGISTRY_PASS}"
            sh 'docker tag backend-practica dinocloud/backend-practica:$(echo ${BackendBranch}   | sed -e "s|origin/||g")'
            sh 'docker push dinocloud/backend-practica:$(echo ${BackendBranch}   | sed -e "s|origin/||g")'
        }

    }


}

