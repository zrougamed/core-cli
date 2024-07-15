from kubernetes import client, config
from kubernetes.client.rest import ApiException
from rich.console import Console

console = Console()

def list_pods(namespace="default"):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)
        console.print(f"[bold cyan]Pods in namespace '{namespace}':")
        for pod in pods.items:
            console.print(f"[green]Name:[/green] {pod.metadata.name} [green]Status:[/green] {pod.status.phase}")
    except ApiException as e:
        console.print(f"[red]Exception when calling CoreV1Api->list_namespaced_pod: {e}")

def list_services(namespace="default"):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        services = v1.list_namespaced_service(namespace=namespace)
        console.print(f"[bold cyan]Services in namespace '{namespace}':")
        for svc in services.items:
            console.print(f"[green]Name:[/green] {svc.metadata.name} [green]Type:[/green] {svc.spec.type} [green]Cluster-IP:[/green] {svc.spec.cluster_ip}")
    except ApiException as e:
        console.print(f"[red]Exception when calling CoreV1Api->list_namespaced_service: {e}")

def delete_pod(pod_name, namespace="default"):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        delete_options = client.V1DeleteOptions()
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace, body=delete_options)
        console.print(f"[green]Pod '{pod_name}' deleted successfully from namespace '{namespace}'")
    except ApiException as e:
        console.print(f"[red]Exception when deleting Pod: {e}")

def describe_pod(pod_name, namespace="default"):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        console.print(f"[bold cyan]Details of Pod '{pod_name}' in namespace '{namespace}':")
        console.print(f"[green]Name:[/green] {pod.metadata.name}")
        console.print(f"[green]Namespace:[/green] {pod.metadata.namespace}")
        console.print(f"[green]Status:[/green] {pod.status.phase}")
        console.print(f"[green]Pod IP:[/green] {pod.status.pod_ip}")
        console.print(f"[green]Node Name:[/green] {pod.spec.node_name}")
    except ApiException as e:
        console.print(f"[red]Exception when calling CoreV1Api->read_namespaced_pod: {e}")
