import os
import paramiko

from logging import getLogger
from bot.configuration import bot_configuration as bot_config
from pathlib import PurePath
from jinja2 import Environment, FileSystemLoader

logger = getLogger(__name__)


async def form_html(results: dict, file_path: str, report_url: str) -> PurePath:
    html_report_file = PurePath(bot_config.project_root, bot_config.reports_temp_folder, file_path)
    logger.debug(f'HTML report will be saved to file: {html_report_file}')
    file_loader = FileSystemLoader(PurePath(bot_config.project_root, bot_config.reports_template_dir))
    tmpl_env = Environment(loader=file_loader)
    template = tmpl_env.get_template(bot_config.reports_template_file)
    logger.debug(f'Template file: {template.filename}')
    rendered_html = template.render(results=results, report_url=report_url)
    with open(html_report_file, 'w') as f:
        f.write(rendered_html)
    return html_report_file


async def delete_temp_file(file_path: PurePath) -> None:
    # If file exists, delete it.
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.debug(f'File {file_path} removed')
    else:
        logger.debug(f'Error: {file_path} file not found')


async def upload_html_results(file_path: PurePath, filename: str) -> str:
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(hostname=bot_config.reports_host,
                username=bot_config.reports_user,
                password=bot_config.reports_user_pass)
    sftp = ssh.open_sftp()
    sftp.put(file_path, bot_config.reports_remote_folder + filename)
    sftp.close()
    ssh.close()
    return bot_config.reports_remote_url + filename
