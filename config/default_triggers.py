"""
Default sales trigger queries for Patsnap Sales Intelligence Dashboard

These queries can be customized by the sales team to match specific
target markets, industries, or customer profiles.
"""

DEFAULT_TRIGGERS = {
    "Patent & IP": '(company OR startup OR firm OR corporation) AND (patent OR "intellectual property" OR "IP portfolio" OR trademark) AND (granted OR filed OR awarded OR secures)',
    #   "Funding": '(company OR startup) AND ("funding round" OR "Series A" OR "Series B" OR "raises" OR "secures funding" OR "venture capital")',
    #   "Acquisition": '(company OR firm) AND (acquisition OR merger OR "acquired by" OR "acquires" OR partnership)',
    #   "Leadership": '(company OR firm OR corporation) AND ("CEO" OR "CTO" OR "CFO") AND (appointment OR "appoints" OR hire OR "joins as" OR "named" OR "announces")',
    "Product Launch": '(company OR startup OR firm) AND ("product launch" OR "launches" OR "unveils" OR "announces" OR "introduces" OR "new product")',
    #  "Regulatory": '(company OR firm) AND ("regulatory approval" OR "FDA approval" OR "receives approval" OR licensed OR certified)',
    # "IPO": '(company OR startup) AND ("IPO" OR "going public" OR "files for IPO" OR "initial public offering" OR "stock listing")',
    "Expansion": '(company OR startup OR firm) AND (expansion OR "opens office" OR "opening" OR "expands into" OR "enters market" OR "new location")',
}
