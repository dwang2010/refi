# grab daily rates from site
# send as title only e-mail to self

import argparse
import urllib.request
from bs4 import BeautifulSoup
from email_helper import EmailHelper
from email.message import EmailMessage

# ---------------------------------------------------------------
# parse page for desired data
# grabs daily mortgage rate (30 year fixed only)
# ---------------------------------------------------------------
def grab_mortgage_rate(soup):
    blob = soup.find("div", class_="rategrouplist").find("tbody").find("tr")
    rate_type = blob.find("td", class_="description").string
    rate_val  = blob.find("td", class_="current").string
    return "{0} ({1})".format(rate_val, rate_type)

# ---------------------------------------------------------------
# main script to grab rate data, e-mail to myself
# ---------------------------------------------------------------
def main(site, src_user, src_pwd, dest):
    # grab the page
    uf = urllib.request.urlopen(site)
    html = uf.read()

    # parse the page for desired data
    soup = BeautifulSoup(html, "html.parser")
    rate_info = grab_mortgage_rate(soup)
    print(rate_info)

    # create message to send (empty body)
    msg = EmailMessage()
    msg['Subject'] = rate_info
    msg['From']    = src_user
    msg['To']      = dest

    # send message in e-mail to self
    mail_butler = EmailHelper()
    mail_butler.login(src_user, src_pwd)
    mail_butler.send(src_user, dest, msg)
    mail_butler.close()

# -----------------------
# execution thread
# -----------------------
if __name__ == "__main__":
    print ("script start")

    # check for script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loc',
                        help='location of email login infos')
    parser.add_argument('-d', '--dest',
                        help='destination address of email msg')
    args = parser.parse_args()

    with open(args.loc, 'r') as file:
        login = file.read().splitlines()
    file.closed

    # target website
    # rates updated around 4pm EST
    link = "http://www.mortgagenewsdaily.com/mortgage_rates/daily.aspx"

    # run the script
    main(link, login[0], login[1], args.dest)
    print ("script done")
