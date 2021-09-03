# smart-switcher
import as pycharm project, requirements.txt should do the rest

# Data/data.json
to read it you can use this command:
`awk '{gsub(/\\n/,"\n")}1' data.json | awk '{gsub(/\\/,"")}1'`
