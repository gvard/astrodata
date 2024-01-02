"""Functions for manipulating with supernovae and transients stats data."""

from urllib import request
from urllib.request import Request
from datetime import datetime
import locale

from bs4 import BeautifulSoup


SNE_BEFORE_1996 = 1065  # CBAT SNe 5504+1065=6569 с 1996 по 2016 + с 1006 до 1996
SNE_IAU_DCT = {
    1995: SNE_BEFORE_1996, 1996: 96, 1997: 163, 1998: 162, 1999: 206,
    2000: 184, 2001: 307, 2002: 334, 2003: 339, 2004: 251, 2005: 367,
    2006: 551, 2007: 573, 2008: 262, 2009: 390, 2010: 342, 2011: 298,
    2012: 247, 2013: 233, 2014: 139, 2015: 60,
}

locale.setlocale(locale.LC_ALL, "ru_RU")
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year


def get_soup_request(url, parser="lxml"):
    """Get url, return BeautifulSoup object."""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with request.urlopen(req) as html:
        return BeautifulSoup(html, parser)


def mk_sne_iau_lst(start_year=1996, end_year=2024):
    """Create list with sum of numbers before start_year as first item and
    other numbers for years before end_year."""
    sne_iau_lst = []
    _sum = 0
    for year, num in SNE_IAU_DCT.items():
        if year < start_year - 1:
            _sum += num
        elif year == start_year - 1:
            sne_iau_lst.append(_sum + num)
        else:
            sne_iau_lst.append(num)
    sne_iau_lst += (end_year - list(SNE_IAU_DCT)[-1]) * [0]
    return sne_iau_lst


def get_tns_stats():
    """Get info from Transient Name Server stats page."""
    soup = get_soup_request("https://www.wis-tns.org/stats-maps")
    # all_stat_num = soup.findAll('div', {"class": "stat-item-right"})
    # def _get_stat_num(i):
    #     return int(all_stat_num[i].text)
    # all_transient = _get_stat_num(0)
    # public_transient = _get_stat_num(1)
    # classified = _get_stat_num(2)
    # spectra = _get_stat_num(3)
    stat_cat_pub = soup.find("div", {"class": "stat-cat-public"})
    stat_cat_pub = stat_cat_pub.findAll("div", {"class": "stat-row"})
    stat_cat_all = soup.find("div", {"class": "stat-cat-all"})
    stat_cat_all = stat_cat_all.findAll("div", {"class": "stat-row"})
    return stat_cat_pub, stat_cat_all


def _yrnum(elm):
    """Get data from div elements of Transient Name Server stats page."""
    year = int(elm.find("div", {"class": "stat-row-left"}).text)
    num = int(elm.find("div", {"class": "stat-row-right"}).text)
    return year, num


def get_tns_year_stats(year_stats, endyear=2024):
    """Get Transient Name Server year stats: numbers of transients discovered
    for each year.
    """
    allnumsa = 0
    yrs_after_1996 = []
    yr_ints = []
    nums = []
    realdates = []
    stats_dct = {}
    sne_final_dct = {}
    _sum = 0
    for elm in year_stats:
        year, num = _yrnum(elm)
        yr_ints.append(year)
        stats_dct[year] = num
        nums.append(num)
        if year == endyear:
            realdate = today
        else:
            realdate = datetime(year + 1, 1, 1)
        realdates.append(realdate)
        if year in range(1976, 1996):
            _sum += num
        else:
            sne_final_dct[realdate] = num
            yrs_after_1996.append(year)
            allnumsa += num
    sne_final_dct[datetime(1996, 1, 1)] = _sum
    return nums, yr_ints, realdates, stats_dct, sne_final_dct


def add_iau_sne(sne_final_dct):
    """Sum SNe numbers in CBAT list and transients from TNS server."""
    for year, dat in SNE_IAU_DCT.items():
        if datetime(year + 1, 1, 1) in sne_final_dct:
            sne_final_dct[datetime(year + 1, 1, 1)] = (
                sne_final_dct[datetime(year + 1, 1, 1)] + dat
            )
        else:
            sne_final_dct[datetime(year + 1, 1, 1)] = dat
    return sne_final_dct


def mk_transient_total_numbers(total_dct):
    """Make list of transient total numbers."""
    total_lst = []
    _sum = 0
    for num in total_dct.values():
        if _sum == 0:
            _sum = num
        else:
            _sum += num
        total_lst.append(_sum)
    return total_lst


def _get_nums_before(stats_dct, start_year=1996):
    """Compute sum of all numbers before given year."""
    summ = 0
    for year, num in stats_dct.items():
        if year < start_year:
            summ += num
    return summ


def mk_tns_data(stats_pub_dct, stats_all_dct, start_year=1996, end_year=2024):
    """Make final data sets of TNS year stats for plotting."""
    nums_diff_dct = {}
    data_to_plot = {}
    _sum = _get_nums_before(stats_pub_dct, start_year=start_year)
    data_to_plot[start_year - 1] = _sum
    nums_diff_dct[start_year - 1] = 0
    for year in range(start_year, end_year + 1):
        if year in stats_pub_dct:
            data_to_plot[year] = stats_pub_dct[year]
            nums_diff_dct[year] = stats_all_dct[year] - stats_pub_dct[year]
        else:
            data_to_plot[year] = 0
            nums_diff_dct[year] = 0
    return data_to_plot, nums_diff_dct


def mk_urls_lst():
    """Make URLs list of Latest Supernovae Archives year stats pages."""
    snyears_urls = []

    def _yrurlstr(pre, pos):
        return f"https://rochesterastronomy.org/{pre}snstats{pos}.html"

    snyears_urls.append((1995, _yrurlstr("snimages/", "other")))
    for year in range(1996, 1999):
        snyears_urls.append((year, _yrurlstr("snimages/", year)))
    snyears_urls.append((1999, _yrurlstr("snimages/sn1999/", "")))
    for year in range(2000, YEAR + 1):
        snyears_urls.append((year, _yrurlstr(f"sn{year}/", "")))
    snyears_urls.append(("all", _yrurlstr("snimages/", "all")))
    return snyears_urls


def get_sn_stats(soup, end=23):
    """Get data from pre element and last modified date of
    Latest Supernovae Archives year stats page."""
    lastmod_txt = soup.findAll("p")[1].text.splitlines()[-1][23:]
    # dt = datetime.strptime(lastmod_txt[:10], '%Y/%m/%d')
    pre = soup.find("pre").text
    return pre.splitlines()[1:end], lastmod_txt[:-5]


def get_sn_count(txt):
    """Get supernova total count from Latest Supernovae Archives stats pages.
    TODO get number of SNe in galaxies and other statistics.
    """
    return (
        int(txt[0].split()[4]),
        int(txt[1].split()[0]),
        int(txt[5].split()[0]),
        int(txt[6].split()[0]),
    )
