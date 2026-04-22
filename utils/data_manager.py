import streamlit as st
import fsspec
from utils.data_handler import DataHandler


class DataManager:
    def __init__(self, fs_protocol="webdav", fs_root_folder="app_data"):
        self.fs_protocol = fs_protocol
        self.fs_root_folder = fs_root_folder

        if fs_protocol not in st.secrets:
            raise ValueError(
                "WebDAV-Konfiguration fehlt. Bitte überprüfe die secrets.toml Datei."
            )

        fs_kwargs = dict(st.secrets[fs_protocol])

        self.filesystem = fsspec.filesystem(fs_protocol, **fs_kwargs)
        self.data_handler = DataHandler(self.filesystem, self.fs_root_folder)

    def _get_username(self):
        return st.session_state.get("username", "anonymous")

    def load_app_data(self, relative_path, initial_value=None, **load_args):
        return self.data_handler.load(
            relative_path,
            initial_value=initial_value,
            **load_args
        )

    def save_app_data(self, content, relative_path):
        self.data_handler.save(relative_path, content)

    def load_user_data(self, relative_path, initial_value=None, **load_args):
        user_path = f"users/{self._get_username()}/{relative_path}"
        return self.data_handler.load(
            user_path,
            initial_value=initial_value,
            **load_args
        )

    def save_user_data(self, content, relative_path):
        user_path = f"users/{self._get_username()}/{relative_path}"
        self.data_handler.save(user_path, content)