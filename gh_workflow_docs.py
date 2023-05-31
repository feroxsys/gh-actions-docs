import argparse
import glob
import os
from yaml import full_load

def parse_workflow_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        workflow = full_load(file)

    name = workflow.get('name', 'Unnamed workflow')
    jobs = workflow.get('jobs', {})

    inputs_table = []
    secrets_table = []

    on = workflow.get('on', {})
    if isinstance(on, dict):
        workflow_call = on.get('workflow_dispatch', None) or on.get('workflow_call', None)
        if workflow_call:
            inputs = workflow_call.get('inputs', {})
            secrets = workflow_call.get('secrets', {})

            if inputs:
                inputs_table.append('| Name | Description | Default | Required |')
                inputs_table.append('| ---- | ----------- | ------- | -------- |')
                for name, details in inputs.items():
                    inputs_table.append(f"| {name} | {details.get('description', '')} | {details.get('default', '')} | {details.get('required', '')} |")

            if secrets:
                secrets_table.append('| Name | Description | Required |')
                secrets_table.append('| ---- | ----------- | -------- |')
                for name, details in secrets.items():
                    secrets_table.append(f"| {name} | {details.get('description', '')} | {details.get('required', '')} |")

    jobs_table = ['| Name | Job ID | Runs On |', '| ---- | ------ | ------- |']
    for name, details in jobs.items():
        jobs_table.append(f"| {details.get('name', 'Unnamed job')} | {name} | {details.get('runs-on')} |")

    return {
        'name': name,
        'inputs': '\n'.join(inputs_table) if inputs_table else 'No inputs specified',
        'secrets': '\n'.join(secrets_table) if secrets_table else 'No secrets specified',
        'jobs': '\n'.join(jobs_table) if jobs_table else 'No jobs specified',
    }

def generate_docs_for_workflow_dir(workflow_dir, output_file):
    workflow_files = glob.glob(os.path.join(workflow_dir, '*.yml'))
    workflows = [parse_workflow_file(file) for file in workflow_files]

    with open(output_file, 'w', encoding='utf-8') as file:
        for workflow in workflows:
            file.write(f"# {workflow['name']}\n\n")
            file.write(f"Inputs:\n\n{workflow['inputs']}\n\n")
            file.write(f"Secrets:\n\n{workflow['secrets']}\n\n")
            file.write(f"Jobs:\n\n{workflow['jobs']}\n\n")
    print(f"Generated docs for {len(workflows)} workflows, output to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate markdown docs for GitHub Actions workflows.')
    parser.add_argument('--workflow_dir', required=True, help='Directory containing workflow files')
    parser.add_argument('--output_file', required=True, help='Output markdown file')
    args = parser.parse_args()

    generate_docs_for_workflow_dir(args.workflow_dir, args.output_file)
