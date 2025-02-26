# Youtrack. Time in status statistics

A Jupyter Notebook that helps understand how long each YouTrack issue stays in each status. It calculates various metrics and statistics.

### Installation
1. Clone the repository.
2. Install the required packages using pip:
  ```bash
  pip install -r requirements.txt
  ```
3. Open the Jupyter Notebook:
  ```bash
  jupyter notebook
  ```

### Configuration
- Set the `YOUTRACK_URL`, `YOUTRACK_TOKEN` in .env file
- Other necessary variables are set in the notebook.

### Instructions
1. All variables set in UPPER_CASE can be and should be changed.
2. Run the sells from "Build DataFrame" section to load and process the data.
3. Once the DataFrame is built, explore the various sections for different metrics and visualizations. You can execute the remaining sections in any order, but ensure that all UPPER_CASE variables are filled.
4. You can call `get_issue_info()` for any issue to retrieve detailed information about it.

### Troubleshooting
- Ensure that the YouTrack API token has the necessary permissions.
- Check the format of the data being imported to match the expected schema.

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
