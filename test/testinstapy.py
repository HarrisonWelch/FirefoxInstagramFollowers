from instapy import InstaPy

my_username = ""
my_password = ""

session = InstaPy(username=my_username, password=my_password)

session.login()

my_followers = session.grab_followers(username='heyitsdiaaa', amount="full", live_match=True, store_locally=True)

print('my = ' + str(my_followers))
