from jenkinsapi.jenkins import Jenkins
from rich.console import Console

console = Console()

def get_server_instance(url, username, password):
    try:
        server = Jenkins(url, username=username, password=password)
        return server
    except Exception as e:
        console.print(f"[red]Error: {e}")
        return None

def get_job_details(url, username, password, job_name):
    server = get_server_instance(url, username, password)
    if server and job_name in server:
        job = server[job_name]
        console.print(f"Job Name: {job.name}")
        console.print(f"Job Description: {job.get_description()}")
        console.print(f"Job Last Build Number: {job.get_last_buildnumber()}")
        return job
    else:
        console.print(f"[red]Job {job_name} not found")
        return None

def build_job(url, username, password, job_name):
    server = get_server_instance(url, username, password)
    if server and job_name in server:
        job = server[job_name]
        job.invoke()
        console.print(f"[green]Job {job_name} invoked successfully!")
        return 0
    else:
        console.print(f"[red]Job {job_name} not found")
        return 1

def list_all_jobs(url, username, password):
    server = get_server_instance(url, username, password)
    if server:
        jobs = server.get_jobs_list()
        console.print("Available Jobs:")
        for job in jobs:
            console.print(f"- {job}")
        return jobs
    else:
        console.print(f"[red]Failed to connect to Jenkins server")
        return None
