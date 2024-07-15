import argparse
import os
import configparser
from rich.console import Console

from modules.kind_manager import get_docker_container, execute_crictl_command, load_docker_image_to_kind
from modules.argocd_manager import template_service, load_application_from_local, list_and_select_applications
from modules.jenkins_manager import get_job_details, build_job, list_all_jobs
from modules.kubernetes_manager import list_pods, list_services, delete_pod, describe_pod

console = Console()

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config/config.ini')

# Get credentials from environment variables or config file
kind_container_name = os.getenv('KIND_CONTAINER_NAME', config['KIND']['ContainerName'])
argocd_url = os.getenv('ARGOCD_URL', config['ARGOCD']['Url'])
argocd_username = os.getenv('ARGOCD_USERNAME', config['ARGOCD']['Username'])
argocd_password = os.getenv('ARGOCD_PASSWORD', config['ARGOCD']['Password'])
jenkins_url = os.getenv('JENKINS_URL', config['JENKINS']['Url'])
jenkins_username = os.getenv('JENKINS_USERNAME', config['JENKINS']['Username'])
jenkins_password = os.getenv('JENKINS_PASSWORD', config['JENKINS']['Password'])

def main():
    parser = argparse.ArgumentParser(description="CLI for managing KIND, ArgoCD, Jenkins, and Kubernetes")
    subparsers = parser.add_subparsers(dest="command")

    # KIND subcommands
    kind_parser = subparsers.add_parser("kind", help="Manage KIND clusters")
    kind_subparsers = kind_parser.add_subparsers(dest="subcommand")

    kind_get_container = kind_subparsers.add_parser("get-container", help="Get Docker container running KIND cluster")
    kind_get_container.add_argument("container_name", type=str, help="Name of the KIND Docker container")

    kind_exec_crictl = kind_subparsers.add_parser("exec-crictl", help="Execute crictl command in KIND Docker container")
    kind_exec_crictl.add_argument("container_id", type=str, help="ID of the Docker container")
    kind_exec_crictl.add_argument("crictl_command", type=str, help="crictl command to execute")

    kind_load_image = kind_subparsers.add_parser("load-image", help="Load Docker image into KIND cluster")
    kind_load_image.add_argument("cluster_name", type=str, help="Name of the KIND cluster")
    kind_load_image.add_argument("image", type=str, help="Docker image to load")

    # ArgoCD subcommands
    argocd_parser = subparsers.add_parser("argocd", help="Manage ArgoCD applications")
    argocd_subparsers = argocd_parser.add_subparsers(dest="subcommand")

    argocd_template = argocd_subparsers.add_parser("template-service", help="Template a new service in ArgoCD")
    argocd_template.add_argument("service_name", type=str, help="Name of the service")

    argocd_load = argocd_subparsers.add_parser("load-application", help="Load application from local file")
    argocd_load.add_argument("app_name", type=str, help="Name of the application")
    argocd_load.add_argument("file_path", type=str, help="Path to the application file")

    argocd_list_sync = argocd_subparsers.add_parser("list-sync", help="List and select applications to sync")

    # Jenkins subcommands
    jenkins_parser = subparsers.add_parser("jenkins", help="Manage Jenkins jobs")
    jenkins_subparsers = jenkins_parser.add_subparsers(dest="subcommand")

    jenkins_get_job = jenkins_subparsers.add_parser("get-job", help="Get Jenkins job details")
    jenkins_get_job.add_argument("job_name", type=str, help="Name of the Jenkins job")

    jenkins_build_job = jenkins_subparsers.add_parser("build-job", help="Trigger a Jenkins job build")
    jenkins_build_job.add_argument("job_name", type=str, help="Name of the Jenkins job")

    jenkins_list_jobs = jenkins_subparsers.add_parser("list-jobs", help="List all Jenkins jobs")

    # Kubernetes subcommands
    kubernetes_parser = subparsers.add_parser("kubectl", help="Manage Kubernetes resources")
    kubernetes_subparsers = kubernetes_parser.add_subparsers(dest="subcommand")

    kubectl_list_pods = kubernetes_subparsers.add_parser("list-pods", help="List pods in a namespace")
    kubectl_list_pods.add_argument("--namespace", "-n", type=str, default="default", help="Namespace (default: 'default')")

    kubectl_list_services = kubernetes_subparsers.add_parser("list-services", help="List services in a namespace")
    kubectl_list_services.add_argument("--namespace", "-n", type=str, default="default", help="Namespace (default: 'default')")

    kubectl_delete_pod = kubernetes_subparsers.add_parser("delete-pod", help="Delete a pod in a namespace")
    kubectl_delete_pod.add_argument("pod_name", type=str, help="Name of the pod")
    kubectl_delete_pod.add_argument("--namespace", "-n", type=str, default="default", help="Namespace (default: 'default')")

    kubectl_describe_pod = kubernetes_subparsers.add_parser("describe-pod", help="Describe a pod in a namespace")
    kubectl_describe_pod.add_argument("pod_name", type=str, help="Name of the pod")
    kubectl_describe_pod.add_argument("--namespace", "-n", type=str, default="default", help="Namespace (default: 'default')")

    args = parser.parse_args()

    if args.command == "kind":
        if args.subcommand == "get-container":
            container_id = get_docker_container(args.container_name)
            console.print(f"Container ID: {container_id}")
        elif args.subcommand == "exec-crictl":
            execute_crictl_command(args.container_id, args.crictl_command)
        elif args.subcommand == "load-image":
            load_docker_image_to_kind(args.cluster_name, args.image)

    elif args.command == "argocd":
        if args.subcommand == "template-service":
            template_service(args.service_name, argocd_url, argocd_username, argocd_password)
        elif args.subcommand == "load-application":
            load_application_from_local(args.app_name, args.file_path)
        elif args.subcommand == "list-sync":
            list_and_select_applications()

    elif args.command == "jenkins":
        if args.subcommand == "get-job":
            get_job_details(jenkins_url, jenkins_username, jenkins_password, args.job_name)
        elif args.subcommand == "build-job":
            build_job(jenkins_url, jenkins_username, jenkins_password, args.job_name)
        elif args.subcommand == "list-jobs":
            list_all_jobs(jenkins_url, jenkins_username, jenkins_password)

    elif args.command == "kubectl":
        if args.subcommand == "list-pods":
            list_pods(args.namespace)
        elif args.subcommand == "list-services":
            list_services(args.namespace)
        elif args.subcommand == "delete-pod":
            delete_pod(args.pod_name, args.namespace)
        elif args.subcommand == "describe-pod":
            describe_pod(args.pod_name, args.namespace)

if __name__ == "__main__":
    main()
