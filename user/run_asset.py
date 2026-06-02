import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "asset_gui.py", "--server.port=8502"]
    sys.exit(stcli.main())
