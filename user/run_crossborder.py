import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "crossborder_gui.py", "--server.port=8503"]
    sys.exit(stcli.main())
