import os
import requests


def scrape_linkeding_profile(linkedin_profile_url: str):
    """scrape information from Linkedin profiles,
    Manually scrape the information from the Linkedin profile
    """
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": os.environ["PROXYCURL_API_KEY"]}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    ##clean data
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("grouops"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
