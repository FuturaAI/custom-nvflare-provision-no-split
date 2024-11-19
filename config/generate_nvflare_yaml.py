import yaml

def create_nvidia_flare_project_config(project_name: str):
    """
    Creates a YAML configuration file for NVIDIA FLARE project with specific formatting
    """
    class CustomDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

        def represent_list(self, data):
            # Special case for coeff_mod_bit_sizes
            if len(data) == 3 and all(isinstance(x, int) for x in data) and data == [60, 40, 40]:
                return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
            return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=False)

    # Configure the custom dumper
    CustomDumper.add_representer(list, CustomDumper.represent_list)

    config = {
        'api_version': 3,
        'name': project_name,
        'description': 'NVIDIA FLARE sample project',
        'participants': [
            {
                'name': 'server1',
                'type': 'server',
                'org': 'nvidia',
                'fed_learn_port': 8002,
                'admin_port': 8003
            },
            {
                'name': 'site-1',
                'type': 'client',
                'org': 'nvidia'
            },
            {
                'name': 'site-2',
                'type': 'client',
                'org': 'nvidia'
            },
            {
                'name': 'admin@nvidia.com',
                'type': 'admin',
                'org': 'nvidia',
                'role': 'project_admin'
            }
        ],
        'builders': [
            {
                'path': 'nvflare.lighter.impl.workspace.WorkspaceBuilder',
                'args': {
                    'template_file': 'master_template.yml'
                }
            },
            {
                'path': 'nvflare.lighter.impl.template.TemplateBuilder'
            },
            {
                'path': 'nvflare.lighter.impl.static_file.StaticFileBuilder',
                'args': {
                    'config_folder': 'config',
                    'overseer_agent': {
                        'path': 'nvflare.ha.dummy_overseer_agent.DummyOverseerAgent',
                        'overseer_exists': False,
                        'args': {
                            'sp_end_point': 'server1:8002:8003',
                            'heartbeat_interval': 6
                        }
                    }
                }
            },
            {
                'path': 'nvflare.lighter.impl.he.HEBuilder',
                'args': {
                    'poly_modulus_degree': 8192,
                    'coeff_mod_bit_sizes': [60, 40, 40],
                    'scale_bits': 40,
                    'scheme': 'CKKS'
                }
            },
            {
                'path': 'nvflare.lighter.impl.cert.CertBuilder'
            },
            {
                'path': 'nvflare.lighter.impl.signature.SignatureBuilder'
            }
        ]
    }

    # Write to YAML file with specific formatting
    with open(f'nvflare_project_config_{project_name}.yml', 'w') as file:
        yaml.dump(
            config, 
            file, 
            Dumper=CustomDumper,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=float("inf")  # Prevents line wrapping
        )

if __name__ == "__main__":
    create_nvidia_flare_project_config()