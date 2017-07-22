import requests, urllib ,emoji
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '2321463265.7db0bd9.03832a1f138846128c522c7d8244c24f'


BASE_URL = 'https://api.instagram.com/v1/'

'''
Function declaration to get the ID of a user by username
'''

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    '''
    print 'GET request url : %s' % (request_url)
    '''
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    '''
    print 'GET request url : %s' % (request_url)
    '''
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

'''
Function declaration to fetch your own details
'''
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



'''
Function declaration to fetch the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User you trying to search does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            '''
            downloaded the most recent post
            '''
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'

            print 'Id of recent post: ' + own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            print 'Id of recent post: ' + user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function  to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id,)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

'''
Function to get a list of people who have liked the recent post of a user\n"

'''

def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    like_list = requests.get(request_url).json()
    if like_list['meta']['code'] == 200:
        if len(like_list['data']):
            print 'List of people who liked the recent post of user:'
            for i in range(len(like_list['data'])):

                print like_list['data'][i]['full_name']

        else:
            print 'There is no user present who liked your recent post!'
            exit()
    else :
        print 'error while fetching'


'''
Function declaration to make a comment on the recent post of the user
'''


def comment_on_post(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

'''
function to get list of comments on recent post of user
'''

def comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    get_list = requests.get(request_url).json()

    if get_list['meta']['code'] == 200:
        if len(get_list['data']):
            print 'List of people who commented on recent post of user:'
            for i in range(len(get_list['data'])):

                print '%d :' %(i+1) + get_list['data'][i]['text']

        else:
            print 'There is no user present who commented your post!'
            exit()
    else :
        print 'error'

'''
FUNTION TO SHOW A PIC WITH MIN LIKES OF USER
'''

'''
Function to Delete negative comments from the recent post of a user
'''
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_details = requests.get(request_url).json()

    if comment_details['meta']['code'] == 200:
        if len(comment_details['data']):
            '''
             Here's a naive implementation of how to delete the negative comments :)
            '''
            for i in range(0, len(comment_details['data'])):
                comment_id = comment_details['data'][i]['id']
                comment_text = comment_details['data'][i]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg >= blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment is successfully deleted!\n'
                    else:
                        print 'Unable to delete comment! Try again'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

'''
Funtion to delete a particular comment by searching a word  
'''
def delete_comment(insta_username):
    word =raw_input('Enter a word to be search and delete a comment')

    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_details = requests.get(request_url).json()

    if comment_details['meta']['code'] == 200:
        if len(comment_details['data']):
            '''
             Here's a naive implementation of how to delete the negative comments :)
            '''
            for i in range(0, len(comment_details['data'])):
                comment_id = comment_details['data'][i]['id']
                comment_text = comment_details['data'][i]['text']
                if(word in comment_text):

                    print ' Comment you requested : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment you requested is successfully deleted!\n'
                    else:
                        print 'Unable to delete comment! Please Try again'
                else:
                    print'Requested word not found in this comment: ' + comment_text
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

'''
Function to count number of post  and get post id of selected post of user
'''
def count_post(insta_username):

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User you trying to search does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'User have %s no. of posts: ' % (user_info['data']['counts']['media'])
            num=raw_input('choose the post number of which you want see a comment')
            num = int(num) -1
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    '''
    print 'GET request url : %s' % (request_url)
    '''
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][num]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()
'''
Function to shows all the comments of a selected post
'''

def get_post_comment(media_id):

    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    get_list = requests.get(request_url).json()

    if get_list['meta']['code'] == 200:
        if len(get_list['data']):
            print 'List of people who commented on post of user:'
            for i in range(len(get_list['data'])):
                print '%d :' %(i+1) + get_list['data'][i]['text']

        else:
            print 'There is no user present who commented on  your post!'
            exit()
    else:
        print 'error'
'''
Function declaration to get a post wtih minmum  likes
'''
def min_liked_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    temp=0
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            min=user_media['data'][0]['likes']['count']
            for i in range(len(user_media['data'])):
                if(min> user_media['data'][i]['likes']['count']):
                    min =user_media['data'][i]['likes']['count']
                    temp = i
            image_url = user_media['data'][temp]['images']['standard_resolution']['url']

            print 'Image URL :'+image_url
            print 'Id of post: ' + user_media['data'][temp]['id']
            print 'Likes in this post : %d' %user_media['data'][temp]['likes']['count']
            print '\n'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
Function declaration to get a post wtih search text in caption of post
'''

def caption_post(insta_username,txt):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            flag =0
            c=0
            for i in range(0, len(user_media['data'])):
                caption_text = user_media['data'][i]['caption']['text']
                if (txt in caption_text):
                    flag=flag+1
                    image_url = user_media['data'][i]['images']['standard_resolution']['url']
                    print '%d )' %flag
                    print 'Image URL :' + image_url
                    print 'Id of resulted post: ' + user_media['data'][i]['id']
                    print 'Caption on this post :' + user_media['data'][i]['caption']['text']
                    print '\n'

            if flag==0:
                print 'Post not fount with the given caption'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to select a particular  post by user crietria
'''

def choice_post(insta_username):
    print('Choose a post :')
    print ('1. The one with minimum number likes')
    print('2. Whose caption has a particular text')
    print ('3. Exit')
    while True:
        ch = int(raw_input('enter you option'))
        if ch == 1:
            min_liked_post(insta_username)
        elif ch ==2:
            txt = raw_input('Enter a text:')
            caption_post(insta_username,txt)
        elif ch == 3:
            exit()
        else:
            print('Wrong choice ..please enter again')


'''
Main program start here:
'''

def start_instabot():
    print 'Hey! Welcome to instaBot!'
    while True:
        print '\n'

        print 'Here are  menu options , choose one of them :'
        print "1.Get your own details"
        print "2.Get details of a user by username"
        print "3.Get your own recent post"
        print "4.Get the recent post of a user by username"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Delete comments by searching a word"
        print "11.Get comments of user's seleted post"
        print "12.Get a particular post through user criteria"
        print "13.Exit"

        choice=raw_input("Enter your choice: ")
        if choice=="1":
            self_info()
        elif choice=="2":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="3":
            get_own_post()
        elif choice=="4":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="5":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="6":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice=="7":
            insta_username = raw_input("Enter the username of the user: ")
            comment_list(insta_username)
        elif choice=="8":
            insta_username = raw_input("Enter the username of the user: ")
            comment_on_post(insta_username)
        elif choice=="9":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice=="10":
            insta_username = raw_input("Enter the username of the user: ")
            delete_comment(insta_username)
        elif choice == "11":
            insta_username = raw_input("Enter the username of the user: ")
            media_id = count_post(insta_username)
            get_post_comment(media_id)
        elif choice=="12":
            insta_username = raw_input("Enter the username of the user: ")
            choice_post(insta_username)

        elif choice=="13":
            print'Thankyou for using .Have a good day'
            exit()
        else:
            print "You have entered wrong choice..Enter a correct choice."
start_instabot()