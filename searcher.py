import praw 
import json
import datetime


class Searcher:
    def __init__(self, reddit, subreddit_name):
        # reddit: praw.Reddit
        # subreddit_name: str 
        self.subreddit = reddit.subreddit(subreddit_name)
        self.submissions_dict = {}
        self.comments_dict = {}
        self.comments = {}

    
    # helper function to write readable lines 
    def split_into_chunks(self, text, chunk_size=80):
        """Split text into chunks of specified size."""
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # in case we want to extract specific info 
    def add_submission_info(self, submission):
        # submission: praw.models.Submission
        if submission.id in self.submissions_dict:
            return 
        sub_info = {
            'title': str(submission.title),
            'author': str(submission.author),
            'flair': str(submission.author_flair_text),
            'time': str(submission.created_utc),
            'selftext': str(submission.selftext),
            'url': str(submission.url)
        }
        self.submissions_dict[submission.id] = sub_info
    
    # in case we want to extract specific info 
    def add_comment_info(self, comment, submission_id):
        # comment: praw.models.Comment
        # submission_id: str 
        if comment.id in self.comments_dict:
            return 
        comment_info = {
            'id': str(comment.id),
            'author': str(comment.author),
            'time': str(datetime.datetime.fromtimestamp(comment.created_utc)),
            'flair': str(comment.author_flair_text),
            'body': comment.body,
            'number of upvotes': str(comment.score),
            'parent submission id': submission_id,
            'number of top-level replies': len(comment.replies)
        }
        self.comments_dict[comment.id] = comment_info
        self.comments[comment.id] = {'body': comment.body,
                                     'parent submission id': submission_id}

    
    # check if we want to include this comment 
    def check_qualify(self, comment, threshold, flair_required=False):
        if len(comment.body.split()) < threshold:
            return False
        if flair_required:
            if comment.author_flair_text is None:
                return False
        return True 
        

    def search(self, limit=2, threshold=50):
        # file_name: str
        # limit: int; upper bounded on number of posts iterated 
        # threshold: int; at least this many words need to be in a comment for it to be included 
        self.top_posts = self.subreddit.top(limit=limit)
        # dictionary of Submissions 
        # list of list of top comments??? 
        for p in self.top_posts:
            self.add_submission_info(p)
            forest = p.comments
            # iterates over top level comments 
            for i in range(len(forest)-1):
                comment = forest[i]
                # filtering word count less than a threshold
                if self.check_qualify(comment, threshold, flair_required=True) == False:
                    continue 
                self.add_comment_info(comment, str(p.id))
    
    def write_to(self, filename_c='comments.txt', filename_ci='comments_info.txt', filename_si='submissions_info.txt'):
        f_comments = open(filename_c, 'w')
        json_comments = json.dumps(self.comments, indent=5)
        chunks = self.split_into_chunks(json_comments)
        for chunk in chunks:
            f_comments.write(chunk + '\n')
        f_comments.close()
        f_comment_info = open(filename_ci, 'w')
        json.dump(self.comments_dict, f_comment_info, indent=5)
        f_comment_info.close()
        f_sub_info = open(filename_si, 'w')
        json.dump(self.submissions_dict, f_sub_info, indent=5)
        f_sub_info.close()
