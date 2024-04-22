from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import os
from utils import context
from utils import vh_config
from utils import logger

directory = context.get_context(os.path.abspath(__file__))
logger = logger.setup_logger("test_logger", f"{directory}/logs/main.log")
config = vh_config.grab(logger)

SHAREPOINT_EMAIL = config["Office365"]["sharepoint-email"]
SHAREPOINT_PWD = config["Office365"]["sharepoint-pwd"]
SHAREPOINT_DOCS_SITE = config["Office365"]["sharepoint-documents-site"]
SHAREPOINT_DOCS_SITE_NAME = config["Office365"]["sharepoint-documents-site-name"]
SHAREPOINT_HEALTH_DOC_LIB = config["Office365"]["sharepoint-health-doc-library"]
SHAREPOINT_HIT_SITE_NAME = config["Office365"]["sharepoint-hit-site-name"]

class SharePoint:
    """
    A class for interacting with SharePoint documents.

    Attributes:
    - SHAREPOINT_DOCS_SITE (str): The URL of the SharePoint documents site.
    - SHAREPOINT_HEALTH_DOC_LIB (str): The name of the SharePoint Health documents library.
    """

    def _auth(self):
        """
        Authenticate with SharePoint using user credentials.

        Returns:
        - ClientContext: The authenticated client context for SharePoint.
        """
        return ClientContext(SHAREPOINT_DOCS_SITE) \
            .with_credentials(UserCredential(SHAREPOINT_EMAIL, SHAREPOINT_PWD))

    def _get_files_list(self, folder_name):
        """
        Get a list of files in a SharePoint folder.

        Args:
        - folder_name (str): The name of the folder in SharePoint.

        Returns:
        - list: A list of File objects representing the files in the folder.
        """
        conn = self._auth()
        target_folder_url = f"{SHAREPOINT_HEALTH_DOC_LIB}/{folder_name}"
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files

    def download_file(self, file_name, folder_name):
        """
        Download a file from a SharePoint folder.

        Args:
        - file_name (str): The name of the file to download.
        - folder_name (str): The name of the folder in SharePoint.

        Returns:
        - bytes: The content of the downloaded file.
        """
        conn = self._auth()
        file_url = f"/sites/{SHAREPOINT_DOCS_SITE_NAME}/{SHAREPOINT_HEALTH_DOC_LIB}/{folder_name}/{file_name}"
        logger.info(f"Downloading files from {file_url}")
        return File.open_binary(context=conn, server_relative_url=file_url).content

    def upload_file(self, file_name, folder_name, content):
        """
        Upload a file to a SharePoint folder.

        Args:
        - file_name (str): The name of the file to upload.
        - folder_name (str): The name of the folder in SharePoint to upload to.
        - content (bytes): The content of the file to upload.
        """
        conn = self._auth()
        target_folder_url = (f"/sites/{SHAREPOINT_DOCS_SITE_NAME}/"
                             f"{SHAREPOINT_HEALTH_DOC_LIB}/{SHAREPOINT_HIT_SITE_NAME}"
                             f"/{folder_name}")
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.upload_file(file_name, content).execute_query()
        logger.info(f"{file_name} has been uploaded to: {response.serverRelativeUrl}")
