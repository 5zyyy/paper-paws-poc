import yaml
import streamlit as st
import time

class SettingsConfiguration:
    def __init__(self, path):
        """
        Initialize the SettingsConfiguration with a path to the YAML file.

        Parameters:
        - path (str): Path to the settings YAML file.
        """
        self.path = path
        with open(path, 'r') as file:
            self.settings_data = yaml.safe_load(file)

    def get_settings(self):
        """
        Retrieve the current settings from the YAML file.

        Returns:
        - dict: Dictionary of settings.
        """
        return self.settings_data
        
    def update_settings(self, key, value, rerun=True):
        """
        Update a specific setting in the YAML file.

        Parameters:
        - key (str): The key of the setting to update.
        - value: The new value for the setting.
        - rerun (bool): Whether to rerun the Streamlit app after updating.
        """
        path = self.path
        try:
            with open(path, 'r') as file:
                data = yaml.safe_load(file)

            data[key] = value

            with open(path, 'w') as file:
                yaml.dump(data, file)
            
            if rerun:
                st.rerun()

        except Exception as e:
            print(f"Error updating YAML: {e}")

@st.dialog("Are you sure you want to reset the database?")
def reset_db_confirmation():
    """
    Display a confirmation dialog to reset the database.
    """
    from .database_helper import delete_db, create_db
    st.write(f"⚠️ This will reset your trade history!")
    if st.button("Confirm"):
        delete_db()
        create_db()
        st.toast("Database has been reset!", icon='🔄')
        time.sleep(1)
        st.rerun()

@st.dialog("Are you sure you want to delete the database?")
def delete_db_confirmation():
    """
    Display a confirmation dialog to delete the database.
    """
    from .database_helper import delete_db
    st.write(f"❗ This will delete your trade history!")
    if st.button("Confirm"):
        delete_db()
        st.toast("Database deleted!", icon='🗑️')
        time.sleep(1)
        st.rerun()