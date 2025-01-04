import yaml
import streamlit as st
import time

class SettingsConfiguration:
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as file:
            self.settings_data = yaml.safe_load(file)

    def get_settings(self):
        return self.settings_data
        
    def update_settings(self, key, value):
        path = self.path
        try:
            with open(path, 'r') as file:
                data = yaml.safe_load(file)

            data[key] = value

            with open(path, 'w') as file:
                yaml.dump(data, file)

            st.rerun()

        except Exception as e:
            print(f"Error updating YAML: {e}")

@st.dialog("Are you sure you want to reset the database?")
def reset_db_confirmation():
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
    from .database_helper import delete_db
    st.write(f"❗ This will delete your trade history!")
    if st.button("Confirm"):
        delete_db()
        st.toast("Database deleted!", icon='🗑️')
        time.sleep(1)
        st.rerun()