class OAuthExample(object):
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self, name, balance=0.0):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        accesstoken = "3746388736-JDPGK6qvv7EtyVPhtb2zj00kPqf1oRh2GAsYo87";
        accesssecret = "lEftplmzq0Mn8HgygHnlDERI7MJ7TcjzX4DTQ0qvwYZG1";
        OAuthTokenSecret tokensecret = new OAuthTokenSecret(accesstoken, accesssecret);
        return tokensecret;

    def GetUserAccessKeySecret(self):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        try {
        // consumer key for Twitter Data Analytics application
        if (OAuthUtils.CONSUMER_KEY.isEmpty())
        {
        System.out.println("Register an application and copy the consumer key into the configuration file.");
        return null;
        }
        if (OAuthUtils.CONSUMER_SECRET.isEmpty())
        {
        System.out.println("Register an application and copy the consumer secret into the configuration file.");
        return null;

        }
        OAuthConsumer
        consumer = new
        CommonsHttpOAuthConsumer(OAuthUtils.CONSUMER_KEY, OAuthUtils.CONSUMER_SECRET);
        OAuthProvider
        provider = new
        DefaultOAuthProvider(OAuthUtils.REQUEST_TOKEN_URL, OAuthUtils.ACCESS_TOKEN_URL, OAuthUtils.AUTHORIZE_URL);
        String
        authUrl = provider.retrieveRequestToken(consumer, OAuth.OUT_OF_BAND);
        System.out.println("Now visit:\n" + authUrl + "\n and grant this app authorization");
        System.out.println("Enter the PIN code and hit ENTER when you're done:");
        BufferedReader
        br = new
        BufferedReader(new
        InputStreamReader(System. in));
        String
        pin = br.readLine();
        System.out.println("Fetching access token from Twitter");
        provider.retrieveAccessToken(consumer, pin);
        String
        accesstoken = consumer.getToken();
        String
        accesssecret = consumer.getTokenSecret();
        OAuthTokenSecret
        tokensecret = new
        OAuthTokenSecret(accesstoken, accesssecret);
        return tokensecret;

        } catch(OAuthNotAuthorizedException
        ex) {
        ex.printStackTrace();
        } catch(OAuthMessageSignerException
        ex) {
        ex.printStackTrace();
        } catch(OAuthExpectationFailedException
        ex) {
        ex.printStackTrace();
        } catch(OAuthCommunicationException
        ex) {
        ex.printStackTrace();
        } catch(IOException
        ex)
        {
        ex.printStackTrace();
        }
        return null;

