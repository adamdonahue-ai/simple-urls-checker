A simple script that checks the status code of each URL in a list of URLs
and prints to stdout whether the status code returned is one of the
list of status codes provided, or otherwise reports an error.

Note that there is no throttling, so if we hammer thousands of endpoints
with the default settings we might get issues.  A delay or some other
logic would probably help here.  I didn't go crazy with optimizations.

I grabbed a bunch of URLs into a file with a quick one-liner:

```
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % curl https://downloads.majestic.com/majestic_million.csv | tail -n +2 | cut -d, -f3  | awk '{ print "https://" $1 }' > /tmp/urls
```

You can then run via Docker easily enough using -v to mount the urls.  Some sample input follows (truncated).

*NOTE: Some of the URLs return 4xx codes because the endpoints don't like that the aiohttp default headers aren't complete.*

```
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % docker build -t urls-checker:latest .
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % docker run -v /tmp:/foo urls-checker --urls-file /foo/urls
OK     https://github.com  [200]  retries=0
OK     https://apple.com  [200]  retries=0
OK     https://wordpress.org  [200]  retries=0
OK     https://en.wikipedia.org  [200]  retries=0
OK     https://x.com  [200]  retries=0
OK     https://vimeo.com  [200]  retries=0
ERROR  https://googletagmanager.com  [HTTP 404]  retries=3
OK     https://google.com  [200]  retries=0
OK     https://wikipedia.org  [200]  retries=0
OK     https://apps.apple.com  [200]  retries=0
OK     https://twitter.com  [200]  retries=0
OK     https://facebook.com  [200]  retries=0
OK     https://instagram.com  [200]  retries=0
OK     https://youtube.com  [200]  retries=0
OK     https://play.google.com  [200]  retries=0
OK     https://pinterest.com  [200]  retries=0
OK     https://nginx.org  [200]  retries=0
OK     https://youtu.be  [200]  retries=0
OK     https://wordpress.com  [200]  retries=0
OK     https://bit.ly  [200]  retries=0
ERROR  https://amazon.com  [HTTP 202]  retries=3
OK     https://docs.google.com  [200]  retries=0
OK     https://api.whatsapp.com  [200]  retries=0
OK     https://policies.google.com  [200]  retries=0
OK     https://linkedin.com  [200]  retries=0
OK     https://mozilla.org  [200]  retries=0
OK     https://apache.org  [200]  retries=0
OK     https://wa.me  [200]  retries=0
OK     https://f5.com  [200]  retries=0
OK     https://support.google.com  [200]  retries=0
OK     https://player.vimeo.com  [200]  retries=0
OK     https://whatsapp.com  [200]  retries=0
OK     https://plus.google.com  [200]  retries=0
ERROR  https://miit.gov.cn  [Cannot connect to host miit.gov.cn:443 ssl:default [Name or service not known]]  retries=3
OK     https://drive.google.com  [200]  retries=0
OK     https://github.io  [200]  retries=0
OK     https://itunes.apple.com  [200]  retries=0
OK     https://nginx.com  [200]  retries=0
OK     https://gravatar.com  [200]  retries=0
OK     https://tiktok.com  [200]  retries=0
OK     https://blogspot.com  [200]  retries=0
OK     https://mailinabox.email  [200]  retries=0
OK     https://nih.gov  [200]  retries=0
ERROR  https://goo.gl  [HTTP 400]  retries=3
OK     https://tumblr.com  [200]  retries=0
OK     https://open.spotify.com  [200]  retries=0
OK     https://archive.org  [200]  retries=0
ERROR  https://maps.app.goo.gl  [HTTP 400]  retries=3
ERROR  https://microsoft.com  [HTTP 403]  retries=3
OK     https://spotify.com  [200]  retries=0
OK     https://t.me  [200]  retries=0
OK     https://office.com  [200]  retries=0
ERROR  https://forms.gle  [HTTP 400]  retries=3
OK     https://europa.eu  [200]  retries=0
OK     https://yahoo.com  [200]  retries=0
OK     https://flickr.com  [200]  retries=0
ERROR  https://reddit.com  [HTTP 403]  retries=3
OK     https://creativecommons.org  [200]  retries=0
OK     https://sites.google.com  [200]  retries=0
OK     https://w3.org  [200]  retries=0
OK     https://www.ncbi.nlm.nih.gov  [200]  retries=0
OK     https://soundcloud.com  [200]  retries=0
OK     https://nytimes.com  [200]  retries=0
OK     https://zoom.us  [200]  retries=0
OK     https://forbes.com  [200]  retries=0
<snip>
```

# What About Alerting?

Given the streaming nature of the program, one way to do alerting (rather
than hard-coding it into the script, although that's certainly an option)
would be to add a flag to enable (or perhaps make default) a CSV
output mode, which could then be streamed into an alert handler,
or probably more flexibly an SQS/SNS (for AWS at least) that an alert
handler could read from/receive alerts from, decoupling these things.  I didn't
do that here but that might be one idea.
