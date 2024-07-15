import subprocess
from rich.console import Console

console = Console()

def get_docker_container(container_name):
    try:
        result = subprocess.run(["docker", "ps", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        return None

def execute_crictl_command(container_id, crictl_command):
    try:
        result = subprocess.run(["docker", "exec", container_id] + crictl_command.split(), capture_output=True, text=True)
        console.print(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        return e.returncode

def load_docker_image_to_kind(cluster_name, image):
    try:
        result = subprocess.run(["kind", "load", "docker-image", image, "--name", cluster_name], capture_output=True, text=True)
        console.print(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        return e.returncode