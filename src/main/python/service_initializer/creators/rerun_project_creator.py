from util.services import invoke_process


def create_project(self, app, definition, service, service_dir):
    args = ['rerun', 'otx:', 'create-otx-project', '--add-repo', 'True', '--project-description',
            definition['description'], '--project-type', definition['service-type'], '--application', app,
            '--role', service]
    invoke_process(args, service_dir, self.dry_run)
