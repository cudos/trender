# test_trender.py
import os

import click
from click.testing import CliRunner

from trender import main


def test_main(tmpdir):
    '''This test is an integration test running the whole script with some sample options
    and checking if all output files were created properly.
    '''

    # Setup services.json.
    services_json = tmpdir.join('services.json')
    services_json.write('''[
        {
    	    "id": "service-1",
            "hostname": "host-1",
    	    "port": "8080"
        },
        {
            "id": "service-2",
            "hostname": "host-2",
            "port": "9090"
        }
    ]
''')

    # Setup template template_t1
    template_1 = tmpdir.join('template_1')
    template_1.write('''Template 1
{{ hostname }}
{{ port }}
''')

    # Setup another template template_2
    template_2 = tmpdir.join('template_2')
    template_2.write('''Template 2
{{ hostname }}
{{ port }}
''')

    # Setup output direcotry path
    output_dir = tmpdir.dirpath('output')
    
    # Setup Click test runner that is able to execute Click script
    runner = CliRunner()
    result = runner.invoke(
        main, [
            '--services', services_json.strpath,
            '--template', template_1.strpath,
            '--template', template_2.strpath,
            '--output-dir', output_dir.strpath,
        ]
    )

    assert result.exit_code == 0

    # Check script output
    path_to_template_1_of_service_1 = os.path.join(output_dir.strpath, 'service-1', template_1.basename)
    path_to_template_2_of_service_1 = os.path.join(output_dir.strpath, 'service-1', template_2.basename)
    path_to_template_1_of_service_2 = os.path.join(output_dir.strpath, 'service-2', template_1.basename)
    path_to_template_2_of_service_2 = os.path.join(output_dir.strpath, 'service-2', template_2.basename)
        
    os.path.join(output_dir.strpath, 'service-1', template_1.basename),
    assert result.output == '''render templates for service {u'hostname': u'host-1', u'id': u'service-1', u'port': u'8080'}
 * render %s, output goes to %s
 * render %s, output goes to %s

render templates for service {u'hostname': u'host-2', u'id': u'service-2', u'port': u'9090'}
 * render %s, output goes to %s
 * render %s, output goes to %s

''' % (
        template_1.strpath,
        path_to_template_1_of_service_1,
        template_2.strpath,
        path_to_template_2_of_service_1,
        template_1.strpath,
        path_to_template_1_of_service_2,
        template_2.strpath,
        path_to_template_2_of_service_2
    )

    # Check content of rendered template_1 for service-1
    assert open(path_to_template_1_of_service_1).read() == '''Template 1
host-1
8080'''

    # Check content of rendered template_2 of service-1
    assert open(path_to_template_2_of_service_1).read() == '''Template 2
host-1
8080'''

    # Check content of rendered template 1 of service-2
    assert open(path_to_template_1_of_service_2).read() == '''Template 1
host-2
9090'''

    # Check content of rendered template 2 of service-2
    assert open(path_to_template_2_of_service_2).read() == '''Template 2
host-2
9090'''
