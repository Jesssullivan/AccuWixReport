import os
import pandas as pd
from pandas import read_csv, concat

ACUITY_REPORT_PATH = './data/AcuityExport.csv'
WIX_REPORT_PATH = './data/WixExport.csv'

# modify paths to absolute paths:
ACUITY_REPORT_PATH, WIX_REPORT_PATH = map(lambda x: os.path.abspath(x), [ACUITY_REPORT_PATH, WIX_REPORT_PATH])

# Create a list of month qualifiers, we do not need the datetime library;
# Wix exports with just these three letter dates
# Acuity exports with fully spelled out dates
MONTH_LIST = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# load CSVs:
ACUITY_REPORT = read_csv(ACUITY_REPORT_PATH)
WIX_REPORT = read_csv(WIX_REPORT_PATH)

# create wix subset:
WIX_SUBSET = WIX_REPORT[["Billing name", "Contact email", "Date", "Item", "Total after refund", "Fulfillment status"]]
ACUITY_SUBSET = ACUITY_REPORT[["First Name", "Last Name", "Email", "Type", "End Time", "Appointment Price", "Paid?"]]

return_shape = {"data": pd.DataFrame,
                "report": dict
                }


# for both paid and unpaid reports, want to return two sets of info:
# ...a merged dataframe of paid transactions for this particular date with the following columns:
# | Client | Date | Service | Gross |
# ^ unpaid report also includes an | Email | column
# ...a dictionary of superlatives:
# | Income | Total Appointments | Unique Clients | ... total appointments of type |
def create_unpaid_report(date="Jul") -> return_shape:
    # if we didn't get a valid three letter date code from `date`, let the user know and
    # perhaps print the help string

    if date not in MONTH_LIST:
        return "not a valid date"

    # initialize unpaid df; this is where we'll store and unify the exports from Wix and Acuity
    wix_unpaid_df = pd.DataFrame()
    acuity_unpaid_df = pd.DataFrame()

    # initialize report df, this contains only the superlative values.
    # we'll append total counts of each unique appointment type as well programmatically
    report_dict = {
        "Income": 0,
        "Total Appointments": 0,
        "Unique Clients": 0,
        "Unique Types": list()
    }

    # filter for this particular date:

    # Acuity:
    ACUITY_SUBSET_DATE = ACUITY_SUBSET[ACUITY_SUBSET["End Time"].str.contains(date, na=True)]
    ACUITY_SUBSET_DATE_UNPAID = ACUITY_SUBSET_DATE[ACUITY_SUBSET_DATE["Paid?"] != "yes"]

    # Wix:
    WIX_SUBSET_DATE = WIX_SUBSET[WIX_SUBSET["Date"].str.contains(date, na=True)]
    WIX_SUBSET_DATE_UNPAID = WIX_SUBSET_DATE[WIX_SUBSET_DATE["Fulfillment status"] != "Fulfilled"]

    # add email:
    acuity_unpaid_df["Email"] = ACUITY_SUBSET_DATE_UNPAID["Email"]
    wix_unpaid_df["Email"] = WIX_SUBSET_DATE_UNPAID["Contact email"]

    # add clients:
    acuity_unpaid_df["Client"] = ACUITY_SUBSET_DATE_UNPAID["First Name"] + " " + ACUITY_SUBSET_DATE_UNPAID["Last Name"]
    wix_unpaid_df["Client"] = WIX_SUBSET_DATE_UNPAID["Billing name"]

    # add dates:
    acuity_unpaid_df["Date"] = ACUITY_SUBSET_DATE_UNPAID["End Time"]
    wix_unpaid_df["Date"] = WIX_SUBSET_DATE_UNPAID["Date"]

    # add services:
    acuity_unpaid_df["Service"] = ACUITY_SUBSET_DATE_UNPAID["Type"]
    wix_unpaid_df["Service"] = WIX_SUBSET_DATE_UNPAID["Item"]

    # add gross:
    acuity_unpaid_df["Gross"] = ACUITY_SUBSET_DATE_UNPAID["Appointment Price"]
    wix_unpaid_df["Gross"] = WIX_SUBSET_DATE_UNPAID["Total after refund"]

    # merge our dataframe so we can return this and create a superlative dictionary:
    report_df = concat([acuity_unpaid_df, wix_unpaid_df])

    # obtain our superlative values:
    report_dict["Income"] = report_df["Gross"].sum()
    report_dict["Total Appointments"] = len(report_df)
    report_dict["Unique Clients"] = len(report_df["Client"].unique())

    # get counts of each unique appointment type:
    for appt_type in report_df["Service"].unique():
        report_dict["Unique Types"].append({
            appt_type: len(report_df[report_df["Service"] == appt_type])
        })

    return {"data": report_df,
            "report": report_dict
            }


def create_paid_report(date="Jul") -> return_shape:
    # we want to return two sets of info:
    # ...a merged dataframe of paid transactions for this particular date with the following columns:
    # | Client | Date | Service | Gross |
    # ...a dictionary of superlatives:
    # | Income | Total Appointments | Unique Clients | ... total appointments of type |

    # if we didn't get a valid three letter date code from `date`, let the user know and
    # perhaps print the help string
    if date not in MONTH_LIST:
        return "not a valid date"

    # initialize paid df; this is where we'll store and unify the exports from Wix and Acuity
    wix_paid_df = pd.DataFrame()
    acuity_paid_df = pd.DataFrame()

    # initialize report df, this contains only the superlative values.
    # we'll append total counts of each unique appointment type as well programmatically
    report_dict = {
        "Income": 0,
        "Total Appointments": 0,
        "Unique Clients": 0,
        "Unique Types": list()
    }

    # filter for this particular date:
    # Acuity:
    ACUITY_SUBSET_DATE = ACUITY_SUBSET[ACUITY_SUBSET["End Time"].str.contains(date, na=True)]
    ACUITY_SUBSET_DATE_ZERO = ACUITY_SUBSET_DATE[ACUITY_SUBSET_DATE["Appointment Price"].astype('float') > .1]
    ACUITY_SUBSET_DATE_PAID = ACUITY_SUBSET_DATE_ZERO[ACUITY_SUBSET_DATE_ZERO["Paid?"] == "yes"]

    # Wix:
    WIX_SUBSET_DATE = WIX_SUBSET[WIX_SUBSET["Date"].str.contains(date, na=True)]
    WIX_SUBSET_DATE_ZERO = WIX_SUBSET_DATE[WIX_SUBSET_DATE["Total after refund"].astype('float') > .1]
    WIX_SUBSET_DATE_PAID = WIX_SUBSET_DATE_ZERO[WIX_SUBSET_DATE_ZERO["Fulfillment status"] == "Fulfilled"]

    # add clients:
    acuity_paid_df["Client"] = ACUITY_SUBSET_DATE_PAID["First Name"] + " " + ACUITY_SUBSET_DATE_PAID["Last Name"]
    wix_paid_df["Client"] = WIX_SUBSET_DATE_PAID["Billing name"]

    # add dates:
    acuity_paid_df["Date"] = ACUITY_SUBSET_DATE_PAID["End Time"]
    wix_paid_df["Date"] = WIX_SUBSET_DATE_PAID["Date"]

    # add services:
    acuity_paid_df["Service"] = ACUITY_SUBSET_DATE_PAID["Type"]
    wix_paid_df["Service"] = WIX_SUBSET_DATE_PAID["Item"]

    # add gross:
    acuity_paid_df["Gross"] = ACUITY_SUBSET_DATE_PAID["Appointment Price"]
    wix_paid_df["Gross"] = WIX_SUBSET_DATE_PAID["Total after refund"]

    # merge our dataframe so we can return this and create a superlative dictionary:
    report_df = concat([acuity_paid_df, wix_paid_df])

    # obtain our superlative values:
    report_dict["Income"] = report_df["Gross"].sum()
    report_dict["Total Appointments"] = len(report_df)
    report_dict["Unique Clients"] = len(report_df["Client"].unique())

    # get counts of each unique appointment type:
    for appt_type in report_df["Service"].unique():
        report_dict["Unique Types"].append({
            appt_type: len(report_df[report_df["Service"] == appt_type])
        })

    return {"data": report_df,
            "report": report_dict
            }

