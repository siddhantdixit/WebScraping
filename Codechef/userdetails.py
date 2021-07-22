from bs4 import BeautifulSoup
import requests

user_profile = input("Enter user profile URL: ")
r = requests.get(user_profile)
content = r.content
soup = BeautifulSoup(content, "html.parser")

stars = None
username = None
country = None
state = None
city = None
profession = None
institute = None
teamList = None
teamInvites = None

userSpan = soup.find("label", string="Username:").nextSibling.findChildren()
stars = userSpan[0].text
username = userSpan[1].text

country = soup.find("label", string="Country:").nextSibling.text.strip()
# print(country)

state = soup.find("label", string="State:").nextSibling.text

city = soup.find("label", string="City:").nextSibling.text

institute = soup.find("label", string="Institution:").nextSibling.text

profession = soup.find(
    "label", string="Student/Professional:").nextSibling.text


print(stars,
      username,
      country,
      state,
      city,
      profession,
      institute,
      teamList,
      teamInvites, sep="\n")
print(soup.find("label", string="Teams List:").nextSibling)
