```
  ___                          _       ______                      _
 / _ \                        (_)      | ___ \                    | |
/ /_\ \ ___ ___ _   ___      _____  __ | |_/ /___ _ __   ___  _ __| |_
|  _  |/ __/ __| | | \ \ /\ / / \ \/ / |    // _ \ '_ \ / _ \| '__| __|
| | | | (_| (__| |_| |\ V  V /| |>  <  | |\ \  __/ |_) | (_) | |  | |_
\_| |_/\___\___|\__,_| \_/\_/ |_/_/\_\ \_| \_\___| .__/ \___/|_|   \__|
                                                 | |
                                                 |_|

```

This command-line utility generates a variety of concise, merged monthly financial superlative reports in raw markdown, drawing from transaction CSVs exported by Acuity and Wix. 
- **"Paid" transaction reports** are marked as "paid" by the respective platforms (automatically via credit card or manually upon receiving otherwise untracked currency)
- **"Unpaid" transaction reports** were *not explicitly* marked as "paid"; while the most likely scenario is that this transaction was **completed successfully** offline (via cash / venmo), an "Unpaid" status may imply the client did not settle up or the transaction was recorded erroneously due to cancellation, revision or other extenuating circumstances.  

### Intended usage:

*Setup:*
```shell
python3.12 -m venv accuwix_venv
source accuwix_venv/bin/activate
pip install -r requirements.txt
```

*Generate and print report for January:*
```shell
 python3 src/cmdline.py -m Jan
```

*Generate and save all reports to markdown file:*
```shell
 python3 src/cmdline.py -all > AccuWixReport.md
```

*Generate a PDF report from markdown file:*
```shell
pandoc AccuWixReport.md -o output.pdf -V geometry:margin=1in
```

- - - 

*Display help screen:*
```shell
usage: 
 -h   : print this message again 
 -all : generate all reports 
 -m   : `month` (optional); specify a month to generate a superlative report`  

 use any of the following month qualifiers: 
 Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
```

