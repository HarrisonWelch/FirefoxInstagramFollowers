import json
import html_to_json

def main():
    followers_html_txt = open('Followers.html', encoding="utf8").read()
    following_html_txt = open('Following.html', encoding="utf8").read()

    followers_json = html_to_json.convert(followers_html_txt)
    following_json = html_to_json.convert(following_html_txt)

    # print(following_json['div'])

    followers_ats = []
    following_ats = []

    for li in followers_json['div']:
        for li2 in li['li']:
            # print('li2 = ' + str(li2))
            try:
                insta_at = li2['div'][0]['div'][0]['div'][1]['div'][0]['span'][0]['a'][0]['_value']
            except KeyError as ke:
                # print('KeyError found')
                insta_at = ''
            try:
                name = li2['div'][0]['div'][0]['div'][1]['div'][1]['_value']
            except KeyError as ke:
                # print('KeyError found')
                name = ''
            # x = x['div']

            followers_ats.append(insta_at)

            # print('follower insta_at = ' + str(insta_at) + ', name = ' + str(name))

    for li in following_json['div']:
        for li2 in li['li']:
            # print('li2 = ' + str(li2))
            try:
                insta_at = li2['div'][0]['div'][0]['div'][1]['div'][0]['span'][0]['a'][0]['_value']
            except KeyError as ke:
                # print('KeyError found')
                insta_at = ''
            try:
                name = li2['div'][0]['div'][0]['div'][1]['div'][1]['_value']
            except KeyError as ke:
                # print('KeyError found')
                name = ''
            # x = x['div']

            following_ats.append(insta_at)

            # print('following insta_at = ' + str(insta_at) + ', name = ' + str(name))

    # print('followers_ats = ' + str(followers_ats))
    # print('')
    # print('following_ats = ' + str(following_ats))

    print('Following but not a Follower')
    following_but_not_a_follower = list(set(following_ats) - set(followers_ats))
    for following_acct in sorted(following_but_not_a_follower):
        print(following_acct)
    print('')
    print('Follower but not Following')
    follower_but_not_a_following = list(set(followers_ats) - set(following_ats))
    for follower_acct in sorted(follower_but_not_a_following):
        print(follower_acct)

    # print(followers_json)

if __name__ == "__main__":
    main()