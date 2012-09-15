from rauth.service import OAuth1Service #see https://github.com/litl/rauth for more info
import shelve #for persistent caching of tokens, hashes,etc.
import time
import datetime 
#get your own consumer key and secret by emailing zeo.
#for more details on the API: https://wiki.zeo.com/display/API/zeo+Resource+Access+API

class Zeo:
    def __init__(self,consumer_key,consumer_secret,api_key,referer,callback_url,verbose=0,cache_name='tokens.dat'):
        #cache stores tokens and hashes on disk so we avoid
        #requesting them every time.
        self.cache=shelve.open(cache_name,writeback=False)
        self.verbose=verbose        
        self.oauth=OAuth1Service(
                name='zeo',
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                request_token_url='http://api.myzeo.com:8080/zeows/oauth/request_token',
                access_token_url='http://api.myzeo.com:8080/zeows/oauth/access_token',
                authorize_url='http://api.myzeo.com:8080/zeows/oauth/confirm_access',
                header_auth=False)

        self.api_key = api_key
        self.referer = referer
        self.callback_url = callback_url
        self.access_token = self.cache.get('zeo_access_token',None)
        self.access_token_secret = self.cache.get('zeo_access_token_secret',None)
        self.request_token =  self.cache.get('zeo_request_token',None)
        self.request_token_secret =  self.cache.get('zeo_request_token_secret',None)
        self.pin= self.cache.get('zeo_pin',None)
        
        #If this is our first time running- get new tokens 
        if (self.need_request_token()):
            self.get_request_token()
            got_access_token=self.get_access_token()
            if( not got_access_token):
                print "Error: Unable to get access token"
                    

    def dbg_print(self,txt):
        if self.verbose==1:
            print txt

    def get_request_token(self):
        self.dbg_print("in get_request_token")
        self.request_token,self.request_token_secret = self.oauth.get_request_token(method='GET')
        self.dbg_print("request token: "+self.request_token)
        self.dbg_print( "self.request_token_secret = "+self.request_token_secret)
        authorize_url=self.oauth.get_authorize_url(self.request_token,callbackURL=self.callback_url)
        #the pin you want here is the string that appears after oauth_verifier on the page served
        #by the authorize_url
        print 'Visit this URL in your browser then login: ' + authorize_url
        self.pin = raw_input("Enter the string after oauth_verifier= from your browser's address bar (at the very end of the URL): ")
        self.cache['zeo_request_token']=self.request_token
        self.cache['zeo_request_token_secret']=self.request_token_secret
        self.cache['zeo_pin']=self.pin
        print "zeo_pin is ",self.cache.get('zeo_pin')

    def need_request_token(self):
        #created this method because i'm not clear when request tokens need to be obtained, or how often
        if (self.request_token==None) or (self.request_token_secret==None) or (self.pin==None):
            return True
        else:
            return False

    def get_access_token(self):
        self.dbg_print("in get_access_token ")
        response=self.oauth.get_access_token('GET',
                request_token=self.request_token,
                request_token_secret=self.request_token_secret,
                params={'oauth_verifier':self.pin})
        data=response.content
        print response.content
        self.access_token=data.get('oauth_token',None)
        self.access_token_secret=data.get('oauth_token_secret',None)
        self.cache['zeo_access_token']=self.access_token
        self.cache['zeo_access_token_secret']=self.access_token_secret
        if not(self.access_token) or not(self.access_token_secret):
            print "access token expired "
            return False
        else:
            return True

    
    def apiRequest(self,action_name,params={}):
        """generic request method used by most other methods in this class"""
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        #note that regardless of what weightUnit is set to, the value of 'weight' is returned in kg
        #you must pass the URL you registered with as your Referer value or you'll get this error:
        #"API Key does not match caller domain"
        headers={'Referer':self.referer}
        params['key'] = self.api_key
        response=self.oauth.get(
                'http://api.myzeo.com:8080/zeows/api/v1/json/sleeperService/%s' % (action_name),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                headers=headers,
                header_auth=False)
        return response.content

    def getOverallAverageZQScore(self,params={}):
        """getOverallAverageZQScore(self)"""
        return self.apiRequest("getOverallAverageZQScore")

    def getOverallAverageDayFeelScore(self,params={}):
        """getOverallAverageDayFeelScore(self)"""
        return self.apiRequest("getOverallAverageDayFeelScore")

    def getOverallAverageMorningFeelScore(self,params={}):
        """getOverallAverageMorningFeelScore(self)"""
        return self.apiRequest("getOverallAverageMorningFeelScore")

    def getOverallAverageSleepStealerScore(self,params={}):
        """getOverallAverageSleepStealerScore(self)"""
        return self.apiRequest("getOverallAverageSleepStealerScore")

    def getAllDatesWithSleepData(self,params={}):
        """getAllDatesWithSleepData(self)"""
        return self.apiRequest("getAllDatesWithSleepData")

    def getDatesWithSleepDataInRange(self,dateFrom=None,dateTo=None):
        """getDatesWithSleepDataInRange(self,dateFrom,dateTo)
        The dateFrom and dateTo parameters define the limits of dates to check for
        sleep data. Note that dateFrom and dateTo are inclusive values, i.e if dateFrom=2012-09-12 and 
        dateTo=2012-09-14 you will receive results for 2012-09-12,2012-09-13, and 2012-09-14.
        """
        params={}
        if dateFrom is not None:
            params['dateFrom'] = dateFrom
        if dateTo is not None:
            params['dateTo'] = dateTo
        return self.apiRequest("getDatesWithSleepDataInRange",params)

    def getSleepStatsForDate(self,date=None):
        """
        getSleepStatsForDate(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getSleepStatsForDate",params)

    def getSleepRecordForDate(self,date=None):
        """
        getSleepRecordForDate(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getSleepRecordForDate",params)

    def getPreviousSleepStats(self,date=None):
        """
        getPreviousSleepStats(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getPreviousSleepStats",params)

    def getPreviousSleepRecord(self,date=None):
        """
        getPreviousSleepRecord(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getPreviousSleepRecord",params)

    def getNextSleepStats(self,date=None):
        """
        getNextSleepStats(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getNextSleepStats",params)
    
    def getNextSleepRecord(self,date=None):
        """
        getNextSleepRecord(self,date=None)
        If no date is specified, the current date will be used
        """
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        params={'date':date}
        return self.apiRequest("getNextSleepRecord",params)

    def getEarliestSleepStats(self):
        """
        getEarliestSleepStats(self)
        """
        return self.apiRequest("getEarliestSleepStats")

