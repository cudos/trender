import json
import os
import shutil

import click
import jinja2


@click.command()
@click.option(
    '--services',
    help='path to json file containing a list of services',
)
@click.option(
    '--template',
    help='the template that is to render for each service; can be passed multiple times',
    multiple=True,
)
@click.option(
    '--output-dir',
    help='the directory to store rendered templates',
)
def main(services, template, output_dir):
    services = json.load(open(services))
    # Drop eventually existing output directory - just recreate it
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    for service in services:
        click.echo('render templates for service %s' % service)
        for templ in template:
            path, filename = os.path.split(templ)
            rendered_template = jinja2.Environment(
                loader=jinja2.FileSystemLoader(path or './')
            ).get_template(filename).render(service)
            service_output_dir = os.path.join(output_dir, service['id'])
            if not os.path.exists(service_output_dir):
                os.makedirs(service_output_dir)
            output_filepath = os.path.join(service_output_dir, filename)
            click.echo(' * render %s, output goes to %s' % (templ, output_filepath))
            with open(output_filepath, 'w') as fd:
                fd.write(rendered_template)
        click.echo()
