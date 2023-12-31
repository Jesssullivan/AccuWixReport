from sys import argv
from datasets import create_unpaid_report, create_paid_report, MONTH_LIST


def help_str() -> str:
    with open('scripts/prefix') as f:
        print(f.read())
        f.close()

    return str('usage: \n' +
               ' -h   : print this message again \n' +
               ' -all : generate all reports \n' +
               ' -m   : `month` (optional); specify a month to generate a superlative report`  \n' +
               '\n use any of the following month qualifiers: \n ' +
               "Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec")


def argtype() -> bool:
    try:
        if len(argv) > 1:
            return True
        elif len(argv) == 1:
            use = False
            print(help_str())
        else:
            print('command takes 0 or 1 args, use -h for help')
            raise SystemExit
    except SystemExit:
        print('arg error... \n command takes 0 or 1 args, use -h for help')
        raise quit()
    return use


def exec_format_reports(date='') -> str:
    md_data_string = ""

    for paid in True, False:
        df = create_paid_report(date) if paid else create_unpaid_report(date)

        # process paid markdown output:
        paid_type = "Paid" if paid else "Unpaid / Unverified"

        if len(df["data"]) > 0:
            md_data_string += "\n\n## *Month of %s: %s Transactions:* \n" % (date, paid_type) + \
                              "| **Client** | **Date** | **Service** | **Gross** | \n" + \
                              "|:---------|----------|----------------------|-----:|"

            for i, t in df["data"].iterrows():
                md_data_string += ("\n|%s|%s|%s|%a|" %
                                   (t['Client'],
                                    t['Date'],
                                    t['Service'],
                                    t['Gross']))

            # create and populate superlative report and append that to md_data_table
            md_super_table = "\n\n## *Month of %s: %s Superlatives:* \n" % (date, paid_type) + \
                             "| **Income** | **Total Appointments** | **Unique Clients** | \n" + \
                             "|:--------|----------|--------:|"

            md_super_table += "\n|%a|%a|%a|" % \
                              (df['report']['Income'],
                               df['report']['Total Appointments'],
                               df['report']['Unique Clients'])

            # create table of appt. types:
            md_appt_table = "\n\n## *Month of %s: %s Appointment Types:* \n" % (date, paid_type) + \
                            "| **Appointment type** | **# Appointments** | \n" + \
                            "|:-----------------|--------:|"

            for t in df['report']['Unique Types']:
                md_appt_table += "\n|%s|%a|" % (*t.keys(), *t.values())

            md_data_string += md_super_table
            md_data_string += md_appt_table

    return md_data_string


def consume_arg():
    if argtype():
        if argv[1] == '-h':
            print('got help: argv[1]: %s' % argv[1].__str__())
            print(help_str())
            quit()

        if argv[1] == '-m':
            if argv[2] in MONTH_LIST:
                print(exec_format_reports(date=argv[2]))
                quit()

        if argv[1] == '-all':
            for month in MONTH_LIST:
                print(exec_format_reports(date=month))
            quit()

        else:
            if argv[1] in MONTH_LIST:
                print(exec_format_reports(date=argv[2]))
            else:
                print(help_str())
            quit()


if __name__ == "__main__":
    consume_arg()
