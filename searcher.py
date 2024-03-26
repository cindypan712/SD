import praw 

class Searcher:
    def __init__(self, reddit, subreddit_name, filename_c='comments', filename_ci='comments info', filename_si='submissions info'):
        # reddit: praw.Reddit
        # subreddit_name: str 
        self.subreddit = reddit.subreddit(subreddit_name)
        self.f_comments = open(filename_c, 'w')
        self.f_comment_info = open(filename_ci, 'w')
        self.f_sub_info = open(filename_si, 'w')

    # in case we want to extract specific info 
    def submission_info(self, submission):
        # submission: praw.models.Submission
        return {
            'id': submission.id,
            'title': submission.title,
            'author': submission.author,
            'flair': submission.author_flair_text,
            'time': submission.created_utc,
            'selftext': submission.selftext,
            'url': submission.url
        }
    
    # in case we want to extract specific info 
    def comment_info(self, comment):
        # submission: praw.models.Comment
        return {
            'id': comment.id,
            'author': comment.author,
            'flair': comment.author_flair_text,
            'body': comment.body,
            'time': comment.created_utc,
            'score': comment.score,
            'replies': comment.replies
        }
    
    # check if we want to include this comment 
    def check_qualify(self, comment, threshold, flair_required=False):
        if len(comment.body.split()) < threshold:
            return False
        if flair_required:
            if comment.author_flair_text is None:
                return False
        return True 
        

    def search(self, limit=100, threshold=50):
        # file_name: str
        # limit: int; upper bounded on number of posts iterated 
        # threshold: int; at least this many words need to be in a comment for it to be included 
        self.top_posts = self.subreddit.top(limit=limit)
        # list of Submissions 
        self.submissions = []
        # list of list of top comments 
        self.tops = []
        acc1 = 0
        for p in self.top_posts:
            self.submissions.append(p)
            self.f_sub_info.write(str(acc1) + ':\n' + str(self.submission_info(p)) + '\n\n')
            forest = p.comments
            # iterates over top level comments 
            tops = []
            acc2 = 0
            for i in range(len(forest)-1):
                comment = forest[i]
                # filtering word count less than a threshold
                if self.check_qualify(comment, threshold, flair_required=True) == False:
                    continue 
                tops.append(comment)
                self.f_comments.write(str(acc1) + ', ' + str(acc2) + ':\n' + comment.body + '\n\n')
                self.f_comment_info.write(str(acc1) + ', ' + str(acc2) + ':\n' + str(self.comment_info(comment)) + '\n\n')
                acc2 += 1
            self.tops.append(tops)
            acc1 += 1
            self.f_comments.flush()