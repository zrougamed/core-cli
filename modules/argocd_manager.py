from rich.console import Console
import subprocess
import json

console = Console()

def template_service(service_name, project_name, repo_url, path):
    template = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "ApplicationSet",
        "metadata": {
            "name": service_name,
            "namespace": "argocd"
        },
        "spec": {
            "generators": [
                {
                    "git": {
                        "repoURL": repo_url,
                        "directories": [
                            {
                                "path": path
                            }
                        ]
                    }
                }
            ],
            "template": {
                "metadata": {
                    "name": service_name
                },
                "spec": {
                    "project": project_name,
                    "source": {
                        "repoURL": repo_url,
                        "path": path,
                        "targetRevision": "HEAD"
                    },
                    "destination": {
                        "server": "https://kubernetes.default.svc",
                        "namespace": "default"
                    }
                }
            }
        }
    }

    with open(f"{service_name}-appset.yaml", 'w') as f:
        json.dump(template, f, indent=2)
    
    console.print(f"[green]ApplicationSet template for {service_name} created successfully!")

def load_application_from_local(app_name, file_path):
    try:
        result = subprocess.run(["argocd", "app", "create", "-f", file_path], capture_output=True, text=True)
        console.print(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        return e.returncode

def list_and_select_applications():
    try:
        result = subprocess.run(["argocd", "app", "list", "-o", "json"], capture_output=True, text=True)
        apps = json.loads(result.stdout)
        app_names = [app['metadata']['name'] for app in apps]

        console.print("Available Applications:")
        for i, app in enumerate(app_names, 1):
            console.print(f"{i}. {app}")

        selected_indexes = console.input("Enter the numbers of the applications to sync (comma-separated): ")
        selected_apps = [app_names[int(index) - 1] for index in selected_indexes.split(",")]

        for app in selected_apps:
            subprocess.run(["argocd", "app", "sync", app], capture_output=True, text=True)
            console.print(f"[green]Application {app} synced successfully!")

        return 0
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        return e.returncode