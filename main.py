from FirefoxInstagramFollowers import *

def main():
    fif = FirefoxInstagramFollowers()
    fif.openBrowser()
    fif.loginToInstagram()
    fif.goToInstagramAccount()
    fif.getFollowingList()
    fif.getFollowerList()
    fif.parseAccounts()
    fif.close()
    fif.print()
    return

if __name__ == "__main__":
    main()
