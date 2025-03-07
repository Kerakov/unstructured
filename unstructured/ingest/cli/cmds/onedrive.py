import logging

import click

from unstructured.ingest.cli.common import (
    add_recursive_option,
    add_shared_options,
    log_options,
    map_to_processor_config,
    map_to_standard_config,
    run_init_checks,
)
from unstructured.ingest.logger import ingest_log_streaming_init, logger
from unstructured.ingest.runner import onedrive as onedrive_fn


@click.command()
@click.option(
    "--authority-url",
    default="https://login.microsoftonline.com",
    help="Authentication token provider for Microsoft apps, default is "
    "https://login.microsoftonline.com",
)
@click.option(
    "--client-id",
    required=True,
    help="Microsoft app client ID",
)
@click.option(
    "--client-cred",
    required=True,
    help="Microsoft App client secret",
)
@click.option(
    "--onedrive-folder",
    default=None,
    help="Folder to start parsing files from.",
)
@click.option(
    "--tenant",
    default="common",
    help="ID or domain name associated with your Azure AD instance",
)
@click.option(
    "--user-pname",
    required=True,
    help="User principal name, usually is your Azure AD email.",
)
def onedrive(**options):
    verbose = options.get("verbose", False)
    ingest_log_streaming_init(logging.DEBUG if verbose else logging.INFO)
    log_options(options)
    try:
        run_init_checks(**options)
        connector_config = map_to_standard_config(options)
        processor_config = map_to_processor_config(options)
        onedrive_fn(connector_config=connector_config, processor_config=processor_config, **options)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise click.ClickException(str(e)) from e


def get_cmd() -> click.Command:
    cmd = onedrive
    add_recursive_option(cmd)
    add_shared_options(cmd)
    return cmd
